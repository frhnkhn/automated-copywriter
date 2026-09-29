from pydantic import BaseModel, Field, field_validator


class CopyRequest(BaseModel):
    product_name: str = Field(
        min_length=1,
        max_length=100
    )

    product_description: str = Field(
        min_length=10,
        max_length=2000
    )

    platform: str

    tone: str

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0
    )

    top_p: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0
    )

    @field_validator("platform")
    @classmethod
    def validate_platform(cls, value):
        allowed = {
            "linkedin",
            "instagram",
            "email"
        }

        value = value.lower().strip()

        if value not in allowed:
            raise ValueError(
                "Platform must be LinkedIn, Instagram, or Email."
            )

        return value

    @field_validator("tone")
    @classmethod
    def validate_tone(cls, value):
        allowed = {
            "professional",
            "friendly",
            "energetic",
            "funny",
            "persuasive"
        }

        value = value.lower().strip()

        if value not in allowed:
            raise ValueError(
                "Tone must be Professional, Friendly, Energetic, Funny, or Persuasive."
            )

        return value