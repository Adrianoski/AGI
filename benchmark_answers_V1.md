# Benchmark RAG — StoriaNew

**Modello:** Qwen/Qwen3.5-4B  |  **top-k:** 5  |  **top-N SLM:** 3

| Metrica | StdRAG | SLM-RAG |
|---|---|---|
| Speedup retrieval | — | **3.1x** |
| Pool medio | 203 chunk | 26 chunk (-87%) |
| Keyword hit | 48% | **77%** |
| Overlap medio top-5 | 28% | — |

---

## 1. Who imported spices into Europe during the Middle Ages?

*da chi venivano importate le spezie in europa nel medioevo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.7 ms | 3.2 ms (4.5x) |
| **Generazione** | 4192 ms | 786 ms |
| **Totale** | 4206 ms | 789 ms |
| **Pool chunk** | 203 | 5 |
| **Keyword hit** | 0% | 100% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

Le spezie venivano importate in Europa nel Medioevo dai mercanti arabi e dalla repubblica veneziana.

---

## 2. What territories did Charles V control?

*quali territori controllava Carlo V?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.0 ms | 3.1 ms (4.8x) |
| **Generazione** | 2514 ms | 465 ms |
| **Totale** | 2529 ms | 469 ms |
| **Pool chunk** | 203 | 4 |
| **Keyword hit** | 83% | 50% |

### Risposta StdRAG

Carlo V controllava i seguenti territori:
*   L'impero spagnolo, un vasto territorio che comprendeva la Spagna, territori nell'Italia meridionale, la Sardegna e territori del Nuovo Mondo (ereditati dalla madre Giovanna la Pazza).
*   I domini asburgici in Austria (ereditati dal nonno Massimiliano d'Asburgo).
*   La Franca Contea, le Fiandre e i Paesi Bassi (ottenuti in eredità dalla nonna Maria di Borgogna).

### Risposta SLM-RAG

The answer is not available in the provided context.

---

## 3. What were the main causes of the French Revolution?

*quali furono le cause della rivoluzione francese?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.7 ms | 4.1 ms (3.6x) |
| **Generazione** | 2061 ms | 547 ms |
| **Totale** | 2076 ms | 551 ms |
| **Pool chunk** | 203 | 11 |
| **Keyword hit** | 33% | 50% |

### Risposta StdRAG

The answer is not available in the provided context.

Although Chunk 2 lists a section titled "Premesse della Rivoluzione: la crisi economica" (Premises of the Revolution: the economic crisis) and "Opinione pubblica e convocazione degli Stati Generali" (Public opinion and convocation of the Estates-General), the actual text describing these causes is not included in the provided context snippets. Only the table of contents is available.

### Risposta SLM-RAG

The answer is not available in the provided context.

---

## 4. How did James Watt's steam engine work?

*come funzionava la macchina a vapore di james watt?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.4 ms | 3.8 ms (3.8x) |
| **Generazione** | 489 ms | 501 ms |
| **Totale** | 504 ms | 505 ms |
| **Pool chunk** | 203 | 8 |
| **Keyword hit** | 67% | 67% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

---

## 5. What were the key principles of the Enlightenment?

*quali erano i principi fondamentali dell'illuminismo?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 15.5 ms | 4.3 ms (3.6x) |
| **Generazione** | 466 ms | 5284 ms |
| **Totale** | 482 ms | 5288 ms |
| **Pool chunk** | 203 | 13 |
| **Keyword hit** | 17% | 50% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

In base al contesto fornito, i principi fondamentali dell'Illuminismo sono:

*   **La ragione:** È il "lume naturale" dell'uomo che sollecita a svincolarsi dalle tradizioni e dai pregiudizi per affermare un nuovo modo di guardare la realtà, la società, la politica, la cultura e la religione.
*   **Il coraggio di usare la propria intelligenza:** Espresso dal motto di Kant "Sapere aude!".
*   **La diffusione del sapere:** L'obiettivo di rendere il sapere disponibile a tutti, come intendeva l'*Enciclopedia*.
*   **La libertà di stampa:** Un principio attuato da sovrani illuminati (come in Prussia) e sollecitato dai filosofi.
*   **La tolleranza:** Promossa per favorire lo scambio culturale tra popolazioni di etnia diversa.
*   **La condanna della tortura e della schiavitù:** Principi difesi da filosofi come Voltaire.
*   **La lotta all'analfabetismo:** Obiettivo perduto per la nobiltà ma sostenuto dal movimento.
*   **Il miglioramento della condizione economica e sociale:** Bas

---

## 6. What was the American Revolution?

*che cosa fu la rivoluzione americana?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.2 ms | 3.2 ms (4.5x) |
| **Generazione** | 502 ms | 3666 ms |
| **Totale** | 516 ms | 3669 ms |
| **Pool chunk** | 203 | 8 |
| **Keyword hit** | 50% | 100% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

La Rivoluzione americana definisce l'insieme delle vicende che portarono alla nascita degli Stati Uniti d'America, tra il 1763 e il 1787. Fu la concreta applicazione dei principi dell'Illuminismo, che difende i diritti del singolo e del popolo contro il despotismo delle autorità. Il conflitto iniziò con scontri tra inglesi e americani, inizialmente le forze inglesi, meglio organizzate, prevalsero, poi prevalsero le vittorie dei coloni, guidati da G. Washington, grazie anche agli interventi di Francia e Spagna. Nel 1776 gli americani stilano la Dichiarazione di Indipendenza, seguita dalla sconfitta inglese e dalla nascita del nuovo stato federale, sancito dalla pace di Parigi del 1783.

---

## 7. Who were the Mongols and how did they expand?

*chi erano i mongoli e come si espansero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 13.9 ms | 4.0 ms (3.5x) |
| **Generazione** | 467 ms | 4615 ms |
| **Totale** | 481 ms | 4619 ms |
| **Pool chunk** | 203 | 8 |
| **Keyword hit** | 33% | 100% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

In base al contesto fornito, i mongoli erano dei **nomadi** abitanti della regione situata nella **Mongolia del Nord**, organizzati in **tribù**. Poiché occupavano terre caratterizzate da steppe non adatte alle coltivazioni, si dedicavano principalmente all'**allevamento delle greggi**, alla **caccia** e alla **guerra**.

Si espansero formando un **impero** che si estendeva dalle coste del **Mar della Cina** e della **Corea** fino al **fiume Indo**, al **Golfo Persico** e al **Volga**, minacciando le popolazioni europee. L'espansione iniziò verso la fine del XII secolo con **Temugin** (1167-1227), un capo tribù che successivamente prese il nome di **Gengis Khan**. Dopo la sua morte, il suo regno fu diviso tra i suoi quattro figli, dando origine a quattro Khanati, tra cui quello del Gran Khan in Cina.

---

## 8. What was Luther's Protestant Reformation?

*che cosa fu la riforma protestante di lutero?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.2 ms | 8.9 ms (1.6x) |
| **Generazione** | 483 ms | 1579 ms |
| **Totale** | 497 ms | 1588 ms |
| **Pool chunk** | 203 | 101 |
| **Keyword hit** | 83% | 83% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

The answer is not available in the provided context.

(Note: While the context mentions "Lutero e l'esigenza della Riforma" in the table of contents of Chunk 1 and discusses Calvin in Chunk 2, it does not provide a definition or description of what the Protestant Reformation of Luther was.)

---

## 9. How was the Italian state formed during the Risorgimento?

*come si formò lo stato italiano nel risorgimento?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.1 ms | 8.3 ms (1.7x) |
| **Generazione** | 5352 ms | 5385 ms |
| **Totale** | 5366 ms | 5393 ms |
| **Pool chunk** | 203 | 94 |
| **Keyword hit** | 67% | 83% |

### Risposta StdRAG

In base al contesto fornito, la formazione dello Stato italiano nel Risorgimento è descritta come segue:

Il termine **Risorgimento** indica quel complesso di eventi, dottrine politiche e iniziative che condussero, a partire dal **1861**, al processo di unificazione dell'Italia. Questo processo aveva come fine l'indipendenza del territorio dall'occupazione straniera e l'unificazione di vari regni interni, condizione che l'Italia aveva vissuto per secoli.

Prima di questo evento, gli Stati italiani contavano circa 24 milioni di persone che, pur condividendo un'identità culturale, linguistica, religiosa e un interesse economico, vivevano sotto condizioni sociali non cambiate dal periodo della Restaurazione. Intorno al concetto di unificazione e indipendenza si coagulò un dibattito articolato tra due schieramenti principali:
*   **Il moderato (destra risorgimentale):** riteneva di poter raggiungere l'unificazione nazionale coinvolgendo gradualmente i governi monarchici, in particolare il Regno dei Savoia.
*   **Il democratico (sinistra risorgimentale):** riteneva necessario escludere lo stato (il testo si interrompe

### Risposta SLM-RAG

In base al contesto fornito, la formazione dello Stato italiano nel Risorgimento è descritta come segue:

Il processo di unificazione dell'Italia, definito Risorgimento, condusse, a partire dal 1861, all'unificazione del territorio che l'Italia aveva vissuto per secoli come una serie di regni interni sotto occupazione straniera. Questo processo fu il risultato di un "complesso di eventi, di dottrine politiche e di iniziative" che portarono all'indipendenza del territorio e all'unificazione.

Il punto culminante della formazione dello Stato avvenne nel marzo 1861 a Torino, quando si riunì il primo parlamento nazionale e Vittorio Emanuele II fu proclamato Re d'Italia.

Il processo fu sostenuto da due principali schieramenti politici che si contrapposero nel dibattito risorgimentale:
1.  **Gli Moderati (destra risorgimentale):** Ritenevano di poter raggiungere l'unificazione coinvolgendo gradualmente i governi monarchici, in particolare il Regno dei Savoia.
2.  **I Democratici (sinistra risorgimentale):** Ritenevano necessario escludere lo stato (il testo

---

## 10. What were the social consequences of the Industrial Revolution?

*quali furono le conseguenze sociali della rivoluzione industriale?*

| | StdRAG | SLM-RAG |
|---|---|---|
| **Retrieval** | 14.0 ms | 3.3 ms (4.2x) |
| **Generazione** | 462 ms | 5291 ms |
| **Totale** | 476 ms | 5295 ms |
| **Pool chunk** | 203 | 8 |
| **Keyword hit** | 50% | 83% |

### Risposta StdRAG

The answer is not available in the provided context.

### Risposta SLM-RAG

Le conseguenze sociali della Rivoluzione Industriale descritte nel contesto includono:

*   **Aumento demografico:** In Europa si verificò un profondo aumento della popolazione, favorito dalla tecnologia agricola e dai nuovi prodotti. In Inghilterra la popolazione raddoppiò nell'arco di un secolo, e anche la Francia crebbe notevolmente.
*   **Cambiamento degli spazi abitativi:** Crescerono le città e si formarono nuovi quartieri, in particolare di operai impiegati nelle fabbriche.
*   **Diffusione dell'informazione:** Nacquero i primi giornali (gazzette), sia statali che indipendenti, permettendo la diffusione di conoscenze e novità tra la borghesia e i ceti emergenti. Tuttavia, nacque anche la censura per evitare contenuti sgraditi alle autorità o alla morale.
*   **Conflitti sociali:** L'abbandono delle campagne da parte dei braccianti (spinto anche dalle enclosures) portò a salari bassi e condizioni di lavoro molto pesanti, preparando i conflitti sociali del 1800.
*   **Espulsione degli operai:** L'introduzione di nuove macchine causò l

---

