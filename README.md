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
**PLANTORA** is an AI-powered crop disease detection and remedy recommendation web application designed to help farmers identify crop diseases from leaf images, track scan history, and manage treatment status using a relational SQLite database.

## 🛠️ Technologies & Tools Used
- **Backend:** Python 3.13, Flask
- **Database:** SQLite (`plantora.db`) with Relational Schema & Full CRUD
- **Image Validation:** Pillow (PIL)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Version Control:** Git & GitHub

## 🗄️ Database Schema (`plantora.db`)
1. **`crops` Table:** `id` (PK), `name` (UNIQUE), `disease`, `confidence`, `remedy`, `buy_link`
2. **`scans` Table:** `id` (PK), `crop_id` (FK -> `crops.id`), `crop`, `filename`, `disease`, `confidence`, `status` (`Pending`/`Treated`), `timestamp`

## ✅ Completed Features (Up to Day 9)
- RESTful Flask Backend with Pillow leaf-image validation.
- Relational SQLite database (`crops` & `scans` tables) with Foreign Key mapping.
- Full **CRUD Operations**:
  - **Create:** `POST /predict` (logs new scans)
  - **Read:** `GET /history` & `GET /db-tables` (fetches scans & table data)
  - **Update:** `PUT /history/<id>` (marks scan status as `Treated`)
  - **Delete:** `DELETE /history/<id>` (removes scan record)
- Interactive Frontend UI with live Scan History table and instant Treated/Delete actions.

## 🚀 How to Run Locally
1. Install dependencies: `pip install flask pillow`
2. Start server: `python backend/app.py`
3. Open `http://127.0.0.1:5000/` in your browser.