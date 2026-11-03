from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeResponse


# Create FastAPI application
app = FastAPI(title="Employee Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database table
Base.metadata.create_all(bind=engine)

# 1. ADD EMPLOYEE (POST)
@app.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# 2. VIEW ALL EMPLOYEES (GET)
@app.get("/employees/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    return employees


# 3. VIEW SINGLE EMPLOYEE (GET)
@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# 4. UPDATE EMPLOYEE (PUT)
@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    updated_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.name = updated_data.name
    employee.email = updated_data.email
    employee.department = updated_data.department

    db.commit()
    db.refresh(employee)

    return employee


# 5. DELETE EMPLOYEE (DELETE)
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}