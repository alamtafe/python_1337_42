#!usr/bin/env python3
from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(
            default=None,
            max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID  nedd to  start with AC")
        if self.contact_type == ContactType.PHYSICAL:
            if not self.is_verified:
                raise ValueError(
                        "Physical contact reports"
                        "need to be verified"
                    )
        if self.contact_type == ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError(
                        "Telepathic contact requires"
                        "at least 3 witnesses"
                        )
        if self.signal_strength > 7.0:
            if not self.message_received:
                raise ValueError(
                        "Strong signals should"
                        "include received messages")
        return self


if __name__ == "__main__":
    contact = AlienContact(
                contact_id="AC_1010_001",
                contact_type="radio",
                timestamp="2027-09-10T07:12:11",
                location="Mars",
                signal_strength=7,
                duration_minutes=1000,
                witness_count=18,
                message_received="I'm gonna burn the plant"
            )
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: {contact.message_received}")
    print("======================================")
    print("Expected validation error:")
    try:
        contact = AlienContact(
                contact_id="AC_1010_001",
                contact_type="telepathic",
                timestamp="2027-09-10T07:12:11",
                location="Mars",
                signal_strength=7,
                duration_minutes=1000,
                witness_count=1,
                message_received="I'm gonna burn the plant"
            )
    except ValidationError as e:
        e = e.errors()
        for er in e:
            print(er["msg"].replace("Value error, ", ""))
