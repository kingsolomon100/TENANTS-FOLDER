from bson import ObjectId 
from pydantic import BaseModel, field_validator, field_serializer, Field 
from datetime import datetime 
from typing import Optional, Literal 
from model.model import Tenant 
from conversion.conversion import convert_tenant, convert_tenants 
from app_confiq.app_confiq import tenants 
from fastapi import APIRouter, HTTPException, status 

router = APIRouter(prefix="/tenants", tags=["Tenant"])

class TenantUpdate(BaseModel):
    roomNumber: Optional[int] = Field(None, ge= 1)
    name: Optional[str] = Field(None, min_length=1)
    gender: Literal["male", "female"] = None

    @field_validator('gender', mode='before')
    @classmethod 
    def gender_base(cls, v: Optional[str])->Optional[str]: 
        if isinstance(v, str):
            return v.strip().lower()
        return v 
    
    @field_serializer('gender')
    def genedr(self, gender: str):
        return gender.capitalize()
    
    @field_validator('name', mode='before')
    @classmethod 
    def name_base(cls, v: Optional[str])->Optional[str]:
        if isinstance(v, str):
            return v.strip().capitalize()
        return v 
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(tenant: Tenant):
    tenant_dict = tenant.model_dump()

    existing_room = tenants.find_one({"roomNumber":  tenant_dict['roomNumber']})
    if existing_room:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="The room is already occupied ")

    tenants.insert_one(tenant_dict)
    return {"Message": f"The room-number {tenant['roomNumber']} is assigned to a Tenant"}

@router.get("/all", status_code=status.HTTP_200_OK )    
def display_all_tenants():
    db_result = list(tenants.find())
    if not db_result:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="No Tenant is recorded")
    
    return {
        "Message": len(db_result),
        "Data": convert_tenants(db_result)
    }
        
@router.get("/{room_number}", status_code= status.HTTP_200_OK)
def get_room(room_number: int):
    raw_data = tenants.find_one({"roomNumber":  room_number})
    if not raw_data:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="The room is empty")
    
    return {
        "Data": convert_tenant(raw_data)
    }

@router.put("/{tenant_id}", status_code= status.HTTP_200_OK)
def update_data(tenant_id: str, update_tenant: TenantUpdate):
    if not ObjectId.is_valid(tenant_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Databse Invalid❌")
    
    target_id = ObjectId(tenant_id)
    existing_tenant = tenants.find_one({"_id":  target_id})
    if not existing_tenant:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="ID is not found")
    
    field_update = update_tenant.model_dump(exclude_unset=True)

    if not field_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed updaing, due to ID")
    
    tenants.update_one({"_id":  target_id}, {"$set":  field_update})

    current_time = datetime.now()
    field_update['updated_time'] = current_time 

    response_data = field_update.copy()
    response_data['updated_time'] = response_data["updated_time"].strftime("%d-%b-%Y, %I:%M%p")

    return {
        "Message": f"Updated👍 {response_data}"
    }


@router.delete("/{room_number}", status_code= status.HTTP_200_OK)
def datedlete(room_number: int):
    delete_data = tenants.find_one({"roomNumber": room_number})
    if not delete_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is missing")
    
    tenants.delete_one(delete_data)
    return {"Message": f"{delete_data['roomNumber']} has been deleted from the database"}
            
         