 ResearchMind

ResearchMind is a multi-agent AI research assistant that automates the process of researching a topic end-to-end — searching the web, reading and synthesizing sources, writing a structured report, and critiquing its own output for quality — all orchestrated through a LangGraph agent workflow.

Live demo:https://researchmind-nyssx2en9ciayg55rpxs6y.streamlit.app/
Repo:[github.com/MK8909/researchmind](https://github.com/MK8909/researchmind)

---

## ✨ Overview

Researching any topic thoroughly usually means juggling search, reading, note-taking, and writing yourself. ResearchMind automates this pipeline with a team of cooperating AI agents, each responsible for one stage of the research process, coordinated through a stateful graph rather than a single monolithic prompt.

Give it a topic → get back a well-structured, fact-checked research report.

---

## 🧠 Multi-Agent Architecture

ResearchMind uses **LangGraph** to orchestrate four specialized agents in a coordinated pipeline:

| Agent | Role |
|---|---|
| 🔎 **Search Agent** | Queries the web for relevant, up-to-date sources on the given topic |
| 📖 **Reader Agent** | Extracts and summarizes key information from the retrieved sources |
| ✍️ **Writer Agent** | Synthesizes findings into a coherent, structured research report |
| 🧐 **Critic Agent** | Reviews the draft for gaps, inconsistencies, or weak reasoning, and sends it back for revision if needed |

This creates a **feedback loop** (Writer ↔ Critic) rather than a single-pass generation, resulting in noticeably higher-quality output than a single LLM call.

```
User Query
    │
    ▼
┌─────────────┐
│ Search Agent │──► gathers sources
└─────────────┘
    │
    ▼
┌─────────────┐
│ Reader Agent │──► extracts & summarizes
└─────────────┘
    │
    ▼
┌─────────────┐
│ Writer Agent │──► drafts report
└─────────────┘
    │
    ▼
┌─────────────┐      revise
│ Critic Agent │───────────┐
└─────────────┘            │
    │ approved              │
    ▼                       │
Final Report  ◄──────────────┘
```

---

## 🛠️ Tech Stack

- **[LangChain](https://www.langchain.com/)** — LLM orchestration and tool integration
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** — stateful multi-agent workflow graph
- **[Groq](https://groq.com/)** — low-latency LLM inference
- **[Streamlit](https://streamlit.io/)** — interactive web UI
- **Python 3.10+**

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A [Groq API key](https://console.groq.com/keys)

### Installation

```bash
# Clone the repo
git clone https://github.com/MK8909/researchmind.git
cd researchmind

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Never commit your `.env` file or expose API keys in code. Add `.env` to `.gitignore`.

### Run locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 💡 Usage

1. Enter a research topic or question in the input box.
2. Watch the agents work through the pipeline in real time (search → read → write → critique).
3. Get a final, polished research report you can copy, export, or refine further.

---

## 📁 Project Structure

```
researchmind/
├── app.py                 # Streamlit entry point
├── agents/
│   ├── search_agent.py
│   ├── reader_agent.py
│   ├── writer_agent.py
│   └── critic_agent.py
├── graph/
│   └── workflow.py         # LangGraph state machine definition
├── requirements.txt
├── .env.example
└── README.md
```
*(Update to match your actual file layout)*

---

## 🧩 Key Challenges Solved

- Designing agent state passing and control flow using LangGraph
- Handling Groq free-tier rate limits gracefully with retries/backoff
- Fixing Streamlit dark-theme CSS rendering issues
- Managing environment/dependency conflicts between conda and venv

---

## 🔮 Future Improvements

- [ ] Add citation tracking with source links in the final report
- [ ] Support PDF/DOCX export of generated reports
- [ ] Add memory across sessions for iterative research
- [ ] Swap in additional LLM providers as fallback options

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙋 Author

Built by **[mk](https://github.com/MK8909)** — final-year B.Tech CS student, VIT Chennai.
