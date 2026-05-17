from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}
