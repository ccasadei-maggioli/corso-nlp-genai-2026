#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore di un dataset SINTETICO di recensioni clienti in italiano.

Perché sintetico?
- È riproducibile (seed fisso => sempre lo stesso dataset).
- Non richiede download esterni né pone problemi di licenza/privacy.
- Possiamo controllarne le caratteristiche (aspetti, tono, casi ambigui)
  per renderlo didatticamente utile in tutte le lezioni del corso.

Il dataset simula recensioni di prodotti e-commerce, con:
- prodotto e relativa categoria merceologica,
- valutazione in stelle (rating 1-5),
- data,
- titolo e testo della recensione.

NOTA: il "sentiment" e gli "aspetti" (spedizione, prezzo, qualità, assistenza...)
NON sono salvati come colonne: li RICAVEREMO con i modelli nelle Lezioni 3-6.
Questo è esattamente lo scopo del corso.

Uso:
    python genera_recensioni.py                 # 200 recensioni -> recensioni.csv
    python genera_recensioni.py --n 500         # 500 recensioni
    python genera_recensioni.py --output /tmp/r.csv --seed 7

Richiede solo la libreria standard di Python (nessuna dipendenza esterna).
"""

import argparse
import csv
import random
from datetime import date, timedelta

# --------------------------------------------------------------------------- #
# Catalogo prodotti: (nome prodotto, categoria merceologica)
# --------------------------------------------------------------------------- #
PRODOTTI = [
    ("Cuffie Bluetooth XSound Pro", "Elettronica"),
    ("Smartwatch FitPro 2", "Elettronica"),
    ("Aspirapolvere senza filo CicloneMax", "Casa"),
    ("Zaino da trekking TrekLite 30L", "Sport e tempo libero"),
    ("Caffè in cialde Aroma Intenso (100 pz)", "Alimentari"),
    ("Monitor UltraView 27 pollici", "Elettronica"),
    ("Frullatore ad alta velocità VitaBlend", "Casa"),
    ("Scarpe da running AeroStep", "Sport e tempo libero"),
    ("Powerbank ChargeGo 20000mAh", "Elettronica"),
    ("Tastiera meccanica KeyForge RGB", "Elettronica"),
    ("Set lenzuola in cotone SoffiCotone", "Casa"),
    ("Macchina per il pane HomeBaker", "Casa"),
]

# --------------------------------------------------------------------------- #
# Banca di frasi per "aspetto" (es. spedizione, prezzo...) divise per tono.
# Ogni recensione viene composta combinando alcuni di questi frammenti in modo
# coerente con il numero di stelle, così da ottenere testi vari e realistici.
# --------------------------------------------------------------------------- #
ASPETTI = {
    "spedizione": {
        "pos": [
            "La spedizione è stata velocissima, arrivato in un giorno.",
            "Consegna puntuale e nei tempi previsti.",
            "Pacco arrivato prima del previsto, ottimo.",
        ],
        "neg": [
            "La spedizione ha tardato parecchi giorni rispetto alla stima.",
            "Consegna in ritardo e nessun aggiornamento sul tracciamento.",
            "Ho aspettato due settimane per la consegna, troppo.",
        ],
    },
    "imballaggio": {
        "pos": [
            "Imballaggio curato e prodotto ben protetto.",
            "Confezione ordinata e sostenibile.",
        ],
        "neg": [
            "La scatola è arrivata ammaccata e mal imballata.",
            "Imballaggio insufficiente, il prodotto ballava dentro la scatola.",
        ],
    },
    "prezzo": {
        "pos": [
            "Ottimo rapporto qualità-prezzo.",
            "Prezzo onesto per quello che offre.",
            "In offerta è un vero affare.",
        ],
        "neg": [
            "Troppo caro per quello che offre.",
            "Il prezzo non è giustificato dalla qualità.",
            "Si trova di meglio allo stesso prezzo.",
        ],
    },
    "qualità": {
        "pos": [
            "Materiali solidi e ben rifiniti.",
            "Qualità costruttiva eccellente, si sente che è robusto.",
            "Costruzione curata nei dettagli.",
        ],
        "neg": [
            "Materiali scadenti, sembra un prodotto economico.",
            "Si è rotto dopo pochi giorni di utilizzo.",
            "Plastica fragile, non lo ricomprerei.",
        ],
    },
    "prestazioni": {
        "pos": [
            "Funziona alla grande, prestazioni sopra le aspettative.",
            "Fa esattamente quello che promette, molto efficiente.",
            "Prestazioni ottime anche sotto sforzo.",
        ],
        "neg": [
            "Prestazioni deludenti, molto al di sotto delle aspettative.",
            "Lento e poco reattivo nell'uso quotidiano.",
            "Non funziona bene come pubblicizzato.",
        ],
    },
    "durata_batteria": {
        "pos": [
            "La batteria dura tantissimo, anche un paio di giorni.",
            "Autonomia eccellente, la ricarico raramente.",
        ],
        "neg": [
            "La batteria si scarica in poche ore, autonomia pessima.",
            "Durata della batteria molto inferiore a quanto dichiarato.",
        ],
    },
    "facilità_uso": {
        "pos": [
            "Semplicissimo da configurare e usare.",
            "Intuitivo fin da subito, nessun manuale necessario.",
        ],
        "neg": [
            "Configurazione complicata e istruzioni poco chiare.",
            "Interfaccia confusionaria, ci ho messo ore a capirlo.",
        ],
    },
    "assistenza": {
        "pos": [
            "Assistenza clienti gentile e rapida nel rispondere.",
            "Ho contattato il supporto e hanno risolto subito.",
        ],
        "neg": [
            "Assistenza clienti pessima, non rispondono alle email.",
            "Ho chiesto un rimborso ma il supporto è stato inutile.",
        ],
    },
    "estetica": {
        "pos": [
            "Esteticamente molto bello, design elegante.",
            "Bel design, fa la sua figura.",
        ],
        "neg": [
            "Esteticamente deludente, sembra diverso dalle foto.",
            "Il colore reale è diverso da quello mostrato online.",
        ],
    },
}

# Aperture e chiusure per dare un tono coerente con il rating.
APERTURE = {
    5: ["Prodotto fantastico!", "Sono entusiasta.", "Acquisto azzeccato."],
    4: ["Nel complesso sono soddisfatto.", "Buon prodotto.", "Mi trovo bene."],
    3: ["Esperienza nella media.", "Né carne né pesce.", "Prodotto con luci e ombre."],
    2: ["Un po' deluso, sinceramente.", "Mi aspettavo di più.", "Non sono soddisfatto."],
    1: ["Pessima esperienza.", "Esperienza da dimenticare.", "Lo sconsiglio."],
}
CHIUSURE = {
    5: ["Lo ricomprerei senza dubbio.", "Consigliatissimo!", "Cinque stelle meritate."],
    4: ["Lo consiglio.", "Promosso, con piccole riserve.", "Buon acquisto."],
    3: ["Valutate bene prima di acquistare.", "Dipende dalle vostre esigenze.", "Così così."],
    2: ["Probabilmente non lo ricomprerei.", "Ci ripenserei due volte.", "Deludente."],
    1: ["Da evitare.", "Soldi buttati.", "Mai più."],
}

# Per ogni numero di stelle: quanti aspetti POSITIVI e NEGATIVI mescolare.
# Es. con 3 stelle mettiamo 1 pro e 1 contro -> recensione "ambigua" (utile!).
MIX_PER_RATING = {
    5: (3, 0),
    4: (2, 1),
    3: (1, 1),
    2: (1, 2),
    1: (0, 3),
}

# Titoli brevi coerenti con il rating.
TITOLI = {
    5: ["Top!", "Promosso a pieni voti", "Lo adoro", "Eccellente"],
    4: ["Buono", "Soddisfatto", "Bel prodotto", "Consigliato"],
    3: ["Nella media", "Alti e bassi", "Si poteva fare meglio", "Insomma..."],
    2: ["Deludente", "Mi aspettavo di più", "Poco convincente", "Non ci siamo"],
    1: ["Pessimo", "Da evitare", "Una delusione totale", "Sconsigliato"],
}

# Distribuzione (volutamente non uniforme) delle stelle: più recensioni
# positive, come capita spesso nei dataset reali.
PESI_RATING = {5: 0.34, 4: 0.26, 3: 0.14, 2: 0.12, 1: 0.14}


def _scegli_aspetti(rng, prodotto_categoria, n_pos, n_neg):
    """Sceglie aspetti coerenti col prodotto e ne estrae frasi pos/neg."""
    disponibili = list(ASPETTI.keys())
    # La "durata_batteria" ha senso quasi solo per l'elettronica.
    if prodotto_categoria != "Elettronica" and "durata_batteria" in disponibili:
        disponibili.remove("durata_batteria")

    rng.shuffle(disponibili)
    frasi = []
    usati = []
    for aspetto in disponibili:
        if len(usati) >= (n_pos + n_neg):
            break
        usati.append(aspetto)

    # Assegna i primi n_pos aspetti come positivi e i successivi come negativi.
    for i, aspetto in enumerate(usati):
        tono = "pos" if i < n_pos else "neg"
        frasi.append(rng.choice(ASPETTI[aspetto][tono]))
    rng.shuffle(frasi)
    return frasi


def _genera_una(rng, id_, data_riferimento):
    """Genera un singolo record di recensione (dict)."""
    prodotto, categoria = rng.choice(PRODOTTI)

    # Estrae il rating secondo la distribuzione pesata.
    stelle = rng.choices(
        population=list(PESI_RATING.keys()),
        weights=list(PESI_RATING.values()),
        k=1,
    )[0]

    n_pos, n_neg = MIX_PER_RATING[stelle]
    corpo = _scegli_aspetti(rng, categoria, n_pos, n_neg)

    testo = " ".join(
        [rng.choice(APERTURE[stelle])] + corpo + [rng.choice(CHIUSURE[stelle])]
    )

    # Data: offset deterministico (in base al seed) negli ultimi ~600 giorni.
    giorni = rng.randint(0, 600)
    data = data_riferimento - timedelta(days=giorni)

    return {
        "id": id_,
        "data": data.isoformat(),
        "prodotto": prodotto,
        "categoria": categoria,
        "rating": stelle,
        "titolo": rng.choice(TITOLI[stelle]),
        "testo": testo,
    }


def genera_recensioni(n=200, seed=42):
    """Restituisce una lista di n recensioni (lista di dict) deterministica."""
    rng = random.Random(seed)
    # Data di riferimento FISSA per garantire la riproducibilità.
    data_riferimento = date(2026, 3, 1)
    return [_genera_una(rng, i + 1, data_riferimento) for i in range(n)]


def salva_csv(recensioni, percorso):
    """Salva le recensioni in un file CSV UTF-8."""
    campi = ["id", "data", "prodotto", "categoria", "rating", "titolo", "testo"]
    with open(percorso, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campi)
        writer.writeheader()
        writer.writerows(recensioni)


def main():
    parser = argparse.ArgumentParser(
        description="Genera un dataset sintetico di recensioni clienti in italiano."
    )
    parser.add_argument("--n", type=int, default=200, help="numero di recensioni")
    parser.add_argument(
        "--output", default="recensioni.csv", help="percorso del file CSV di output"
    )
    parser.add_argument("--seed", type=int, default=42, help="seed per la riproducibilità")
    args = parser.parse_args()

    recensioni = genera_recensioni(n=args.n, seed=args.seed)
    salva_csv(recensioni, args.output)

    # Riepilogo a video.
    distrib = {}
    for r in recensioni:
        distrib[r["rating"]] = distrib.get(r["rating"], 0) + 1
    print(f"Generate {len(recensioni)} recensioni -> {args.output}")
    print("Distribuzione stelle:", dict(sorted(distrib.items(), reverse=True)))
    print("\nEsempio:")
    esempio = recensioni[0]
    print(f"  [{esempio['rating']}★] {esempio['titolo']} — {esempio['prodotto']}")
    print(f"  {esempio['testo']}")


if __name__ == "__main__":
    main()
