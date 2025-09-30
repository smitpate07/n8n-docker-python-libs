# 📊 From File → Charts → Telegram 🚀  
**Automated Exploratory Data Analysis (EDA) Pipeline with Python + n8n + Telegram**

Turn raw data files into **insightful charts + summaries** delivered directly to your **Telegram bot** — all in seconds.  

---

## 🎥 Demo  
Check out the workflow in action:  
👉 [Watch the demo video](#) <!-- replace # with actual video link -->

---

## ⚡ Workflow Overview  

1. **Upload a file (CSV)** via Telegram  
2. **n8n workflow** triggers a Python EDA script  
3. **Python (Pandas, NumPy, Seaborn, Matplotlib)** generates:  
   - 📈 Clean charts (PNG)  
   - 📝 JSON summary (insights, correlations, missing values)  
4. **n8n Code node** prepares binary + text payload  
5. **Telegram bot** receives:  
   - Chart as an image  
   - Human-readable text summary  

---
📂 Project Structure

.
├── n_test.py               # Python script for EDA
├── Dockerfile              # Docker File to copy local script to Docker Desktop 
├── docker-compose          # File to build Docker Image 
├── requirements.txt        # Python dependencies
├── assets/
│   └── workflow.png        # Workflow diagram (README preview)   
└── README.md

## 🖼️ Workflow Diagram  

![Workflow](./assets/workflow.png)  

---

## 🛠️ Tech Stack  

- **[Python](https://www.python.org/)** → Data wrangling + visualization  
  - Pandas · NumPy · Seaborn · Matplotlib  
- **[n8n](https://n8n.io/)** → Workflow automation engine  
- **[Telegram Bot API](https://core.telegram.org/bots/api)** → File input + message delivery  
- **Docker** → To customize the n8n image    

---

