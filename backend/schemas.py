from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: str
    email: EmailStr
    glucose: float
    haemoglobin: float
    cholesterol: float
    remarks: str = ""

    @field_validator("date_of_birth")
    def dob_not_future(cls, v):
        from datetime import date
        for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                dob = datetime.strptime(v, fmt).date()
                if dob > date.today():
                    raise ValueError("Date of birth cannot be a future date")
                return dob.strftime("%Y-%m-%d" or "%d-%m-%Y")  
            except ValueError as e:
                if "future" in str(e):
                    raise
                continue
        raise ValueError("Date format must be YYYY-MM-DD or DD-MM-YYYY")

    @field_validator("glucose", "haemoglobin", "cholesterol")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Blood test values must be positive numbers")
        return v
    