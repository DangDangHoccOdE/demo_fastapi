from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'