# 🤖 TalentAnalytics AI: Backend LLM Pipeline

A high-performance Python backend service designed to automate the extraction and analysis of candidate data. This project implements a full **analysis pipeline**, transforming unstructured resume text into structured, actionable insights using **Large Language Models (LLMs)**.

## 🚀 Key Features

* **Structured LLM Output**: Utilizes **Pydantic** schemas with **Gemini 2.5 Pro** to ensure 100% machine-readable JSON responses.
* **Asynchronous Pipeline**: Executes a non-blocking workflow: Request -> Unique ID Generation -> LLM Processing -> **MongoDB Atlas** Persistence.
* **RESTful Interface**: Fully documented API endpoints for initiating analysis and retrieving historical reports.
* **Cloud Native**: Containerized with **Docker** for consistent environment parity across local and production stages.

## 🛠️ Technical Stack

* **Language**: Python 3.10+
* **Framework**: FastAPI (Web API)
* **AI/ML**: Google Gemini 1.5 Pro (Generative AI)
* **Database**: MongoDB Atlas (NoSQL)
* **DevOps**: Docker, Docker Compose, GitHub Actions
* **Validation**: Pydantic v2

## 🏗️ System Architecture

The system follows a modern service-oriented design:

1. **Client Layer**: Sends raw resume and job description text via POST request.
2. **Logic Layer**: `llm_analyzer.py` handles prompt engineering and Gemini API orchestration.
3. **Persistence Layer**: `db_utils.py` manages asynchronous connections to the cloud database.
4. **Reporting Layer**: GET endpoints allow for fetching data by unique Analysis IDs.

## 📥 Getting Started

### Prerequisites

* Docker & Docker Compose
* Google AI (Gemini) API Key
* MongoDB Atlas Connection String

### Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/resume-analysis-service.git
cd resume-analysis-service

```


2. **Configure Environment:**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_key_here
MONGO_URL=your_atlas_url_here
MONGO_DB_NAME=resume_db

```


3. **Run with Docker:**
```bash
docker-compose up --build

```


4. **Access Documentation:**
Open `http://localhost:8000/docs` to view the interactive Swagger UI.

## 📊 API Documentation

| Endpoint | Method | Description |
| --- | --- | --- |
| `/analyze` | POST | Submits data to the LLM pipeline and saves results. |
| `/status/{id}` | GET | Retrieves analysis results and metadata from MongoDB. |

---

