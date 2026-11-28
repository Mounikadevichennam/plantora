# PLANTORA
# PLANTORA – Functional Testing & Debugging Report (Day 12)

**Project:** PLANTORA – Intelligent Crop Health Monitoring & Smart Farming System  
**Intern:** Mounika Devi Chennam  
**Domain:** AI & Automation  

---

## 1. Executed Test Cases

| Test Case ID | Feature / Module | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Frontend Validation | Submit form without selecting an image | Crop: `Rice`, Image: `None` | Display red client-side validation error without calling API | Displayed `Validation Error: Please select a leaf image before analyzing.` | Pass |
| **TC-02** | Leaf Image Validation | Upload a non-leaf image (random photo/screenshot) | Crop: `Tomato`, Image: Non-leaf PNG/JPG | Backend rejects image and returns HTTP `400` error | Red error box displayed: `Invalid image! Please upload a clear plant leaf photo.` | Pass |
| **TC-03** | End-to-End Scan (`POST /predict`) | Upload a valid crop leaf image | Crop: `Tomato`, Image: Valid leaf JPG | Disable button, show loading state, save to SQLite, display result & refresh history | Result displayed with Estimated Possibility & Disclaimer; new row added to Scan History | Pass |
| **TC-04** | Update Status (`PUT /history/<id>`) | Mark a pending scan as `Treated` | Click `Treated` button on latest scan row | Update status to `Treated` in SQLite and reflect in UI | Status updated to green `Treated` badge immediately | Pass |
| **TC-05** | Delete Record (`DELETE /history/<id>`) | Delete an existing scan record | Click `Delete` button on a scan row | Remove record from SQLite and refresh Scan History table | Record deleted and table refreshed without page reload | Pass |
| **TC-06** | API Error Handling (`404`) | Request an invalid/non-existent API route | `GET /wrong-url` | Return structured JSON `404` error instead of raw HTML | Returned clean JSON error with HTTP `404` status | Pass |

---

## 2. Bugs Identified & Resolved

1. **Duplicate Database Records on Rapid Clicks:**
   * *Issue:* Clicking the "Analyze Crop" button multiple times quickly while a request was in progress inserted duplicate scan rows into SQLite.
   * *Fix:* Disabled the submit button (`analyzeBtn.disabled = true`) and added a visible loading indicator during API execution, re-enabling it in the `finally` block.
   * *Retest:* Verified single record insertion per submission.

2. **Raw HTML Error Pages on Invalid API Routes:**
   * *Issue:* Requesting an undefined endpoint returned default HTML error pages instead of JSON.
   * *Fix:* Implemented global `@app.errorhandler(404)` and `@app.errorhandler(405)` handlers returning standardized JSON error responses.
   * *Retest:* Verified clean JSON responses for invalid routes.

---

## 3. Pending Issues / Planned Enhancements
* **Static Crop Remedy Mapping:** Currently, predictions map to stored crop remedies in SQLite. Integrating a fine-tuned MobileNetV2 disease detection model, ChromaDB RAG with verified agricultural documents, and the Gemini API for 5-language explanations is planned for the upcoming development stages.
* **Direct Camera Capture:** Currently supports gallery file upload; direct camera capture will be added in the next UI upgrade.