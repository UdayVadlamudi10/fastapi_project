from fastapi import FastAPI

app = FastAPI()



patients=[
    {
        "id":1,
        "name":"Akhil",
        "disease":"fever"
    },
    {
        "id":2,
        "name":"Bharat",
        "disease":"Cough"
    },
    {
        "id":3,
        "name":"Chandu",
        "disease":"headache"
        
    }
]

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}

@app.get("/home")
def home():
    return root()

@app.get("/about")
def about():
    return {"message": "This is fast api demonstration class"}

@app.get("/contactus")
def contact():
    return {"message":"Connected with us by follwowing in linked in ........."}



# @app.get("/patients")
# def get_all_patients():
#     return patients



@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    
    for pateint in patients:
        if pateint['id']==patient_id:
            return pateint
    
    return {"message":f"Patient not available with the given patient id {patient_id}"}
    
    
    
@app.get("/patients")
def get_patients(name: str | None = None, disease:str |None=None):
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



# @app.get("/search")
# def search_patients(
#     id: int,
#     name: str | None=None,
#     disease: str|None=None
# ):
    
    