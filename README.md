# 🤖 AI Agents with ADK

This project demonstrates how to build and run AI Agents using the **Agent Development Kit (ADK)**, integrated with Google's Gemini models.

---

## 📦 Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Tsaihemanth150/ai-agents-with-adk.git
   cd ai-agents-with-adk
   ```

2. **(Optional) Create a Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   .\venv\Scripts\activate      # Windows
   ```

3. **Install Requirements**  
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configure Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey  
2. Generate a new API key.  
3. Create a `.env` file in the root of the project and add:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

---

## 🚀 Running the Project

1. **Start ADK Web (if using Genkit ADK)**  
   ```bash
   npx genkit dev
   ```
   > Make sure you have Genkit installed:  
   > `npm install -g @genkit-ai/cli`

2. **Run the Agent Code**  
   ```bash
   python src/agent_main.py
   ```
   Replace `agent_main.py` with your actual entry‑point file if different.

---

## 🌐 Project Structure

```
ai-agents-with-adk/
│
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── src/                  # Agent logic
│   └── agent_main.py     # Main script
├── prompts/              # Prompt templates (if used)
├── README.md             # This file
└── ...
```

---

## 🧠 Features

- Modular Agent Architecture  
- Gemini‑powered AI responses  
- ADK web for managing and testing agents  

---

## 🛠️ Troubleshooting

- Double‑check that your `.env` file exists and contains the correct `GEMINI_API_KEY`.  
- If you see module import errors, ensure you activated the virtual environment.  
- Use `--force` with pip install if needed:
  ```bash
  pip install --force-reinstall -r requirements.txt
  ```

---

## 📄 License

MIT — free to use, modify, and distribute.

---

## 🙌 Author

Built by [@Tsaihemanth150](https://github.com/Tsaihemanth150)
