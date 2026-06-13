# Corso: NLP & Generative AI con modelli open source 🇮🇹

Materiale completo del corso pratico **Maggioli Academy** su **NLP** (Natural Language Processing) e
**Generative AI** pensato per **sviluppatori** che conoscono Python ma non hanno
ancora lavorato con gli LLM e gli altri modelli di Intelligenza Artificiale.

Il corso usa **solo modelli open source scaricabili da Hugging Face** (nessuna API
key da gestire) ed è progettato per girare sulla **GPU T4 gratuita di Google Colab**.
Come framework per la Generative AI usiamo **LangChain**.

> 🎯 **Filo conduttore:** in tutte le lezioni lavoriamo sullo stesso scenario reale —
> l'**analisi di recensioni clienti in italiano** — costruendo pezzo dopo pezzo i
> mattoni che confluiscono nel **progetto finale**: un'app che arricchisce le
> recensioni (sentiment, entità, categorie, riassunti) e risponde a domande tramite
> **RAG** (Retrieval-Augmented Generation).

---

## 🚀 Come eseguire i notebook su Google Colab

Hai due strade. La **più semplice** è il pulsante *Open in Colab* qui sotto.

### Opzione A — Pulsante "Open in Colab" (consigliata)

Clicca il badge della lezione che ti interessa: il notebook si apre direttamente in Colab.

| Lezione                                               | Apri in Colab                                                                                                                                                                                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 · Introduzione a NLP & GenAI + Setup                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ccasadei-maggioli/corso-nlp-genai-2026/blob/main/lezione_1_introduzione/notebook_01_introduzione.ipynb)         |
| 2 · Embeddings & ricerca semantica                    | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ccasadei-maggioli/corso-nlp-genai-2026/blob/main/lezione_2_embeddings/notebook_02_embeddings.ipynb)             |
| 3 · Modelli task-specific (sentiment, NER, zero-shot) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ccasadei-maggioli/corso-nlp-genai-2026/blob/main/lezione_3_pipelines_ner_sentiment/notebook_03_pipelines.ipynb) |
| 4 · LLM generativi open source su T4                  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ccasadei-maggioli/corso-nlp-genai-2026/blob/main/lezione_4_llm_generativi/notebook_04_llm_generativi.ipynb)     |
| 5 · LangChain: dal modello all'app                    | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ccasadei-maggioli/corso-nlp-genai-2026/blob/main/lezione_5_langchain/notebook_05_langchain.ipynb)               |
| 6 · Progetto finale: analisi recensioni + RAG         | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ccasadei-maggioli/corso-nlp-genai-2026/blob/main/lezione_6_progetto_finale_rag/notebook_06_progetto_rag.ipynb)  |

### Opzione B — Clonare il repo dentro Colab

Apri un notebook Colab vuoto e in una cella esegui:

```python
!git clone https://github.com/ccasadei-maggioli/corso-nlp-genai-2026.git
%cd corso-nlp-genai-2026
```

Poi apri il notebook della lezione dal pannello file di Colab.

### 🔗 Link rapido al repository

- URL completo: **https://github.com/ccasadei-maggioli/corso-nlp-genai-2026**

- Link breve (TinyURL): **https://tinyurl.com/259ql6gw**

- QR code (punta al link breve):
  
  ![QR code del repository](assets/qr_repo.png)

---

## ⚙️ IMPORTANTE: attivare la GPU T4

Quasi tutti i notebook caricano modelli su GPU. **Prima di eseguire le celle**:

1. Menu **`Runtime`** (in italiano: *Runtime* / *Ambiente di esecuzione*)
2. **`Change runtime type`** (*Cambia tipo di runtime*)
3. Alla voce **Hardware accelerator** seleziona **`T4 GPU`**
4. Premi **`Save`** (*Salva*)

Verifica che la GPU sia attiva eseguendo nel notebook:

```python
import torch
print("GPU disponibile:", torch.cuda.is_available())
print("Modello GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "—")
```

Se vedi `Tesla T4` sei pronto. ✅

> ⏱️ **Nota sui tempi:** il modello generativo principale (Qwen2.5-7B in 4-bit) è
> potente ma su T4 impiega qualche secondo per rispondere. È normale. Nei notebook
> trovi una variante più leggera (Qwen2.5-3B) se preferisci risposte più rapide.

---

## 🗂️ Struttura del repository

```
.
├── README.md                          # questo file
├── requirements.txt                   # dipendenze di riferimento
├── dati/
│   └── genera_recensioni.py           # genera il dataset di recensioni italiane (riproducibile)
├── assets/                            # QR code e immagini di supporto
├── lezione_1_introduzione/
│   ├── notebook_01_introduzione.ipynb
│   ├── slides.pdf                     # slide esportate 
├── lezione_2_embeddings/
├── lezione_3_pipelines_ner_sentiment/
├── lezione_4_llm_generativi/
├── lezione_5_langchain/
└── lezione_6_progetto_finale_rag/
```

Ogni cartella `lezione_*` contiene gli stessi materiali: **notebook**, **slides**.

---

## 📚 Programma del corso (6 lezioni da ~20 minuti)

1. **Introduzione a NLP & GenAI + Setup** — cosa sono NLP, LLM e GenAI; l'ecosistema
   Hugging Face + LangChain; setup di Colab e prima `pipeline` di analisi.
2. **Embeddings & ricerca semantica** — come si rappresenta il testo in vettori,
   similarità coseno, ricerca semantica su recensioni.
3. **Modelli task-specific** — sentiment, NER (estrazione entità) e classificazione
   zero-shot con le `pipeline` di Hugging Face.
4. **LLM generativi open source su T4** — caricare Qwen2.5 con quantizzazione 4-bit,
   generare testo, riassumere, prompting efficace.
5. **LangChain** — dal modello all'applicazione: prompt template, catene (LCEL),
   output strutturato (JSON) e memoria conversazionale.
6. **Progetto finale: analisi recensioni + RAG** — mettiamo tutto insieme in un'app
   che risponde a domande sulle recensioni citando le fonti.

---

## 🔬 Risorse interattive esterne (citate nelle lezioni)

Per visualizzare concetti astratti usiamo alcuni strumenti online:

- **TensorFlow Embedding Projector** — visualizzare lo "spazio latente"/embeddings:
  [https://projector.tensorflow.org]()
- **The Illustrated Transformer** (Jay Alammar) — capire i Transformer:
  [https://jalammar.github.io/illustrated-transformer/]()
- **Tokenizer playground** — vedere come il testo viene spezzato in token:
  [https://huggingface.co/spaces/Xenova/the-tokenizer-playground]()

---

## 🧠 Modelli usati (tutti open e scaricabili senza API key)

| Compito                    | Modello Hugging Face                                                 |
| -------------------------- | -------------------------------------------------------------------- |
| Generazione testo (LLM)    | `Qwen/Qwen2.5-7B-Instruct` (4-bit) · alt. `Qwen/Qwen2.5-3B-Instruct` |
| Embeddings (multilingue)   | `intfloat/multilingual-e5-base`                                      |
| Sentiment (italiano)       | `neuraly/bert-base-italian-cased-sentiment`                          |
| NER / entità (multilingue) | `Babelscape/wikineural-multilingual-ner`                             |
| Classificazione zero-shot  | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`                            |

---

## 📝 Note

- I notebook installano da soli le dipendenze necessarie (`!pip install ...`).
- Il dataset di recensioni è **generato** dallo script `dati/genera_recensioni.py`
  (seed fisso → risultati riproducibili): nessun download esterno, nessun problema
  di licenza.
- Materiale didattico in **italiano**, a scopo formativo.

## ⚖️ Licenza

Codice e materiali rilasciati a scopo formativo. 

I modelli scaricati da **Hugging Face** restano soggetti alle rispettive licenze (es. Apache-2.0 per Qwen2.5).

Il corso è proprietà di **Maggioli Academy**.
