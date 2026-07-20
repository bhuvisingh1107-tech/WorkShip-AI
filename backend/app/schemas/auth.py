from app.schemas.employee import EmployeeRead as UserResponse

# Keep Token model for completeness (though not used)
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True