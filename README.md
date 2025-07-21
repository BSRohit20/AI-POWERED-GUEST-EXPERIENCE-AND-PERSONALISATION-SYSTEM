# AI-Driven Guest Experience Personalization System for Hospitality

This project is a full-stack hospitality management system leveraging AI and ML for guest experience personalization, feedback analytics, and smart recommendations. It is designed for modern software development best practices, with modular code, clear separation of concerns, and extensible architecture.

## Full Functionality Overview

### AI & ML Features

- **Sentiment Analysis**: Uses Hugging Face DistilBERT to analyze guest feedback in real time, flagging negative sentiment and powering analytics.
- **Personalized Recommendations**: ML-driven engine tailors dining, amenities, and activities for each guest, factoring in loyalty tier, preferences, and feedback sentiment.
- **Recommendation Upgrades**: Gold-tier guests receive premium offers; negative feedback triggers comfort-focused suggestions.
- **Data-Driven Analytics**: Admin dashboard visualizes feedback trends, guest satisfaction, and system health using Pandas, Matplotlib, Seaborn, and Plotly.
- **CRM Integration**: Reads and writes guest and feedback data from JSON files, simulating a CRM backend.

### Software Architecture

- **Backend**: FastAPI, modular service and API layers, async endpoints, JWT authentication, password hashing, and Slack alert integration.
- **Frontend**: Jinja2 templates, modern HTML/CSS/JS, responsive dashboards for guests and admins.
- **Data Storage**: JSON files for users, feedback, and guest profiles; easy to swap for a real database.
- **Testing**: Includes test scripts for feedback, alerts, analytics, and recommendations.

### Key Functionalities

- **Guest Dashboard**: Personalized recommendations, feedback submission, profile management.
- **Admin Dashboard**: View analytics, manage alerts, review feedback, add guests, and system settings.
- **Real-Time Alerts**: Slack notifications for negative feedback, admin alert dashboard for urgent issues.
- **Role-Based Access**: Secure login for guests and admins, JWT-based session management.
- **Feedback Analytics**: Sentiment breakdown, rating trends, and actionable insights for management.
- **Recommendation Engine**: Considers loyalty tier, preferences, and recent feedback to suggest upgrades, comfort options, and trending amenities.
- **Extensible Design**: Easily add new recommendation categories, ML models, or external integrations.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Jinja2 Templates, HTML/CSS/JavaScript
- **AI/ML**: Hugging Face Transformers (DistilBERT)
- **Database**: JSON files (mock CRM data)
- **Alerts**: Slack Webhooks
- **Authentication**: Python-JOSE with JWT tokens
- **Password Hashing**: Passlib with bcrypt
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Web Server**: Uvicorn (ASGI server)
- **HTTP Client**: Requests
- **Environment Management**: Python-dotenv
- **File Operations**: Aiofiles
- **Real-time Communication**: WebSockets

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BSRohit20/Infosys-Project.git
   cd Infosys-Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements-minimal.txt
   ```

5. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Configure necessary variables for your local setup

6. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 10000
   ```

7. **Access the application**
   - Open your browser to [http://localhost:10000](http://localhost:10000)
   - Use the admin interface to create guest accounts and manage the system

## Users

- **Admin**: View analytics, alerts, and system management
- **Guest**: Receive personalized recommendations and submit feedback

## API Endpoints

- `/` - Guest dashboard
- `/admin` - Admin dashboard
- `/api/feedback` - Feedback submission and analysis
- `/api/recommendations` - Personalized recommendations
- `/api/analytics` - System analytics

## Environment Variables

```
SLACK_WEBHOOK_URL=your_slack_webhook_url
HF_API_TOKEN=your_hugging_face_token
SECRET_KEY=your_secret_key
```
