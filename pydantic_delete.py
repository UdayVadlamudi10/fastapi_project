
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI(
    title="Patient Management API",
    description="CRUD operations using FastAPI, Pydantic and JSON storage.",
    version="1.0.0"
)

FILE_PATH = "patients.json"


# --------------------------------
# Pydantic models
# --------------------------------

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


class PatientPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="New patient name (optional)"
    )

    disease: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="New patient disease (optional)"
    )


# --------------------------------
# JSON file operations
# --------------------------------

def load_patients():
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_patients(patients):
    with open(FILE_PATH, "w") as file:
        json.dump(patients, file, indent=4)


# --------------------------------
# General GET endpoints
# --------------------------------

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


# --------------------------------
# GET: Patient by ID
# --------------------------------

@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: int = Path(..., ge=1)
):
    patients = load_patients()

    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# --------------------------------
# GET: Search patients
# --------------------------------

@app.get("/patients")
def get_patients(
    name: str | None = Query(default=None),
    disease: str | None = Query(default=None)
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


# --------------------------------
# POST: Create a patient
# --------------------------------

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


# --------------------------------
# PUT: Replace editable patient data
# --------------------------------

@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: int = Path(..., ge=1),
    updated_data: PatientCreate = ...
):
    patients = load_patients()

    for patient in patients:
        if patient["id"] == patient_id:
            patient["name"] = updated_data.name
            patient["disease"] = updated_data.disease

            save_patients(patients)

            return {
                "message": "Patient updated successfully",
                "patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# --------------------------------
# PATCH: Update selected fields
# --------------------------------

@app.patch(
    "/patients/{patient_id}",
    summary="Partially update a patient",
    description="Updates only the patient fields supplied in the request."
)
def patch_patient(
    patient_id: int = Path(..., ge=1),
    updated_data: PatientPatch = ...
):
    patients = load_patients()

    for patient in patients:
        if patient["id"] == patient_id:

            # Get only the fields explicitly provided by the client
            update_fields = updated_data.model_dump(
                exclude_unset=True
            )

            if not update_fields:
                raise HTTPException(
                    status_code=400,
                    detail="Provide at least one field to update"
                )

            # Apply the provided changes
            patient.update(update_fields)

            # Persist the changes
            save_patients(patients)

            return {
                "message": "Patient partially updated successfully",
                "patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )



## Delete End point

@app.delete(
    "/patients/{patient_id}",
    summary="Delete a patient",
    description="Deletes a patient using their ID."
)
def delete_patient(
    patient_id: int = Path(..., ge=1)
):
    patients = load_patients()

    for patient in patients:
        if patient["id"] == patient_id:
            patients.remove(patient)
            save_patients(patients)

            return {
                "message": "Patient deleted successfully",
                "deleted_patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
