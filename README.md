**MIRA — Medical Intelligence Robotic Automation**

A health prediction web application that collects patient blood test data and uses Gemini AI to generate intelligent health risk assessments, with an automatic fallback to a trained Machine Learning model when the API is unavailable.


**Tech Stack**

Backend: Python, FastAPI
Frontend: React.js (Vite) 
Database: SQLite 
AI Integration: Google Gemini 1.5 Flash API
ML Fallback: Scikit-learn (trained on diabetes dataset) 
HTTP Client: HTTPX (async) 


**Features**

-> Full CRUD: Create, Read, Update, Delete patient records

-> AI-Powered Predictions: Gemini API analyses blood test values and returns a health risk summary

-> ML Fallback: If Gemini API quota is exceeded or unavailable, a trained sklearn model automatically generates the prediction

-> Input Validation: Email format, future date check, numeric blood values enforced on both frontend and backend

-> Persistent Storage: SQLite database stores all patient records

-> Clean UI: Responsive React frontend with form and data table


**Patient Fields**

-> Full Name
-> Date of Birth
-> Email Address
-> Glucose (mg/dL)
-> Haemoglobin (g/dL)
-> Cholesterol (mg/dL)
-> Remarks (AI or ML generated)


**Project Structure**

mira-health-app/
├── backend/
│   ├── main.py              # FastAPI routes
│   ├── ai_service.py        # Gemini API + ML fallback logic
│   ├── crud.py              # Database operations
│   ├── schemas.py           # Pydantic validation models
│   ├── database.py          # sql.connector setup
│   ├── train_model.py       # ML model training script
│   ├── health_model.pkl     # Trained sklearn model
│   ├── dataset/
│   │   └── diabetes.csv     # Training dataset
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── PatientForm.jsx
│   │       └── PatientTable.jsx
│   └── package.json
├── .gitignore
└── README.md


**Setup Instructions**

Prerequisites:
-> Python 3.10+
-> Node.js 18+
-> A free Gemini API key from [aistudio.google.com](https://aistudio.google.com)


**Backend Setup**

```bash
cd backend
python -m venv venv
venv\Scripts\activate       #Windows

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder:
GEMINI_API_KEY=your_gemini_api_key_here

Start the backend server:

```bash
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`


**Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`


**API Endpoints**

GET: `/patients` - Get all patient records 
POST: `/patients` - Add new patient + generate AI prediction 
PUT: `/patients/{id}` - Update patient + regenerate prediction 
DELETE: `/patients/{id}` - Delete a patient record 


**AI Integration Logic**

1. User submits blood test values
2. Call Gemini 1.5 Flash API
3. Success? → Display Gemini prediction in Remarks
4. API Error / Quota Exceeded?
5. Automatically use trained ML model → Display ML prediction in Remarks

The ML model was trained on the Pima Indians Diabetes dataset using scikit-learn. It predicts diabetes risk probability based on glucose, BMI estimate, and other derived features.


**Environment Variables**

Create `backend/.env` with the following:
GEMINI_API_KEY=your_api_key_here

-> This file is excluded from version control via `.gitignore`. Never commit your API key.


**How to Run**

Open two terminals:

**Terminal 1 — Backend:**

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.


