from fastapi import FastAPI,Path,Query,Body
import json

app = FastAPI()


FILE_PATH = "patients.json"


def load_patients():
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_patients(patients):
    with open(FILE_PATH, "w") as file:
        json.dump(patients, file, indent=4)
        
#Load patients 
patients=load_patients()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}

@app.get("/home")
def home():
    return root()

@app.get(
    "/about",
    summary="About the application",
    description="Returns information about this FastAPI demonstration application.",
    response_description="Information about the application"
)
def about():
    return {"message": "This is fast api demonstration class"}

@app.get("/contactus")
def contact():
    return {"message":"Connected with us by follwowing in linked in ........."}



# @app.get("/patients")
# def get_all_patients():
#     return patients





@app.get(
    "/patients/{patient_id}",
    summary="Get a patient by ID",
    description="Finds and returns a patient using their unique patient ID."
)
def get_patient(
    patient_id: int = Path(
        ...,
        title="Patient ID",
        description="The unique ID assigned to the patient.",
        ge=1,
        example=2
    )
):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    return {
        "message": f"Patient not available with the given patient id {patient_id}"
    }    
    
@app.get(
    "/patients",
    summary="Search patients",
    description="Returns patient records filtered by name, disease, or both."
)
def get_patients(
    name: str | None = Query(
        default=None,
        title="Patient name",
        description="Filter patients by their exact name.",
        min_length=2,
        max_length=50,
        example="Akhil"
    ),
    disease: str | None = Query(
        default=None,
        title="Disease",
        description="Filter patients by their disease.",
        min_length=2,
        max_length=50,
        example="fever"
    )
):
    if name and not disease:
        for pateint in patients:
                if pateint['name']==name:
                    return pateint
        return {"message":"Requested name is not available"}
    
    if disease and not name:
            for pateint in patients:
                    if pateint['disease']==disease:
                        return pateint
            return {"message":"Requested disease is not available"}
        
    
    if name and disease:
        for pateint in patients:
            if pateint['disease']==disease and pateint["name"]==name:
                return pateint
        return {"message":"No patient is there with given disease and name"} 
           
    return patients


########################### POST LOGIC ###################################################

@app.post("/patients")
def create_patient(patient: dict = Body(...)):
    patients.append(patient)
    save_patients(patients)
    

    return {
        "message": "Patient created successfully",
        "patient": patient
    }


# @app.get("/search")
# def search_patients(
#     id: int,
#     name: str | None=None,
#     disease: str|None=None
# ):
    
    