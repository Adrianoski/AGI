"""
benchmark.py — Confronto RAG standard vs SLM-routed retrieval.

Metriche:
  - Latenza media (ms) per query
  - Dimensione del pool di ricerca (n. chunk esaminati)
  - Overlap@5 tra i due sistemi (per stimare la qualità relativa)

Uso:
    python3 benchmark.py
"""

import time
import json
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import chromadb
from router import load_registry, find_top_n_slms

# ── Config ─────────────────────────────────────────────────────────────
TOP_N_SLMS        = 3
TOP_K             = 5
RRF_K             = 60
GENERATION_MODEL  = "Qwen/Qwen3.5-4B"    # modello HuggingFace per la generazione
MAX_NEW_TOKENS    = 256
MAX_INPUT_TOKENS  = 131072                # 128K — Qwen3.5-4B nativo è 256K, niente rope scaling necessario
OUTPUT_FILE       = f"benchmark_answers_spacy_4B_3_WAYS_5PDF_{TOP_N_SLMS}_SLM_TOK_K_{TOP_K}.md"

QUERIES = [
    
    (
        "Who imported spices into Europe during the Middle Ages?",
        "Chi importava le spezie in Europa nel Medioevo?",
        ["arabi", "veneziana", "mercanti", "spezie", "oriente", "monopolio"],
        (
            "The spice trade was controlled by Arab merchants together with the "
            "Venetian republic, who held the monopoly by crossing Muslim "
            "territories. The many risks of the journey and the various changes "
            "of hands considerably raised the price of the goods."
        ),
    ),
    (
        "What territories did Charles V control?",
        "Quali territori controllava Carlo V?",
        ["carlo", "spagna", "impero", "asburgo", "fiandre", "napoli"],
        (
            "Charles V controlled a vast empire that included Spain, the "
            "Habsburg territories, Flanders, the Kingdom of Naples, and the "
            "American colonies. His reign was marked by conflicts with France, "
            "the Lutheran German princes, and the Ottoman Empire."
        ),
    ),
    (
        "What were the main causes of the French Revolution?",
        "Quali furono le principali cause della Rivoluzione Francese?",
        ["crisi", "stato", "terzo", "nobiltà", "tasse", "assemblea"],
        (
            "The main causes of the French Revolution were the economic crisis "
            "of the Ancien Régime, the fiscal injustices that burdened the third "
            "estate, the convening of the Estates General, and the growing "
            "influence of public opinion. The nobility and clergy enjoyed fiscal "
            "privileges that fuelled popular discontent."
        ),
    ),
    (
        "What were the key principles of the Enlightenment?",
        "Quali erano i principi fondamentali dell'Illuminismo?",
        ["ragione", "philosophes", "libertà", "progresso", "lume", "diritti"],
        (
            "The Enlightenment was founded on the primacy of the 'natural light' "
            "of reason as a tool for knowledge and criticism of reality. The "
            "philosophes advocated a new vision of economics and politics based "
            "on freedom, progress, and the natural rights of the individual."
        ),
    ),
    (
        "Who were the Mongols and how did they expand?",
        "Chi erano i Mongoli e come si espansero?",
        ["mongoli", "gengis", "khan", "asia", "impero", "tartari"],
        (
            "The Mongols were a people of horsemen led by Genghis Khan, who "
            "launched his offensive toward China by crossing the Great Wall, "
            "then occupied the steppes of southern Russia, conquered Samarkand "
            "and Bukhara, and attacked Persia, Georgia, and Bulgaria. They were "
            "called Tartars by Europeans. After his death the kingdom was "
            "divided among his four sons, giving rise to four Khanates."
        ),
    ),
    (
        "How was the Italian state formed during the Risorgimento?",
        "Come si formò lo Stato italiano durante il Risorgimento?",
        ["cavour", "garibaldi", "mazzini", "unità", "piemonte", "italia"],
        (
            "Italian unification was the result of the Risorgimento, led by "
            "figures such as Mazzini (founder of Young Italy), Cavour (who "
            "conducted diplomatic policy and the Second War of Independence), "
            "and Garibaldi (who led the Expedition of the Thousand). Piedmont "
            "was the fulcrum of the unification process."
        ),
    ),
    (
        "What were the social consequences of the Industrial Revolution?",
        "Quali furono le conseguenze sociali della Rivoluzione Industriale?",
        ["operai", "fabbriche", "lavoro", "proletariato", "borghesia", "sfruttamento"],
        (
            "The Industrial Revolution brought about the birth of the "
            "working-class proletariat, who worked in factories under "
            "exploitative conditions. The divide between the property-owning "
            "bourgeoisie and the working class deepened. The negative effects of "
            "industrialisation included exhausting working hours and poor "
            "sanitary conditions."
        ),
    ),
    (
        "How did the population of Europe change from the year 1000 to the 14th century?",
        "Come cambiò la popolazione europea dall'anno 1000 al XIV secolo?",
        ["popolazione", "raddoppiando", "40 milioni", "80 milioni", "carestie", "disboscare"],
        (
            "The European population grew from the year 1000 until the beginning "
            "of the fourteenth century, doubling from around 40 million to "
            "around 80 million inhabitants. This made it necessary to clear new "
            "land to increase agricultural production, although cyclical famines "
            "occurring every decade caused thousands of deaths."
        ),
    ),
    (
        "How did the plague spread from Crimea to Europe?",
        "Come si diffuse la peste dalla Crimea all'Europa?",
        ["crimea", "genovesi", "catapulte", "cadaveri", "genova", "venezia", "sicilia"],
        (
            "The first epidemic of plague broke out in a Genoese colony in "
            "Crimea besieged by the Tartars, who hurled infected corpses over "
            "the walls using catapults. Genoese citizens fleeing the siege "
            "spread the contagion by sea. Around 1347 the plague reached Genoa, "
            "Venice, and Sicily, spreading the following year to Tuscany, "
            "France, England, Spain, and Germany. By 1353 it had killed "
            "approximately one third of the European population."
        ),
    ),
    (
        "Who was Henry the Navigator and what was his contribution to exploration?",
        "Chi era Enrico il Navigatore e qual fu il suo contributo all'esplorazione?",
        ["enrico il navigatore", "sagres", "caravella", "algarve", "venti", "atlantico"],
        (
            "Henry the Navigator was the king of Portugal who founded a naval "
            "school at his residence at Cape Sagres in the Algarve. There, "
            "information was gathered on tides, winds, and the Atlantic Ocean. "
            "He promoted the replacement of the galley with the more "
            "manoeuvrable caravel and launched Portuguese explorations toward "
            "the Azores and the circumnavigation of Africa."
        ),
    ),
    (
        "What were the main features of the First Industrial Revolution?",
        "Quali furono le principali caratteristiche della Prima Rivoluzione Industriale?",
        ["rivoluzione industriale", "fabbrica", "operai", "carbone", "watt", "inghilterra"],
        (
            "The First Industrial Revolution was characterised by the "
            "introduction of new technologies such as James Watt's steam engine, "
            "the emergence of the factory as a centre of concentrated "
            "production, the massive use of coal, and the transformation of "
            "social relations with the birth of the working-class proletariat."
        ),
    ),
    (
        "What were the economic causes of the French Revolution?",
        "Quali furono le cause economiche della Rivoluzione Francese?",
        ["crisi economica", "ancien regime", "stati generali", "terzo stato", "debito"],
        (
            "The economic crisis is identified as one of the main preconditions "
            "of the French Revolution. The Ancien Régime was characterised by "
            "fiscal privileges for the nobility and clergy, while the burden of "
            "taxation fell on the third estate. The convening of the Estates "
            "General was a direct response to this financial crisis."
        ),
    ),
    (
        "What were Napoleon's main military campaigns and how did his empire end?",
        "Quali furono le principali campagne militari di Napoleone e come finì il suo impero?",
        ["campagna d'italia", "mosca", "sant'elena", "consolato", "impero", "sconfitta"],
        (
            "Napoleon led the Italian campaign, during which the Republics were "
            "established, and the Egyptian campaign, which accelerated his "
            "political rise; he then installed the Consulate and the Empire, "
            "extending his hegemony over Europe. The conquest of Moscow marked "
            "the beginning of his decline; the empire ended with his final "
            "defeat and exile to the island of Saint Helena."
        ),
    ),
    (
        "Who was Mazzini and what was the Giovine Italia?",
        "Chi era Mazzini e cos'era la Giovine Italia?",
        ["mazzini", "giovine italia", "dio e popolo", "repubblica", "indipendenza"],
        (
            "Giuseppe Mazzini was one of the leading figures of the Risorgimento "
            "and founder of Young Italy (Giovine Italia), an association that "
            "advocated the independence and unification of Italy as a free "
            "republican nation, inspired by the motto 'God and the People'."
        ),
    ),
    (
        "What was Cavour's role in the unification of Italy?",
        "Qual fu il ruolo di Cavour nell'unificazione d'Italia?",
        ["cavour", "seconda guerra", "spedizione dei mille", "piemonte", "diplomatica"],
        (
            "Count Camillo Benso di Cavour was the central political figure in "
            "the unification process. He introduced reforms in the Kingdom of "
            "Sardinia, pursued a foreign policy that led to an alliance with "
            "France, directed the Second War of Independence, and created the "
            "diplomatic conditions for Garibaldi's Expedition of the Thousand."
        ),
    ),

    
    (
        "What was the ITHACA project and what was its main contribution to information systems design?",
        "Che cos'era il progetto ITHACA e qual fu il suo contributo principale alla progettazione dei sistemi informativi?",
        ["ithaca", "reusability", "recast", "requirements", "esprit", "toolkit"],
        (
            "The ITHACA project (FP2-ESPRIT 2, 1989–1992) aimed to address the "
            "life cycle of large software projects by providing an integrated toolkit "
            "for application development. Its key contribution was demonstrating that "
            "reuse could extend beyond code to the requirements level through the "
            "RECAST tool, which captured, classified, and retrieved validated "
            "requirements from previous projects."
        ),
    ),
    (
        "What was the INFOKIT project and what design paradigm did it promote?",
        "Che cos'era il progetto INFOKIT e quale paradigma di progettazione promuoveva?",
        ["infokit", "design by reuse", "entity-relationship", "library", "cnr", "clustering"],
        (
            "The INFOKIT research line, developed within the Italian CNR national "
            "programme (1989–1994), promoted the paradigm of 'design by reuse'. It "
            "proposed building a library of Entity–Relationship schemas systematically "
            "classified using indexing and clustering techniques, from which reusable "
            "components could be extracted and adapted for new application contexts."
        ),
    ),
    (
        "What was the F3 project and what was its central goal in requirements engineering?",
        "Che cos'era il progetto F3 e qual era il suo obiettivo centrale nell'ingegneria dei requisiti?",
        ["f3", "fuzzy to formal", "requirements", "workbench", "reusable", "specifications"],
        (
            "The F3 (From Fuzzy To Formal) project (FP3-ESPRIT3, 1992–1994) aimed to "
            "transform informal, ambiguous business requirements into formal, validated "
            "system specifications. Its main achievement was a requirements engineering "
            "workbench featuring a Reusable Requirements Library — an archive of "
            "validated specifications enabling systematic reuse across projects."
        ),
    ),
    (
        "What are the main dimensions of Information Systems Engineering (ISE) research contributions according to the framework proposed in the book?",
        "Quali sono le principali dimensioni dei contributi di ricerca nell'Information Systems Engineering (ISE) secondo il framework proposto nel libro?",
        ["ise", "artefact", "representation", "method", "tool", "vision", "contribution"],
        (
            "The proposed framework for characterising ISE research contributions "
            "identifies five main dimensions: the IS artefact being addressed, the "
            "representation or model provided, the method or approach proposed, the "
            "tool that supports it, and the vision or conceptual insight offered. "
            "A contribution must explicitly identify the ISE problem addressed and "
            "its expected real-world impact."
        ),
    ),
    (
        "How does Work System Theory (WST) contribute to defining ISE research?",
        "Come contribuisce la Work System Theory (WST) alla definizione della ricerca in ISE?",
        ["work system theory", "alter", "stakeholders", "activities", "products", "ise"],
        (
            "Work System Theory (WST), developed by Steve Alter, provides a framework "
            "for characterising ISE research by structuring the field around core "
            "components: processes and activities, participants, information, technology, "
            "products/services, customers, and environment. ISE contributions must "
            "identify tools, methods, or new ways of thinking where IS practice is "
            "influenced by these components."
        ),
    ),
    (
        "What is Business Process Management (BPM) and how does it relate to workflow management systems?",
        "Che cos'è il Business Process Management (BPM) e come si relaziona ai sistemi di gestione dei workflow?",
        ["bpm", "workflow", "process engine", "tasks", "temporal", "dbms"],
        (
            "Business Process Management considers complex organisational processes "
            "requiring the coordinated execution of tasks by human or automatic agents, "
            "described as workflows. The automatic enactment of process instances is "
            "supported by process engines or workflow management systems (WFMS), which "
            "rely on database management systems where temporal aspects of workflow "
            "execution are managed explicitly."
        ),
    ),
    (
        "What are 'valid time' and 'transaction time' in the context of temporal data management?",
        "Cosa sono il 'valid time' e il 'transaction time' nel contesto della gestione dei dati temporali?",
        ["valid time", "transaction time", "temporal", "database", "timestamp", "bpm"],
        (
            "Valid time refers to when a fact is true in the real world, while "
            "transaction time refers to when a fact is recorded as true in the database "
            "system. These two temporal dimensions allow database systems to track both "
            "the historical reality of data and its storage history, enabling temporal "
            "queries essential for correct process execution and auditing."
        ),
    ),
    (
        "What are the main dimensions of data quality and why are they important for GDPR compliance?",
        "Quali sono le principali dimensioni della qualità dei dati e perché sono importanti per la conformità al GDPR?",
        ["data quality", "accuracy", "completeness", "timeliness", "gdpr", "assessment"],
        (
            "The main data quality dimensions include accuracy, completeness, consistency, "
            "and timeliness. Under the EU GDPR, data quality is a legal obligation that "
            "directly conditions the protection of data subjects' rights. Failures in "
            "data quality can result in erroneous classifications, compliance breaches "
            "across multiple regulatory dimensions, and substantial financial penalties, "
            "as illustrated by enforcement actions against organisations with inaccurate data."
        ),
    ),
    (
        "What was the MAIS project and what limitations of service-oriented architectures did it address?",
        "Che cos'era il progetto MAIS e quali limitazioni delle architetture orientate ai servizi affrontava?",
        ["mais", "multichannel", "adaptive", "qos", "service", "context"],
        (
            "The MAIS (Multichannel Adaptive Information Systems) project was an Italian "
            "and European research initiative that addressed three main limitations of "
            "early service-oriented architectures: lack of adaptivity (static workflows), "
            "limited treatment of Quality of Service (QoS), and minimal consideration "
            "of context such as device capabilities and network conditions. MAIS sought "
            "to make services context-aware, quality-sensitive, and continuously adaptable."
        ),
    ),
    (
        "What is the distinction between abstract and concrete services in the MAIS framework?",
        "Qual è la distinzione tra servizi astratti e concreti nel framework MAIS?",
        ["abstract service", "concrete service", "late binding", "qos", "provider", "mais"],
        (
            "In the MAIS framework, abstract services capture the essence of a "
            "functionality — what the service should do and which QoS characteristics "
            "it must satisfy — without committing to any specific provider or technical "
            "realization. Concrete services correspond to actual deployable Web services "
            "offered by real providers, adding endpoint locations, protocols, and concrete "
            "QoS guarantees. This separation enables late binding and dynamic substitution "
            "at runtime."
        ),
    ),
    (
        "What is Vanilla-Converter and what migration challenge does it address?",
        "Che cos'è Vanilla-Converter e quale sfida di migrazione affronta?",
        ["vanilla-converter", "camunda 7", "camunda 8", "bpmn", "migration", "zeebe"],
        (
            "Vanilla-Converter is a command-line tool that automates the transformation "
            "of BPMN process models from Camunda 7 to Camunda 8. It addresses the "
            "challenge posed by the end-of-life of Camunda 7 in 2030 and the fundamental "
            "architectural differences between the two platforms — Camunda 7 being a "
            "monolithic embedded engine while Camunda 8 is a cloud-native distributed "
            "system built on Zeebe — which make direct model reuse impossible."
        ),
    ),
    (
        "What are the two sides of environmental sustainability in Information Systems Engineering discussed in the book?",
        "Quali sono i due aspetti della sostenibilità ambientale nell'Information Systems Engineering discussi nel libro?",
        ["green is", "is for green", "sustainability", "energy", "pernici", "caise"],
        (
            "Two sides of environmental sustainability in ISE were identified at a "
            "CAiSE 2011 panel moderated by Barbara Pernici: designing information "
            "systems for sustainability (IS for green), which uses IS to support "
            "sustainability goals in other domains, and designing sustainable "
            "information systems (Green IS), which focuses on reducing the "
            "environmental footprint of IS themselves."
        ),
    ),
    (
        "What was the GAMES project and what energy savings did it demonstrate?",
        "Che cos'era il progetto GAMES e quali risparmi energetici ha dimostrato?",
        ["games", "energy", "data centre", "gpi", "qos", "adaptation"],
        (
            "The European FP7 GAMES (Green Active Management of Energy in IT Service "
            "Centres) project developed a holistic framework for modelling, monitoring, "
            "and dynamically controlling energy consumption in data centres and cloud "
            "infrastructures. It introduced Green Performance Indicators (GPIs) to "
            "measure energy efficiency across software and infrastructure layers, and "
            "demonstrated measurable energy savings typically in the range of 20–25% "
            "without degrading Quality of Service."
        ),
    ),
    (
        "What is 'personal sovereignty' in AI-mediated ecosystems and how does it differ from autonomy?",
        "Che cos'è la 'sovranità personale' negli ecosistemi mediati dall'AI e come si differenzia dall'autonomia?",
        ["personal sovereignty", "autonomy", "ai", "agency", "alignment", "cognitive"],
        (
            "Personal sovereignty (PS) is defined as the meta-capacity to define the "
            "boundaries of one's own domain of action and to resist external imposition, "
            "distinct from autonomy which is the capacity to self-govern within a given "
            "set of options. In AI-mediated ecosystems, autonomy can be preserved "
            "while sovereignty is eroded: users may still choose among options but "
            "cannot define or understand the conditions of those choices, gradually "
            "losing cognitive and epistemic independence."
        ),
    ),
    (
        "How did Barbara Pernici contribute to the field of Information Systems Engineering?",
        "Come ha contribuito Barbara Pernici al campo dell'Information Systems Engineering?",
        ["pernici", "caise", "sustainability", "mais", "workflow", "politecnico"],
        (
            "Barbara Pernici was a central figure in ISE since the 1980s, strongly "
            "contributing to its formation and evolution. She co-founded and shaped CAiSE "
            "as a leading ISE conference, led the MAIS project on multichannel adaptive "
            "information systems, pioneered research on temporal aspects of workflows, "
            "and was among the first to introduce environmental sustainability as a "
            "research dimension in ISE, proposing and moderating the landmark CAiSE "
            "2011 panel on Green IS."
        ),
    ),
    
    (
        "What is the transformer architecture and why was it a breakthrough for natural language processing?",
        "Che cos'è l'architettura transformer e perché ha rappresentato una svolta per il natural language processing?",
        ["transformer", "attention", "sequential", "dependencies", "rnn", "llm"],
        (
            "The transformer architecture, introduced with the attention mechanism, "
            "allows models to weigh the importance of different parts of an input "
            "sequence simultaneously, overcoming the limitation of RNNs in handling "
            "long-range dependencies. This breakthrough enabled the development of "
            "large language models by making it possible to understand the entire "
            "context of a sequence in parallel rather than sequentially."
        ),
    ),
    (
        "What is the difference between pre-training and fine-tuning in the context of large language models?",
        "Qual è la differenza tra pre-training e fine-tuning nel contesto dei large language models?",
        ["pre-training", "fine-tuning", "transfer learning", "task-specific", "weights", "dataset"],
        (
            "Pre-training involves training a model on large corpora to capture "
            "fundamental features shared across multiple tasks, producing a general-purpose "
            "foundation. Fine-tuning adapts the pre-trained model to a specific task "
            "using a smaller, task-specific dataset, either by freezing the feature "
            "extraction layers (feature freezing) or by updating all weights (full "
            "fine-tuning). This process is grounded in transfer learning."
        ),
    ),
    (
        "What is prompt engineering and what are the main prompting techniques?",
        "Che cos'è il prompt engineering e quali sono le principali tecniche di prompting?",
        ["prompt", "zero-shot", "few-shot", "chain-of-thought", "instructions", "llm"],
        (
            "Prompt engineering is the practice of carefully designing and refining "
            "prompts to optimise LLM responses. The main techniques are zero-shot "
            "prompting (directly asking the model without examples), few-shot prompting "
            "(providing input-output examples to guide the model), and chain-of-thought "
            "prompting (structuring the prompt to encourage the model to articulate "
            "intermediate reasoning steps for complex tasks)."
        ),
    ),
    (
        "What is Retrieval-Augmented Generation (RAG) and what problem does it solve?",
        "Che cos'è la Retrieval-Augmented Generation (RAG) e quale problema risolve?",
        ["rag", "retrieval", "knowledge", "hallucination", "vector", "generation"],
        (
            "Retrieval-Augmented Generation (RAG) combines a retrieval component with "
            "a generative LLM to ground responses in external knowledge sources. It "
            "addresses the problem of hallucinations and outdated knowledge by retrieving "
            "relevant documents from a vector store at query time and providing them as "
            "context to the LLM, enabling accurate and up-to-date responses without "
            "retraining the model."
        ),
    ),
    (
        "What are the main evaluation metrics for RAG systems?",
        "Quali sono le principali metriche di valutazione per i sistemi RAG?",
        ["contextual precision", "contextual recall", "faithfulness", "answer relevancy", "ragas", "deepeval"],
        (
            "RAG systems are evaluated on both retrieval and generation quality. "
            "Retrieval metrics include Contextual Precision, which measures whether "
            "relevant nodes are ranked higher than irrelevant ones, and Contextual "
            "Recall, which measures how well the retrieval context covers the expected "
            "output. Generation metrics include Answer Relevancy, which assesses how "
            "well the output addresses the query, and Faithfulness, which measures "
            "whether the output is factually supported by the retrieved context."
        ),
    ),
    (
        "What are LLM agents and what are their main architectural components?",
        "Che cosa sono gli LLM agent e quali sono i loro principali componenti architetturali?",
        ["agent", "memory", "planning", "tools", "short-term", "long-term"],
        (
            "LLM agents augment large language models with additional modules to handle "
            "complex, multi-step tasks that a standalone LLM cannot manage. Their three "
            "primary architectural components are memory (short-term for retaining "
            "current context and long-term for storing knowledge across sessions), "
            "planning (decomposing complex tasks into manageable sub-goals with "
            "reflection and refinement), and tools (external resources such as APIs "
            "and databases that extend the agent's capabilities)."
        ),
    ),
    (
        "What is a multi-agent LLM system and what are its main coordination mechanisms?",
        "Che cos'è un sistema multi-agent LLM e quali sono i suoi principali meccanismi di coordinazione?",
        ["multi-agent", "profiling", "communication", "cooperative", "debate", "competitive"],
        (
            "A multi-agent LLM system assigns distinct roles to multiple specialized "
            "LLM-based agents that collaborate to solve complex tasks. Its main "
            "operational framework covers four aspects: environment interface (sandbox, "
            "physical, or purely inter-agent), profiling (pre-defined, model-generated, "
            "or data-derived roles), communication (cooperative, debate-based, or "
            "competitive), and evolution (memory-based learning and self-adaptation "
            "over time)."
        ),
    ),
    (
        "What is the information systems life cycle and what are its main phases?",
        "Che cos'è il ciclo di vita dei sistemi informativi e quali sono le sue principali fasi?",
        ["life cycle", "planning", "design", "development", "testing", "monitoring"],
        (
            "The information systems life cycle is an iterative development plan "
            "structured into five main phases: planning (strategic guidelines and "
            "feasibility study), design (conceptual, process, and interaction modelling "
            "using languages such as E/R, UML, and BPMN), development (implementation "
            "through programming and database population), testing and validation (unit, "
            "system, and user acceptance tests), and monitoring and maintenance "
            "(corrective, perfective, and adaptive maintenance)."
        ),
    ),
    (
        "What is the difference between an information system and a computer system?",
        "Qual è la differenza tra un sistema informativo e un sistema informatico?",
        ["information system", "computer system", "hardware", "software", "organization", "knowledge"],
        (
            "An information system includes hardware, software, and the set of technical "
            "and organisational knowledge of a business entity within which it operates, "
            "encompassing both computerised and manual routines as well as the people "
            "involved. A computer system consists solely of hardware and software. The "
            "information system is therefore the broader concept, of which the computer "
            "system is only the technological implementation part."
        ),
    ),
    (
        "What is LSTM and what problem does it solve compared to standard RNNs?",
        "Che cos'è LSTM e quale problema risolve rispetto alle RNN standard?",
        ["lstm", "rnn", "sequential", "long-term", "forget gate", "cell state"],
        (
            "Long Short-Term Memory (LSTM) is a specific type of recurrent neural "
            "network designed to handle sequential data and capture long-term "
            "dependencies that standard RNNs fail to retain. It achieves this through "
            "gating mechanisms: the forget gate (deciding what information to discard), "
            "the input gate (deciding what new information to add), and the output gate "
            "(determining how much of the cell state contributes to the output)."
        ),
    ),
    (
        "What is Parameter-Efficient Fine-Tuning (PEFT) and what is LoRA?",
        "Che cos'è il Parameter-Efficient Fine-Tuning (PEFT) e che cos'è LoRA?",
        ["peft", "lora", "fine-tuning", "parameters", "memory", "rank"],
        (
            "Parameter-Efficient Fine-Tuning (PEFT) refers to techniques that adapt "
            "a pre-trained LLM to a specific task while updating only a small subset "
            "of parameters, drastically reducing GPU memory requirements. LoRA "
            "(Low-Rank Adaptation) is the most prominent PEFT technique: it introduces "
            "low-rank decomposition matrices into the model layers, allowing fine-tuning "
            "with approximately 33% less GPU memory compared to full fine-tuning."
        ),
    ),
    (
        "What is the ETL process and what role does it play in information and knowledge management?",
        "Che cos'è il processo ETL e quale ruolo svolge nella gestione dell'informazione e della conoscenza?",
        ["etl", "extraction", "transformation", "loading", "data warehouse", "quality"],
        (
            "ETL (Extraction, Transformation, Loading) is a process that ensures data "
            "quality and standardisation before integration into structured repositories. "
            "Extraction involves connecting systems and collecting data; transformation "
            "converts data into a standard format; loading imports the transformed data "
            "into a data warehouse. ETL supports enhanced system performance and "
            "business intelligence by making data more reliable, accurate, and easily "
            "accessible for analytical processing."
        ),
    ),
    (
        "What is COSMADS and how does it leverage LLMs for industrial data retrieval?",
        "Che cos'è COSMADS e come sfrutta gli LLM per il recupero di dati industriali?",
        ["cosmads", "pipeline", "data services", "manufacturing", "langchain", "retrieval"],
        (
            "COSMADS (COmposing SMart Data Services) is an LLM-based tool that "
            "synthesises information extraction pipelines as Python scripts from "
            "natural language queries in manufacturing environments. It uses dynamic "
            "context retrieval to fetch relevant example pipelines and data service "
            "documentation from vector stores, feeding them to an LLM agent that "
            "generates executable scripts bridging the gap between operators and "
            "siloed industrial data sources."
        ),
    ),
    (
        "What are the main ethical challenges of large language models according to the book?",
        "Quali sono le principali sfide etiche dei large language models secondo il libro?",
        ["ethics", "bias", "fairness", "transparency", "hallucination", "governance"],
        (
            "The book identifies several key ethical challenges of LLMs: bias and "
            "fairness concerns arising from training data that may encode societal "
            "prejudices, lack of transparency and interpretability due to the "
            "scarcely explainable nature of LLM behaviour, the risk of hallucinations "
            "generating incorrect or misleading outputs, and the need for human-in-the-"
            "loop governance mechanisms to ensure responsible and accountable use of "
            "these systems in information systems engineering."
        ),
    ),
    (
        "What are MetaGPT and ChatDev and how do they apply multi-agent LLM systems to software engineering?",
        "Che cosa sono MetaGPT e ChatDev e come applicano i sistemi multi-agent LLM all'ingegneria del software?",
        ["metagpt", "chatdev", "software engineering", "roles", "workflow", "agents"],
        (
            "MetaGPT is a multi-agent framework that structures software development "
            "by assigning distinct roles — product manager, architect, engineer, QA "
            "engineer — each building on the previous agent's output in a predefined "
            "sequential workflow. ChatDev models a virtual software company where "
            "agents with roles such as architects, programmers, and testers communicate "
            "through structured dialogues across four phases — designing, coding, "
            "testing, and documenting — with peer verification to reduce hallucinations "
            "in generated code."
        ),
    ),
    # ── NEUROPSICOLOGIA DELLE DEMENZE (15 nuove) ─────────────────────────────
    (
        "What is dementia and what are its two defining diagnostic criteria?",
        "Che cos'è la demenza e quali sono i due criteri diagnostici fondamentali?",
        ["demenza", "funzioni cognitive", "vita quotidiana", "deficit multipli", "progressiva", "vigilanza"],
        (
            "Dementia is a progressive chronic cognitive deterioration consisting in "
            "the progressive loss of cognitive functions of sufficient severity to "
            "compromise functional autonomy in daily life. The two fundamental "
            "diagnostic criteria are the presence of multiple cognitive deficits "
            "and their interference with daily life, in a subject with normal "
            "wakefulness conditions."
        ),
    ),
    (
        "What are the main epidemiological data on dementia worldwide?",
        "Quali sono i principali dati epidemiologici sulla demenza nel mondo?",
        ["47 milioni", "alzheimer", "50-60%", "vascolare", "prevalenza", "età"],
        (
            "Approximately 47 million people worldwide are affected by dementia, "
            "with 9.9 million new cases in 2015 alone — one new case every 3 seconds. "
            "Alzheimer's disease is the most frequent form, representing 50-60% of "
            "cases. Vascular dementia is second with 15-20% prevalence, followed by "
            "frontotemporal dementia and Lewy body dementia. Prevalence doubles "
            "every 5-6 years with increasing age."
        ),
    ),
    (
        "What is the role of the APOE gene in Alzheimer's disease risk?",
        "Qual è il ruolo del gene APOE nel rischio di sviluppare la malattia di Alzheimer?",
        ["apoe", "ε4", "amiloide", "cromosoma 19", "rischio", "allele"],
        (
            "The APOE gene, which codes for apolipoprotein E involved in removing "
            "amyloid-β, presents three allelic forms: ε2 (highest efficiency), ε3 "
            "(intermediate, most common at ~80%), and ε4 (least efficient). The ε4 "
            "allele increases AD risk proportionally to the number of alleles present: "
            "one ε4 allele raises risk approximately 3-fold, while two alleles raise "
            "it up to 15-fold compared to the most common genotype."
        ),
    ),
    (
        "What are the two stages of neuropsychological assessment in cognitive deterioration?",
        "Quali sono i due stadi della valutazione neuropsicologica nel deterioramento cognitivo?",
        ["screening", "secondo livello", "profilo cognitivo", "diagnosi", "deterioramento", "nosografica"],
        (
            "Neuropsychological assessment of cognitive deterioration follows a "
            "two-stage algorithm. The first stage is a screening evaluation aimed at "
            "identifying the presence and severity of cognitive deterioration. The "
            "second stage is an extended evaluation aimed at defining the specific "
            "cognitive profile characteristic of the type of dementia, useful for "
            "differential diagnosis, longitudinal monitoring, and treatment planning."
        ),
    ),
    (
        "What are the main limitations of the MMSE as a screening tool for dementia?",
        "Quali sono i principali limiti del MMSE come strumento di screening per le demenze?",
        ["mmse", "falsi negativi", "funzioni esecutive", "scolarità", "sensibilità", "screening"],
        (
            "The MMSE is unreliable in subjects with both low education/illiteracy "
            "(false positives) and high education (false negatives). Its test selection "
            "is unbalanced and does not specifically assess executive functions, so "
            "severe executive deficits may produce a normal score. It is also poorly "
            "sensitive to early-stage deterioration (MCI), and its most reliable use "
            "is providing a quantitative measure in advanced dementia."
        ),
    ),
    (
        "What is Mild Cognitive Impairment (MCI) and what is its clinical relevance?",
        "Che cos'è il Mild Cognitive Impairment (MCI) e qual è la sua rilevanza clinica?",
        ["mci", "amnesico", "conversione", "alzheimer", "demenza", "memoria episodica"],
        (
            "Mild Cognitive Impairment (MCI) is a condition of acquired cognitive "
            "decline demonstrated by neuropsychological tests, sufficiently mild not "
            "to significantly interfere with daily functional independence. Its main "
            "clinical relevance lies in the possibility of identifying early-stage AD "
            "patients: the annual conversion rate from MCI to AD is estimated at 5-10% "
            "in community studies and up to 20% in selected populations."
        ),
    ),
    (
        "What is the typical neuropsychological profile of Alzheimer's disease and why is the hippocampal memory deficit distinctive?",
        "Qual è il profilo neuropsicologico tipico della malattia di Alzheimer e perché il deficit di memoria ippocampale è distintivo?",
        ["alzheimer", "memoria episodica", "ippocampo", "cues semantici", "riconoscimento", "amnesia"],
        (
            "The dominant feature of Alzheimer's disease is early and disproportionate "
            "episodic memory deficit of hippocampal type: learning and recall are not "
            "facilitated by semantic cues, and recognition is also impaired, reflecting "
            "damage to medial temporal structures. This pattern, assessed with paradigms "
            "such as the Free and Cued Selective Reminding Test, distinguishes "
            "hippocampal amnesia from frontal amnesia, where cueing normalises performance."
        ),
    ),
    (
        "What are the main neuropsychological features of vascular cognitive impairment compared to Alzheimer's disease?",
        "Quali sono le principali caratteristiche neuropsicologiche del deterioramento cognitivo vascolare rispetto alla malattia di Alzheimer?",
        ["vascolare", "esecutive", "sottocorticale", "amnesia frontale", "gradini", "lacune"],
        (
            "Vascular cognitive impairment is characterised by a predominance of "
            "attentive-executive deficits over memory deficits, reflecting involvement "
            "of fronto-subcortical circuits. Unlike Alzheimer's disease, memory deficits "
            "in vascular dementia have more executive characteristics: recall improves "
            "with semantic cuing (frontal amnesia pattern). Multinfarctal dementia "
            "shows a characteristic stepwise or fluctuating progression rather than the "
            "slowly progressive course of degenerative dementias."
        ),
    ),
    (
        "What is the CADASIL disease and what cognitive profile does it produce?",
        "Che cos'è la malattia CADASIL e quale profilo cognitivo produce?",
        ["cadasil", "sostanza bianca", "cromosoma 19", "lacunari", "dominante", "piccoli vasi"],
        (
            "CADASIL (Cerebral Autosomal Dominant Arteriopathy with Subcortical Infarcts "
            "and Leukoencephalopathy) is a hereditary small vessel disease caused by a "
            "missense mutation in the NOTCH3 gene on chromosome 19. It manifests "
            "clinically with migraine with aura, mood disorders, recurrent strokes, and "
            "cognitive deterioration. The cognitive profile is characterised by executive "
            "and attentive deficits with subcortical features, and no treatment is able "
            "to modify its course."
        ),
    ),
    (
        "What are the main cognitive and behavioural features of Huntington's disease?",
        "Quali sono le principali caratteristiche cognitive e comportamentali della malattia di Huntington?",
        ["huntington", "esecutive", "procedurale", "striato", "apatia", "emozioni"],
        (
            "Huntington's disease produces a predominantly subcortical-frontal cognitive "
            "profile with severe executive deficits, psychomotor slowing, and procedural "
            "memory impairment reflecting striatal involvement. Episodic memory is "
            "affected with frontal characteristics: recall improves with semantic cuing. "
            "Among the earliest manifestations is impaired recognition of negative "
            "emotions from facial expressions. Behavioural symptoms include apathy, "
            "irritability, depression, and obsessive-compulsive disorder."
        ),
    ),
    (
        "What distinguishes Parkinson's disease dementia (PD-D) from Alzheimer's disease neuropsychologically?",
        "Cosa distingue neuropsicologicamente la demenza nella malattia di Parkinson (PD-D) dalla malattia di Alzheimer?",
        ["parkinson", "fronto-striatale", "visuo-spaziale", "ippocampale", "allucinazioni", "esecutive"],
        (
            "PD-D is characterised by more pronounced executive and visuo-spatial deficits "
            "compared to Alzheimer's disease, with relatively less severe memory impairment. "
            "Memory deficits in PD-D have frontal-striatal characteristics: recall improves "
            "with semantic cuing, unlike the hippocampal pattern of AD. Additional features "
            "include complex visual hallucinations (70% prevalence in PD-D) and apathy. "
            "The MMSE is not sensitive to fronto-striatal compromise; the MoCA is preferred."
        ),
    ),
    (
        "What are prion diseases and what are their main neuropathological characteristics?",
        "Che cosa sono le malattie da prioni e quali sono le loro principali caratteristiche neuropatologiche?",
        ["prioni", "spongiforme", "trasmissibili", "proteina", "degenerazione", "fatali"],
        (
            "Prion diseases are a group of fatal and transmissible neurodegenerative conditions "
            "caused by an unconventional infectious agent — a misfolded protein rather than a "
            "virus or bacterium. They exist in sporadic, genetic, and acquired forms. Shared "
            "neuropathological features include spongiform degeneration, astrocytic gliosis, "
            "neuronal loss, and sometimes amyloid plaques. They cause rapidly progressive "
            "dementia as both direct neuronal damage and neuroinflammation contribute."
        ),
    ),
    (
        "What are the three main variants of Primary Progressive Aphasia (PPA)?",
        "Quali sono le tre principali varianti dell'Afasia Primaria Progressiva (APP)?",
        ["afasia primaria progressiva", "non fluente", "semantica", "logopenica", "temporale", "linguaggio"],
        (
            "Primary Progressive Aphasia has three main variants. The non-fluent variant "
            "is characterised by effortful speech with agrammatism and apraxia of speech, "
            "associated with left frontal-insular atrophy. The semantic variant presents "
            "with progressive multimodal degradation of semantic knowledge and anomia, "
            "with anterior temporal lobe atrophy. The logopenic variant shows reduced "
            "speech rate with phonological errors and impaired sentence repetition, "
            "associated with left posterior peri-sylvian atrophy and Alzheimer pathology."
        ),
    ),
    (
        "What is cognitive reserve and how does it influence the clinical manifestation of dementia?",
        "Che cos'è la riserva cognitiva e come influenza la manifestazione clinica della demenza?",
        ["riserva cognitiva", "scolarizzazione", "sintomi", "compensazione", "plasticità", "diagnosi"],
        (
            "Cognitive reserve refers to the brain's ability to cope with neurological damage "
            "before symptoms become clinically manifest. It derives from education level and "
            "learning acquired throughout adult life. Patients with high cognitive reserve "
            "may remain asymptomatic longer due to greater compensatory mechanisms; however, "
            "they often receive a dementia diagnosis later and at a more advanced disease "
            "stage, potentially obtaining fewer benefits from cognitive interventions compared "
            "to patients with low cognitive reserve."
        ),
    ),
    (
        "What is legal capacity and what is its relationship with dementia according to Italian law?",
        "Che cos'è la capacità di agire e qual è il suo rapporto con la demenza secondo il diritto italiano?",
        ["capacità di agire", "demenza", "incapacità", "tutela", "civile", "procura"],
        (
            "Legal capacity is the ability to validly perform legal acts by exercising one's "
            "rights and fulfilling obligations through expressions of will. It requires the "
            "capacity to understand (cognitive functions underlying comprehension of one's "
            "actions) and to will (aspects of cognition regulating conscious choice). "
            "Dementia represents a risk factor for incapacity but does not inevitably cause "
            "it: individual capacities may be selectively impaired. The law provides "
            "protective instruments such as power of attorney, which can be granted before "
            "the person loses legal capacity."
        ),
    ),
    # ── AU CONTINENTAL AI STRATEGY (15 nuove) ────────────────────────────────
    (
        "What is the definition of Artificial Intelligence adopted in the AU Continental AI Strategy?",
        "Qual è la definizione di Intelligenza Artificiale adottata nella Strategia Continentale sull'IA dell'UA?",
        ["computer systems", "simulate", "learn", "adapt", "autonomous", "objectives"],
        (
            "Within the framework of the AU Continental AI Strategy, AI refers to "
            "computer systems that can simulate the processes of natural intelligence "
            "exhibited by humans, where machines use technologies that enable them to "
            "learn and adapt, sense and interact, predict and recommend, reason and plan, "
            "optimise procedures and parameters, operate autonomously, be creative, and "
            "extract knowledge from large amounts of data to make decisions and "
            "recommendations for the purpose of achieving objectives identified by humans."
        ),
    ),
    (
        "What are the five focus areas of the AU Continental AI Strategy?",
        "Quali sono le cinque aree di intervento della Strategia Continentale sull'IA dell'UA?",
        ["maximising", "minimising", "capabilities", "cooperation", "investment", "governance"],
        (
            "The five focus areas of the AU Continental AI Strategy are: maximising "
            "the benefits of AI for social and economic development and cultural renaissance; "
            "minimising risks and safeguarding AI development from harm to African people; "
            "building capabilities in infrastructure, datasets, computing, skills, and research; "
            "fostering regional and international cooperation; and accelerating AI investment, "
            "all framed within an inclusive governance and regulatory framework."
        ),
    ),
    (
        "What is the estimated economic potential of AI for Africa according to the strategy?",
        "Qual è il potenziale economico stimato dell'IA per l'Africa secondo la strategia?",
        ["pwc", "1.5 trillion", "gdp", "generative ai", "productivity", "110 billion"],
        (
            "PwC estimates that AI could contribute up to $1.5 trillion to the African "
            "economy, equivalent to 6% of the continent's GDP. Additionally, a McKinsey "
            "study suggests Generative AI could increase global productivity by 40% and "
            "add between $2.2 to $4.4 trillion annually to the world economy. If Africa "
            "recouped just 5% of this opportunity, Generative AI could add between $110 "
            "to $220 billion to African GDP per year."
        ),
    ),
    (
        "What are the main risks of AI identified in the Continental AI Strategy for Africa?",
        "Quali sono i principali rischi dell'IA identificati nella Strategia Continentale per l'Africa?",
        ["bias", "discrimination", "job displacement", "disinformation", "privacy", "cultural heritage"],
        (
            "The strategy identifies risks across several dimensions: environmental risks "
            "from energy consumption and e-waste; system-level risks including algorithmic "
            "bias and privacy breaches; structural risks such as gender inequality, job "
            "displacement, and the AI divide; and risks to African values including societal "
            "cohesion threats from disinformation and hate speech, undermining of democracy "
            "through AI-enabled election manipulation, and subversion of indigenous knowledge "
            "and African cultural heritage."
        ),
    ),
    (
        "What are the main inhibitors to AI uptake in Africa identified in the strategy?",
        "Quali sono i principali ostacoli all'adozione dell'IA in Africa identificati nella strategia?",
        ["internet", "computing", "data", "skills", "supercomputers", "awareness"],
        (
            "The main inhibitors to AI uptake in Africa are gaps in internet usage, lack "
            "of computing platforms, limited data availability for training AI models, and "
            "scarce AI skills. As of 2023, 100% of the world's supercomputers reside in only "
            "30 nations, and Africa lacks these critical resources. Limited awareness of AI "
            "among the workforce is identified as the biggest barrier to adoption in both "
            "public and private sectors, alongside insufficient research and development "
            "and low investment in digital technologies."
        ),
    ),
    (
        "What are the guiding principles of the AU Continental AI Strategy?",
        "Quali sono i principi guida della Strategia Continentale sull'IA dell'UA?",
        ["local first", "people-centred", "human rights", "inclusion", "ethics", "ubuntu"],
        (
            "The guiding principles are: Local First (African solutions for African challenges); "
            "People-centred (inclusive growth, well-being and cultural renaissance); Human "
            "Rights and Human Dignity (upholding the African Charter and international human "
            "rights law); Peace and Prosperity (advancing peaceful and prosperous societies); "
            "Inclusion and Diversity (non-discriminatory, leaving no one behind, respecting "
            "cultural diversity and empowering African women); Ethics and Transparency "
            "(responsible AI avoiding bias and widening inequalities); and Cooperation and "
            "Integration (regionally integrated governance approaches)."
        ),
    ),
    (
        "What multi-tiered governance approach does the strategy propose for AI regulation in Africa?",
        "Quale approccio di governance multilivello la strategia propone per la regolamentazione dell'IA in Africa?",
        ["existing laws", "regulatory gaps", "policy frameworks", "assessment tools", "research", "sandboxes"],
        (
            "The strategy proposes a multi-tiered governance approach comprising five "
            "tiers: amendment and application of existing laws and frameworks (including "
            "intellectual property, data protection, cybersecurity, and consumer protection "
            "laws); identification of regulatory gaps; establishment of enabling policy "
            "frameworks through national AI strategies; development and roll-out of AI "
            "assessment and evaluation tools; and continuous African-led research and "
            "evaluation of governance efficacy, including regulatory sandboxes for innovation."
        ),
    ),
    (
        "How does the AU Continental AI Strategy propose to expand AI adoption in agriculture?",
        "Come la Strategia Continentale sull'IA dell'UA propone di espandere l'adozione dell'IA in agricoltura?",
        ["crop yield", "soil", "weather forecasting", "pest", "centres of excellence", "geospatial"],
        (
            "The strategy proposes promoting widespread AI adoption in African agriculture "
            "through AI technologies covering crop yield, irrigation, soil content sensing, "
            "crop monitoring, planting and weeding, weather forecasting, precision agriculture, "
            "and pest, disease and weed prediction using AI combined with space observation "
            "and geospatial technologies. Key actions include designating continental centres "
            "of excellence to build knowledge bases on agricultural AI use cases, supporting "
            "member states, and raising awareness of both benefits and risks."
        ),
    ),
    (
        "What are the strategy's recommendations for AI adoption in education in Africa?",
        "Quali sono le raccomandazioni della strategia per l'adozione dell'IA nell'istruzione in Africa?",
        ["curriculum", "generative ai", "tutoring systems", "disabilities", "coding", "higher education"],
        (
            "The strategy recommends formulating inclusive national AI in education policies, "
            "integrating coding and AI into curricula from primary through higher education, "
            "and developing AI competency frameworks for both teachers and students. It "
            "promotes AI-powered Intelligent Tutoring Systems, assistive AI tools for students "
            "with disabilities, and automation of administrative tasks for teachers. It also "
            "warns against GenAI threatening teachers' rights and learners' creativity, calling "
            "for age limits and data protection requirements for GenAI platforms in education."
        ),
    ),
    (
        "What challenges does Africa face regarding AI data infrastructure according to the strategy?",
        "Quali sfide affronta l'Africa riguardo all'infrastruttura dati per l'IA secondo la strategia?",
        ["data centres", "high performance computing", "quality", "1.8%", "open data", "cloud"],
        (
            "Africa faces a significant deficit in AI data infrastructure: as of 2023 Africa "
            "accounts for only 1.8% of large-scale data centres globally despite representing "
            "15% of the world's population, with only about 10% of data centre demand "
            "currently served. There are also shortages of high-performance computing "
            "resources with advanced graphics-processing units in research institutions, "
            "limited quality and diversity of locally produced datasets, and insufficient "
            "open public sector data, making it difficult to train AI models on African contexts."
        ),
    ),
    (
        "What does the strategy recommend to address gender equality and inclusion in AI development in Africa?",
        "Cosa raccomanda la strategia per affrontare la parità di genere e l'inclusione nello sviluppo dell'IA in Africa?",
        ["women", "disabilities", "languages", "indigenous", "vulnerable", "empowerment"],
        (
            "The strategy recommends ensuring AI development and adoption benefit everyone "
            "especially women and girls, and respect Africa's cultural and linguistic diversity. "
            "It calls for developing AI capabilities in local African languages including support "
            "for low-resourced languages, creating AI innovations for vulnerable persons "
            "including those with disabilities, incentivising women-led AI innovations and "
            "entrepreneurship, tailoring AI applications for rural and remote areas, and "
            "conducting ex-ante and ex-post impact assessments to identify and address "
            "adverse impacts on underrepresented groups."
        ),
    ),
    (
        "What AI safety and security risks does the strategy identify as particularly relevant for Africa?",
        "Quali rischi per la sicurezza dell'IA la strategia identifica come particolarmente rilevanti per l'Africa?",
        ["disinformation", "deepfakes", "cyberattacks", "autonomous weapons", "democracy", "surveillance"],
        (
            "The strategy identifies three main categories of AI safety and security risks: "
            "digital sphere risks including cyberattacks, fraud, scams, impersonation, child "
            "sexual abuse images, technology-facilitated gender-based violence and illegal "
            "surveillance; risks to political systems and societies including synthetic media "
            "eroding democratic engagement and public trust in government institutions; "
            "and physical security risks as Generative AI becomes embedded in critical "
            "infrastructure and military systems, potentially escalating conflicts through "
            "incorrect threat predictions."
        ),
    ),
    (
        "What is Africa's current position in global AI development and what countries lead on the continent?",
        "Qual è la posizione attuale dell'Africa nello sviluppo globale dell'IA e quali paesi guidano nel continente?",
        ["mauritius", "south africa", "startups", "2400", "github", "oxford insights"],
        (
            "Africa has more than 2,400 organisations working on AI innovation, 41% of which "
            "are startups. Africa's share of GitHub contributors grew from 0.3% in 2010 to "
            "about 2.3% in 2020. However, the US, China, EU, UK and India still dominate "
            "global AI development. Oxford Insight's Global AI Index places African countries "
            "among 'waking up' and 'nascent' nations, with Mauritius leading regional AI "
            "readiness at a score of 53.27, followed by South Africa, Rwanda, Senegal and "
            "Benin in the 2023 index."
        ),
    ),
    (
        "What does the strategy recommend to strengthen African participation in global AI governance?",
        "Cosa raccomanda la strategia per rafforzare la partecipazione africana nella governance globale dell'IA?",
        ["G20", "UNESCO", "OECD", "diplomats", "common position", "multilateral"],
        (
            "The strategy recommends that the AU Commission coordinate and lead Africa's "
            "participation in multilateral AI governance forums, leveraging AU membership in "
            "the G20 to establish strategic AI partnerships. It calls for building the capacities "
            "of African diplomats, parliamentarians and policymakers on AI governance issues, "
            "disseminating information on major AI events to ensure African stakeholder "
            "participation, organising consultative multistakeholder workshops to build "
            "common African positions before major global events, and ensuring AU Member "
            "States bid to host global AI events."
        ),
    ),
    (
        "What is the implementation timeframe of the Continental AI Strategy and how is it structured?",
        "Qual è il calendario di attuazione della Strategia Continentale sull'IA e come è strutturato?",
        ["2025", "2030", "phase 1", "phase 2", "monitoring", "readiness index"],
        (
            "The Continental AI Strategy proposes a five-year implementation timeframe "
            "from 2025 to 2030. Phase 1 (2025–2026) focuses on creating governance "
            "frameworks, national AI strategies, resource mobilisation, and capacity building "
            "at the AU, RECs and member states. Phase 2 commences in 2028, implementing "
            "core projects based on a 2027 midterm review. Monitoring and evaluation will "
            "be supported by an African AI readiness index, a dedicated web platform "
            "dashboard, and coordination with regional AI observatories."
        ),
    ),
]
# ── Helpers ────────────────────────────────────────────────────────────

def tokenize(text: str):
    return re.sub(r'[^\w\s]', ' ', text.lower()).split()


def rrf(rankings, k=RRF_K):
    scores = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)


def cosine_scores(q_emb, embeddings):
    q_norm = float(np.linalg.norm(q_emb))
    scores = []
    for emb in embeddings:
        e = np.array(emb, dtype=np.float32)
        e_norm = float(np.linalg.norm(e))
        scores.append(float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0)
    return scores


# ── RAG standard: cerca su TUTTI i chunk di TUTTE le collection ────────

def retrieve_standard(query, q_emb, chroma_client, top_k=TOP_K):
    t0 = time.perf_counter()

    embeddings, documents = [], []
    for col_info in chroma_client.list_collections():
        col  = chroma_client.get_collection(col_info.name)
        data = col.get(include=["embeddings", "documents"])
        embeddings.extend(data["embeddings"])
        documents.extend(data["documents"])

    dense_scores = cosine_scores(q_emb, embeddings)
    dense_rank   = sorted(range(len(embeddings)), key=lambda i: dense_scores[i], reverse=True)

    bm25       = BM25Okapi([tokenize(d) for d in documents])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(embeddings)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [documents[i] for i in fused], len(embeddings), elapsed


# ── SLM-routed retrieval ───────────────────────────────────────────────

def retrieve_slm(query, q_emb, registry, chroma_client, top_k=TOP_K):
    t0 = time.perf_counter()

    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    all_chunks = []
    for slm_name, _ in top_slms:
        entry = registry[slm_name]
        chunks_path = Path(entry["chunks_json"])
        if not chunks_path.exists():
            continue
        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        col = chroma_client.get_collection(entry["collection"])
        data = col.get(ids=chunk_ids, include=["embeddings", "documents", "metadatas"])
        for i, emb in enumerate(data["embeddings"]):
            e = np.array(emb, dtype=np.float32)
            e_norm = float(np.linalg.norm(e))
            q_norm = float(np.linalg.norm(q_emb))
            ds = float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0
            all_chunks.append({"text": data["documents"][i], "score": ds})

    if not all_chunks:
        return [], 0, (time.perf_counter() - t0) * 1000

    dense_rank = sorted(range(len(all_chunks)), key=lambda i: all_chunks[i]["score"], reverse=True)
    bm25       = BM25Okapi([tokenize(c["text"]) for c in all_chunks])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(all_chunks)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused   = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [all_chunks[i]["text"] for i in fused], len(all_chunks), elapsed


# ── SLM-Full: routing + tutti i chunk del cluster (no retrieval interno) ──

def retrieve_slm_full(q_emb, registry, chroma_client):
    """Solo routing semantico: passa al LLM TUTTI i chunk dei top-N SLM,
    senza ulteriore filtraggio dense/BM25 intra-cluster."""
    t0 = time.perf_counter()

    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    docs = []
    for slm_name, _ in top_slms:
        entry = registry[slm_name]
        chunks_path = Path(entry["chunks_json"])
        if not chunks_path.exists():
            continue
        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        col = chroma_client.get_collection(entry["collection"])
        data = col.get(ids=chunk_ids, include=["documents"])
        docs.extend(data["documents"])

    elapsed = (time.perf_counter() - t0) * 1000
    return docs, len(docs), elapsed


# ── Generation ────────────────────────────────────────────────────────

_gen_tok = None
_gen_mdl = None

def _load_gen_model(model_name: str):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    global _gen_tok, _gen_mdl
    if _gen_tok is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype  = torch.int8 if device == "cuda" else torch.float32
        print(f"  Carico {model_name} su {device} (max_input_tokens={MAX_INPUT_TOKENS})...")
        _gen_tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        _gen_tok.model_max_length = MAX_INPUT_TOKENS
        _gen_mdl = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, trust_remote_code=True
        ).to(device).eval()


def generate(query: str, docs: list, model_name: str) -> str:
    import torch
    from SLMAgent import build_messages, _apply_chat_template_no_think
    _load_gen_model(model_name)
    device = next(_gen_mdl.parameters()).device
    # apply_chat_template with enable_thinking=False prevents <think> tokens at the source.
    text = _apply_chat_template_no_think(_gen_tok, build_messages(query, docs))
    inputs = _gen_tok(text, return_tensors="pt", truncation=True, max_length=MAX_INPUT_TOKENS).to(device)
    with torch.no_grad():
        out = _gen_mdl.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=_gen_tok.eos_token_id,
        )
    return _gen_tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Carico modelli...")
    emb_model    = SentenceTransformer("BAAI/bge-m3")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    registry     = load_registry()

    all_cols     = chroma_client.list_collections()
    total_chunks = sum(chroma_client.get_collection(c.name).count() for c in all_cols)
    col_names    = [c.name for c in all_cols]

    print(f"Collections: {col_names}  |  chunk totali: {total_chunks}  |  SLM: {len(registry)}")
    print(f"Query: {len(QUERIES)}  |  top-k={TOP_K}  |  top-N SLM={TOP_N_SLMS}  |  model={GENERATION_MODEL}\n")

    def hit_rate(docs, keywords):
        joined = " ".join(docs).lower()
        hits = sum(1 for kw in keywords if kw in joined)
        return hits / len(keywords) * 100 if keywords else 0.0

    std_times, slm_times, full_times = [], [], []
    std_pools, slm_pools, full_pools = [], [], []
    std_gens,  slm_gens,  full_gens  = [], [], []
    overlaps, std_hits, slm_hits, full_hits = [], [], [], []
    md_rows = []

    for idx, (query_en, query_it, expected_kws, ground_truth) in enumerate(QUERIES, 1):
        print(f"\n[{idx}/{len(QUERIES)}] {query_en}")

        # Retrieval con la query IT: BM25 lavora nella stessa lingua dei documenti
        # (confronto fair tra StdRAG e SLM-RAG sull'aspetto retrieval).
        # La generazione riceve query_it ma il system prompt forza l'output in inglese,
        # così evaluate_quality.py può usare query_en + mpnet senza language mismatch.
        q_emb = emb_model.encode(
            [query_it], normalize_embeddings=True, convert_to_numpy=True
        )[0].astype(np.float32)

        docs_std,  pool_std,  t_std  = retrieve_standard(query_it, q_emb, chroma_client)
        docs_slm,  pool_slm,  t_slm  = retrieve_slm(query_it, q_emb, registry, chroma_client)
        docs_full, pool_full, t_full = retrieve_slm_full(q_emb, registry, chroma_client)

        overlap = len(set(docs_std[:TOP_K]) & set(docs_slm[:TOP_K])) / TOP_K * 100
        hr_std  = hit_rate(docs_std,  expected_kws)
        hr_slm  = hit_rate(docs_slm,  expected_kws)
        hr_full = hit_rate(docs_full, expected_kws)

        std_times.append(t_std);   slm_times.append(t_slm);   full_times.append(t_full)
        std_pools.append(pool_std); slm_pools.append(pool_slm); full_pools.append(pool_full)
        overlaps.append(overlap)
        std_hits.append(hr_std);   slm_hits.append(hr_slm);   full_hits.append(hr_full)

        speedup = t_std / t_slm if t_slm > 0 else float("inf")

        print(f"  Retrieval  —  StdRAG: {t_std:.1f}ms (pool={pool_std})  |  "
              f"SLM-RAG: {t_slm:.1f}ms (pool={pool_slm})  |  "
              f"SLM-Full: {t_full:.1f}ms (pool={pool_full})  speedup={speedup:.1f}x")
        # Generazione: query EN per forzare risposte in inglese (Qwen 4B segue la lingua
        # della domanda; il system prompt da solo non basta su modelli piccoli).
        print(f"  Generazione StdRAG...")
        t_gen0 = time.perf_counter()
        ans_std = generate(query_en, docs_std, GENERATION_MODEL)
        t_gen_std = (time.perf_counter() - t_gen0) * 1000

        print(f"  Generazione SLM-RAG...")
        t_gen0 = time.perf_counter()
        ans_slm = generate(query_en, docs_slm, GENERATION_MODEL)
        t_gen_slm = (time.perf_counter() - t_gen0) * 1000

        print(f"  Generazione SLM-Full...")
        t_gen0 = time.perf_counter()
        ans_full = generate(query_en, docs_full, GENERATION_MODEL)
        t_gen_full = (time.perf_counter() - t_gen0) * 1000

        std_gens.append(t_gen_std); slm_gens.append(t_gen_slm); full_gens.append(t_gen_full)

        print(f"  Gen times  —  StdRAG: {t_gen_std:.0f}ms  |  SLM-RAG: {t_gen_slm:.0f}ms  |  SLM-Full: {t_gen_full:.0f}ms")
        print(f"  StdRAG  : {ans_std[:100]}…")
        print(f"  SLM-RAG : {ans_slm[:100]}…")
        print(f"  SLM-Full: {ans_full[:100]}…")

        md_rows.append({
            "query_en":     query_en,
            "query_it":     query_it,
            "ground_truth": ground_truth,
            "ans_std":      ans_std,
            "ans_slm":      ans_slm,
            "ans_full":     ans_full,
            "docs_std":     docs_std,
            "docs_slm":     docs_slm,
            "docs_full":    docs_full,
            "t_ret_std":    t_std,
            "t_ret_slm":    t_slm,
            "t_ret_full":   t_full,
            "t_gen_std":    t_gen_std,
            "t_gen_slm":    t_gen_slm,
            "t_gen_full":   t_gen_full,
            "speedup":      speedup,
            "pool_std":     pool_std,
            "pool_slm":     pool_slm,
            "pool_full":    pool_full,
            "hr_std":       hr_std,
            "hr_slm":       hr_slm,
            "hr_full":      hr_full,
            "overlap":      overlap,
        })

    # ── Salva Markdown ─────────────────────────────────────────────────
    avg_speedup        = np.mean(std_times) / np.mean(slm_times)
    avg_speedup_full   = np.mean(std_times) / np.mean(full_times) if np.mean(full_times) > 0 else 0.0
    pool_reduction     = (1 - np.mean(slm_pools)  / np.mean(std_pools)) * 100
    pool_reduction_full= (1 - np.mean(full_pools) / np.mean(std_pools)) * 100

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Benchmark RAG — {', '.join(col_names)}\n\n")
        f.write(f"**Modello:** {GENERATION_MODEL}  |  **top-k:** {TOP_K}  |  **top-N SLM:** {TOP_N_SLMS}\n\n")
        f.write(f"| Metrica | StdRAG | SLM-RAG | SLM-Full |\n|---|---|---|---|\n")
        f.write(f"| Speedup retrieval | — | **{avg_speedup:.1f}x** | **{avg_speedup_full:.1f}x** |\n")
        f.write(f"| Pool medio | {int(np.mean(std_pools))} chunk "
                f"| {int(np.mean(slm_pools))} chunk (-{pool_reduction:.0f}%) "
                f"| {int(np.mean(full_pools))} chunk ({pool_reduction_full:+.0f}%) |\n")
        f.write(f"| Generazione media | {np.mean(std_gens):.0f} ms | {np.mean(slm_gens):.0f} ms | {np.mean(full_gens):.0f} ms |\n")
        f.write(f"| Keyword hit | {np.mean(std_hits):.0f}% | **{np.mean(slm_hits):.0f}%** | {np.mean(full_hits):.0f}% |\n")
        f.write(f"| Overlap medio top-{TOP_K} (Std vs SLM) | {np.mean(overlaps):.0f}% | — | — |\n\n")
        f.write("---\n\n")

        for i, r in enumerate(md_rows, 1):
            f.write(f"## {i}. {r['query_en']}\n\n")
            f.write(f"*{r['query_it']}*\n\n")
            f.write(f"| | StdRAG | SLM-RAG | SLM-Full |\n|---|---|---|---|\n")
            f.write(f"| **Retrieval** | {r['t_ret_std']:.1f} ms | {r['t_ret_slm']:.1f} ms ({r['speedup']:.1f}x) | {r['t_ret_full']:.1f} ms |\n")
            f.write(f"| **Generazione** | {r['t_gen_std']:.0f} ms | {r['t_gen_slm']:.0f} ms | {r['t_gen_full']:.0f} ms |\n")
            f.write(f"| **Totale** | {r['t_ret_std']+r['t_gen_std']:.0f} ms "
                    f"| {r['t_ret_slm']+r['t_gen_slm']:.0f} ms "
                    f"| {r['t_ret_full']+r['t_gen_full']:.0f} ms |\n")
            f.write(f"| **Pool chunk** | {r['pool_std']} | {r['pool_slm']} | {r['pool_full']} |\n")
            f.write(f"| **Keyword hit** | {r['hr_std']:.0f}% | {r['hr_slm']:.0f}% | {r['hr_full']:.0f}% |\n\n")
            f.write(f"### Risposta StdRAG\n\n{r['ans_std']}\n\n")
            f.write(f"### Risposta SLM-RAG\n\n{r['ans_slm']}\n\n")
            f.write(f"### Risposta SLM-Full\n\n{r['ans_full']}\n\n")
            f.write(f"### Ground Truth\n\n{r['ground_truth']}\n\n")
            f.write("---\n\n")

    print(f"\nFile salvato: {OUTPUT_FILE}")

    # ── Salva JSON per evaluate_quality.py ────────────────────────────
    json_path = OUTPUT_FILE.replace(".md", f"_results.json")
    json_data = {
        "metadata": {
            "collections": col_names,
            "model":      GENERATION_MODEL,
            "top_k":      TOP_K,
            "top_n_slm":  TOP_N_SLMS,
        },
        "results": [
            {
                "query_en":     r["query_en"],
                "query_it":     r["query_it"],
                "ground_truth": r["ground_truth"],
                "std": {
                    "chunks":          r["docs_std"],
                    "answer":          r["ans_std"],
                    "t_ret_ms":        r["t_ret_std"],
                    "t_gen_ms":        r["t_gen_std"],
                    "pool":            r["pool_std"],
                    "keyword_hit_pct": r["hr_std"],
                },
                "full": {
                    "chunks":          r["docs_full"],
                    "answer":          r["ans_full"],
                    "t_ret_ms":        r["t_ret_full"],
                    "t_gen_ms":        r["t_gen_full"],
                    "pool":            r["pool_full"],
                    "keyword_hit_pct": r["hr_full"],
                },
                "overlap_pct": r["overlap"],
                "speedup":     r["speedup"],
            }
            for r in md_rows
        ],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"JSON salvato:  {json_path}")
    print(f"\nRIEPILOGO")
    print(f"  Speedup retrieval SLM-RAG  : {avg_speedup:.1f}x")
    print(f"  Speedup retrieval SLM-Full : {avg_speedup_full:.1f}x")
    print(f"  Pool medio  StdRAG  : {int(np.mean(std_pools))} chunk")
    
    print(f"  Pool medio  SLM-Full: {int(np.mean(full_pools))} chunk  ({pool_reduction_full:+.0f}%)")
    print(f"  Generazione StdRAG  : {np.mean(std_gens):.0f} ms")
    
    print(f"  Generazione SLM-Full: {np.mean(full_gens):.0f} ms")
    print(f"  Overlap medio top-{TOP_K}  : {np.mean(overlaps):.0f}%")
    print(f"  Keyword hit StdRAG  : {np.mean(std_hits):.0f}%")
    
    print(f"  Keyword hit SLM-Full: {np.mean(full_hits):.0f}%")


if __name__ == "__main__":
    main()
