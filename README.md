# PLANTORA
# plantora
## Project Status

Development environment setup completed.
Git and GitHub integration successful.

## Project Modules

1. **Frontend (User Interface):** Handles user interactions, allowing users to upload crop images (rice, tomato, potato, chilli) and view the disease detection results clearly.
2. **Backend (API & Data Routing):** Acts as the bridge between the frontend and the AI model. It receives uploaded images, sends them for processing, and returns the results to the user.
3. **AI & Automation (Processing):** The core module containing the deep learning model trained on crop datasets. It analyzes the uploaded images to predict and identify crop diseases.
4. **Storage & Data Management:** Responsible for securely saving user-uploaded images, prediction logs, and system data.

## Requirements & Module Planning
Detailed functional requirements, non-functional requirements, feature breakdown, development priorities, and module-wise task planning are documented in [requirements.md](documentation/requirements.md).

# 🌿 PLANTORA – Intelligent Crop Health Monitoring & Smart Farming System

## 📌 Project Overview
**PLANTORA** is an AI-powered crop disease detection and remedy recommendation web application with a Python/Flask RESTful backend, Pillow leaf-image validation, and a relational SQLite database.

## 🛠️ Technologies & Tools Used
- **Backend:** Python 3.13, Flask (REST API)
- **Database:** SQLite (`plantora.db`) with Relational Schema & Full CRUD
- **Image Validation:** Pillow (PIL)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **API Testing:** cURL & Browser DevTools
- **Version Control:** Git & GitHub

## 📂 Backend & Project Structure
```text
plantora/
├── backend/
│   ├── app.py          # Flask REST API, CRUD routes, Pillow validation & error handlers
│   └── plantora.db     # SQLite relational database (crops & scans tables)
├── frontend/
│   └── index.html      # Interactive UI connected to Flask APIs
└── README.md           # Project & API documentation
```

## 🔌 Implemented API Endpoints (Day 10)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the PLANTORA frontend web interface |
| `GET` | `/status` | Backend health check & SQLite database connectivity status |
| `GET` | `/api/crops` | Fetches all supported crops and remedies from the `crops` table |
| `POST` | `/predict` | Validates leaf image, predicts disease, and inserts scan into `scans` table |
| `GET` | `/history` | Retrieves the 10 most recent scan records from the database |
| `PUT` | `/history/<id>` | Updates a scan record's status to `Treated` |
| `DELETE` | `/history/<id>` | Deletes a specific scan record from the database |
| `GET` | `/db-tables` | Returns structured JSON of both `crops` and `scans` tables |

*Global JSON error handlers (`404 Not Found` and `405 Method Not Allowed`) are implemented for invalid API requests.*

## 🚀 How to Run Locally
1. Install dependencies: `pip install flask pillow`
2. Start server: `python backend/app.py`
3. Open `http://127.0.0.1:5000/` in your browser.