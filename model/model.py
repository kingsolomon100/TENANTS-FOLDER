from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field, field_serializer 
from typing import Literal 
from datetime import datetime 


model_config = ConfigDict(
    populate_by_name=True,
    str_strip_whitespace=True
)

class Tenant(BaseModel):
    roomNumber: int = Field(ge=1)
    name: str = Field(min_length=1)
    email: EmailStr
    gender: Literal["male", "female"]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_time: datetime = Field(default_factory=datetime.now) 

    @field_validator("gender", mode='before')
    @classmethod 
    def gender_base(cls, value: str):
        if isinstance(value, str):
            return value.lower()
        return value 
    
    @field_serializer("gender")
    def gender_serializer(self, gender: str):  
        return gender.capitalize() 
    

    @field_validator("name")
    @classmethod
    def name_base(cls, value: str):
        if not value:
            raise ValueError("It must be left with blank spaces")
        return value 