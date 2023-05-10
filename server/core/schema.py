from pydantic import BaseModel


class SoundMessage(BaseModel):
    wavBuffer: object | None = None
    transcript: str | None = None
    voice_base: str | None = None

    class Config:
        orm_mode = True
