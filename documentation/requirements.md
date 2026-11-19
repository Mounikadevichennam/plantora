# PLANTORA – Requirements Analysis & Module Planning

**Project Title:** PLANTORA – Intelligent Crop Health Monitoring & Smart Farming System  
**Domain:** AI & Automation  

---

## 1. Requirements Identification

### Functional Requirements
1. Users must be able to select a crop type (Rice, Tomato, Potato, or Chilli).
2. Users must be able to upload a clear image of a crop leaf.
3. The system must validate the uploaded file format (JPG/PNG) before processing.
4. The AI model must analyze the image and detect whether the crop is healthy or affected by a specific disease.
5. The system must display the predicted disease name, confidence score, and basic treatment/prevention tips.

### Non-Functional Requirements
1. **Performance:** Disease prediction results should be generated within 3–5 seconds.
2. **Usability:** The interface must be clean, simple, and mobile-friendly for easy use by farmers.
3. **Accuracy:** The AI model should provide reliable and accurate predictions based on trained datasets.
4. **Reliability:** The system should handle invalid file uploads gracefully with clear error messages.

### User Requirements
1. Farmers and agricultural users need a quick, easy-to-use tool that does not require technical expertise.
2. Results should clearly explain the detected crop issue and actionable next steps for care or treatment.

---

## 2. Feature Breakdown

| Feature Name | Purpose | Expected Input | Processing / Functionality | Expected Output |
| :--- | :--- | :--- | :--- | :--- |
| **Crop Selection & Image Upload** | Allow users to submit leaf photos for analysis. | Crop type + Leaf image (JPG/PNG) | Validates file type and size; sends image to backend. | Confirmation of valid upload ready for analysis. |
| **AI Disease Detection** | Identify crop health status using deep learning. | Preprocessed leaf image + Crop type | Runs image through the trained AI classification model. | Predicted disease name + Confidence percentage. |
| **Remedy Recommendation** | Guide users on how to treat or prevent the disease. | Predicted disease name | Matches the detected disease with a curated remedy guide. | Clear treatment and prevention instructions. |
| **Prediction History** | Let users review their past crop scans. | Scan result + Timestamp | Stores uploaded image metadata and result in storage. | List of previous scans and outcomes. |

---

## 3. Module Breakdown

1. **Frontend (User Interface Module):** Handles crop selection, image upload interface, error alerts, and displaying prediction results and remedies.
2. **Backend (API & Data Routing Module):** Receives requests from the frontend, validates and preprocesses images, communicates with the AI model, and sends back structured JSON responses.
3. **AI & Automation (Processing Module):** Houses the trained deep learning models for Rice, Tomato, Potato, and Chilli disease classification.
4. **Storage & Data Management Module:** Manages storage of uploaded images, prediction logs, and remedy reference data.

---

## 4. Development Priorities

### Must Have (Essential)
* Crop type selection (Rice, Tomato, Potato, Chilli).
* Leaf image upload and format validation.
* AI-based crop disease prediction.
* Clear display of the predicted disease result.

### Should Have (Important)
* Prediction confidence score percentage.
* Basic treatment and prevention recommendations for detected diseases.
* User-friendly error handling for invalid or blurry uploads.

### Could Have (If Time Permits)
* Online purchase links for recommended pesticides/medicines (product-specific).
* Scan history dashboard to view past predictions.
* Regional language support (e.g., Telugu, Hindi) for wider farmer accessibility.

---

## 5. Development Task List

### Module 1: Frontend (User Interface)
1. Design a clean, mobile-friendly upload page layout.
2. Implement the crop selection dropdown and image file picker.
3. Add client-side image format validation (JPG/PNG).
4. Create a result display card for disease name, confidence score, and remedies.
5. Connect the frontend form to the backend API endpoint.

### Module 2: Backend (API & Data Routing)
1. Initialize the backend server and set up API routes.
2. Implement image upload handling and preprocessing (resizing/normalization).
3. Integrate the trained AI model for inference.
4. Map predicted disease labels to treatment recommendations.
5. Return formatted JSON responses and test API error handling.

### Module 3: AI & Automation (Processing)
1. Organize and clean crop leaf datasets (Rice, Tomato, Potato, Chilli).
2. Preprocess and augment image data for model training.
3. Train and validate the deep learning classification model.
4. Evaluate model accuracy and export the final trained model file.

### Module 4: Storage & Data Management
1. Set up storage for uploaded leaf images and prediction logs.
2. Create a structured mapping/database for disease remedies.
3. Test saving and retrieving prediction records.