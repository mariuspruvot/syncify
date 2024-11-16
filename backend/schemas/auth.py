from pydantic import BaseModel
from pydantic import field_validator


class Login(BaseModel):
    email: str
    password: str

    @classmethod
    @field_validator("email")
    def email_must_be_valid_domain(cls, v):
        if not v.endswith((".com", ".fr", ".net")):
            raise ValueError("Domain name must end with .com, .fr or .net")
        return v
