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
**PLANTORA** is an AI-powered crop disease detection and remedy recommendation web application designed to help farmers quickly identify crop diseases from leaf images and get actionable treatment advice along with direct online medicine purchase links.

## 🛠️ Technologies & Tools Used
- **Backend:** Python 3.13, Flask
- **Image Validation:** Pillow (PIL)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Version Control:** Git & GitHub
- **IDE:** Visual Studio Code

## 📂 Current Project Structure
```text
plantora/
├── backend/
│   └── app.py          # Flask API, Pillow leaf validation & remedy routing
├── frontend/
│   └── index.html      # Interactive UI for crop selection & image upload
└── README.md           # Project documentation & weekly progress