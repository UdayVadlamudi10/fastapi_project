
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI(
    title="Patient Management API",
    description="A simple FastAPI application using Pydantic and JSON storage.",
    version="1.0.0"
)

FILE_PATH = "patients.json"


# -------------------------------
# Pydantic model
# -------------------------------

class PatientCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Patient's name"
    )

    disease: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Patient's disease"
    )


# -------------------------------
# JSON file functions
# -------------------------------

def load_patients():
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_patients(patients):
    with open(FILE_PATH, "w") as file:
        json.dump(patients, file, indent=4)


# -------------------------------
# General endpoints
# -------------------------------

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}


@app.get("/home")
def home():
    return root()


@app.get("/about")
def about():
    return {
        "message": "This is fast api demonstration class"
    }


@app.get("/contactus")
def contact():
    return {
        "message": "Connected with us by following on LinkedIn."
    }


# -------------------------------
# GET: Patient by ID
# -------------------------------

@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: int = Path(
        ...,
        title="Patient ID",
        description="The unique ID assigned to the patient.",
        ge=1
    )
):
    patients = load_patients()

    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# -------------------------------
# GET: Search patients
# -------------------------------

@app.get("/patients")
def get_patients(
    name: str | None = Query(
        default=None,
        min_length=2,
        max_length=50
    ),
    disease: str | None = Query(
        default=None,
        min_length=2,
        max_length=50
    )
):
    patients = load_patients()

    results = [
        patient for patient in patients
        if (name is None or patient["name"] == name)
        and (disease is None or patient["disease"] == disease)
    ]

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No matching patients found"
        )

    return results


# -------------------------------
# POST: Create a patient
# -------------------------------

@app.post("/patients", status_code=201)
def create_patient(patient: PatientCreate):
    patients = load_patients()

    new_id = max(
        (p["id"] for p in patients),
        default=0
    ) + 1

    new_patient = {
        "id": new_id,
        **patient.model_dump()
    }

    patients.append(new_patient)
    save_patients(patients)

    return {
        "message": "Patient created successfully",
        "patient": new_patient
    }


# -------------------------------
# PUT: Update a patient
# -------------------------------

@app.put(
    "/patients/{patient_id}",
    summary="Update a patient",
    description="Updates an existing patient's name and disease."
)
def update_patient(
    patient_id: int = Path(
        ...,
        ge=1,
        description="ID of the patient to update"
    ),
    updated_data: PatientCreate = ...
):
    patients = load_patients()

    for patient in patients:
        if patient["id"] == patient_id:

            # Update the existing patient's fields
            patient["name"] = updated_data.name
            patient["disease"] = updated_data.disease

            # Save the updated list to the JSON file
            save_patients(patients)

            return {
                "message": "Patient updated successfully",
                "patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} not found"
    )
