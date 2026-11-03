from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str


class EmployeeResponse(EmployeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)