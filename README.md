# AI-Powered Guest Experience and Personalisation System

A comprehensive FastAPI-based hospitality management platform for the hospitality industry, integrating AI/ML for sentiment analysis, personalized guest recommendations, and real-time feedback analytics.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [AI/ML Details](#aiml-details)
- [Development Workflow](#development-workflow)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This system enables hotels and hospitality providers to deliver personalized guest experiences using advanced AI and machine learning. It analyzes guest feedback, predicts sentiment, and recommends amenities, dining, and activities tailored to each guest.

---

## Architecture

- **Backend:** FastAPI RESTful API
- **Frontend:** (Optional) React/Vite or Jinja2 templates
- **AI/ML:** Python, Hugging Face Transformers, PyTorch, scikit-learn
- **Database:** (Add details if using SQLite, PostgreSQL, etc.)
- **Deployment:** Docker-ready, local development focus

---

## Features

- **Sentiment Analysis:** Real-time NLP using DistilBERT (Hugging Face Transformers) to classify guest feedback.
- **Personalized Recommendations:** ML models suggest amenities and activities based on guest profile, loyalty tier, and feedback.
- **Admin Dashboard:** Visualizes feedback trends, satisfaction scores, and system health using Pandas, Matplotlib, Seaborn.
- **Alerts:** Slack webhook integration for negative sentiment detection.
- **Dual UI:** Separate dashboards for guests and admins.
- **Extensible:** Modular codebase for easy feature addition.

---

## Tech Stack

- **Python 3.11+**
- **FastAPI** (API framework)
- **Uvicorn** (ASGI server)
- **Jinja2** (templating)
- **Pandas, scikit-learn, Matplotlib, Seaborn** (data analysis & visualization)
- **Transformers, torch** (AI/ML models)
- **Docker** (optional for containerization)

---

## Project Structure

```
app/                # FastAPI backend, routers, models, services
api/                # API endpoints (if present)
frontend/           # Frontend code (React/Vite or templates)
requirements.txt    # Python dependencies
Dockerfile          # Docker setup (optional)
venv/               # Python virtual environment (optional)
.env                # Environment variables (local only)
.gitignore          # Git ignore rules
```

---

## Setup & Installation

1. **Install Python 3.11+**

2. **Install dependencies:**
   ```sh
   pip install --user -r requirements.txt
   ```

3. **Run the server:**
   ```sh
   python -m uvicorn app.main:app --reload
   ```
   *(Adjust entry point if needed)*

4. **Access the app:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Usage

- **API Endpoints:**  
  See `app/` and `api/` for available endpoints (e.g., `/feedback`, `/recommendations`, `/admin`).
- **Swagger UI:**  
  Interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs)
- **Admin Dashboard:**  
  Visualizes analytics and feedback (see frontend or Jinja2 templates).

---

## AI/ML Details

- **Sentiment Analysis:**  
  Uses Hugging Face DistilBERT via `transformers` and `torch` for NLP classification.
- **Recommendation Engine:**  
  ML models (scikit-learn, custom logic) factor in guest history, loyalty tier, and feedback sentiment.
- **Data Pipeline:**  
  Pandas for data wrangling, Matplotlib/Seaborn for visualization.
- **Model Training:**  
  Scripts and notebooks (add details if present) for retraining and evaluation.

---

## Development Workflow

1. **Clone the repository:**
   ```sh
   git clone https://github.com/BSRohit20/AI-POWERED-GUEST-EXPERIENCE-AND-PERSONALISATION-SYSTEM.git
   cd AI-POWERED-GUEST-EXPERIENCE-AND-PERSONALISATION-SYSTEM
   ```

2. **Create a feature branch:**
   ```sh
   git checkout -b feature/my-feature
   ```

3. **Make changes and commit:**
   ```sh
   git add .
   git commit -m "Add new feature"
   ```

4. **Push and create a pull request:**
   ```sh
   git push origin feature/my-feature
   ```

---

## Contributing

- Fork the repo and clone locally.
- Create a new branch for your feature.
- Commit and push your changes.
- Open a pull request.

---

## License

MIT License

---

**For more details, see the code and comments in each
