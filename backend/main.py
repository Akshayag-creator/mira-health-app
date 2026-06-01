from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import crud, schemas
from ai_service import get_health_prediction

app = FastAPI(title="MIRA Health API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/patients")
def list_patients():
    return crud.get_all_patients()

@app.post("/patients")
async def add_patient(patient: schemas.PatientCreate):
    prediction = await get_health_prediction(
        patient.glucose, patient.haemoglobin, patient.cholesterol
    )
    data = patient.dict()
    data["remarks"] = prediction
    return crud.create_patient(data)

@app.put("/patients/{patient_id}")
async def edit_patient(patient_id: int, patient: schemas.PatientCreate):
    prediction = await get_health_prediction(
        patient.glucose, patient.haemoglobin, patient.cholesterol
    )
    data = patient.dict()
    data["remarks"] = prediction
    updated = crud.update_patient(patient_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

@app.delete("/patients/{patient_id}")
def remove_patient(patient_id: int):
    success = crud.delete_patient(patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

