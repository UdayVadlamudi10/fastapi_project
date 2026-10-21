
from fastapi import FastAPI, Path, Query, Body, HTTPException
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
        ge=1,
        example=2
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
        max_length=50,
        description="Filter patients by exact name",
        example="Akhil"
    ),
    disease: str | None = Query(
        default=None,
        min_length=2,
        max_length=50,
        description="Filter patients by exact disease",
        example="fever"
    )
):
    patients = load_patients()

    if name is None and disease is None:
        return patients

    results = []

    for patient in patients:
        name_matches = (
            name is None or patient["name"] == name
        )
        disease_matches = (
            disease is None or patient["disease"] == disease
        )

        if name_matches and disease_matches:
            results.append(patient)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No matching patients found"
        )

    return results


# -------------------------------
# POST: Create patient using Pydantic
# -------------------------------

@app.post(
    "/patients",
    status_code=201,
    summary="Create a patient",
    description="Creates a patient after validating the request body."
)
def create_patient(patient: PatientCreate):
    patients = load_patients()

    # Generate the next ID automatically
    new_id = max(
        (p["id"] for p in patients),
        default=0
    ) + 1

    # Convert the validated Pydantic model to a dictionary
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
