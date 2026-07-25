#!/usr/bin/env python3
from pydantic import model_validator, BaseModel, ValidationError, Field
from enum import Enum
from datetime import datetime


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=1000.0)

    @model_validator(mode="after")
    def validator(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        validate_rank = False
        for member in self.crew:
            if (
                    member.rank == Rank.COMMANDER
                    or member.rank == Rank.CAPTAIN
            ):
                validate_rank = True
            if not member.is_active:
                raise ValueError("All crew must be active")
        if not validate_rank:
            raise ValueError(
                    "Mission must have at least "
                    "one Commander or Captain")
        size_member = len(self.crew)
        validate_exp = size_member / 2
        validate_count = 0
        if self.duration_days > 365:
            for member in self.crew:
                if member.years_experience >= 5:
                    validate_count += 1
            if validate_count < validate_exp:
                raise ValueError(
                        "Long missions (> 365 days) "
                        "need 50% experienced crew (5+ years)")
        return self


if __name__ == "__main__":
    space = SpaceMission(
            mission_id="M0192",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2030-08-11T12:30:12",
            duration_days=400,
            crew=[
                CrewMember(
                    member_id="AS1332",
                    name="Jhon Wick",
                    rank="commander",
                    age=20,
                    specialization="Mission Command",
                    years_experience=6,
                    ),
                CrewMember(
                    member_id="AS1432",
                    name="Alice Johnson",
                    rank="officer",
                    age=25,
                    specialization="Engineering",
                    years_experience=9,
                    ),
                CrewMember(
                    member_id="AS1102",
                    name="arah Connor",
                    rank="lieutenant",
                    age=29,
                    specialization="Navigation",
                    years_experience=2,
                    ),
                ],
            budget_millions=500
            )
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {space.mission_name}")
    print(f"ID: {space.mission_id}")
    print(f"Destination: {space.destination}")
    print(f"Duration: {space.duration_days} days")
    print(f"Budget: ${space.budget_millions}M")
    print(f"Crew size: {len(space.crew)}")
    print("Crew members:")
    for member in space.crew:
        print(
                f" {member.name} ({member.rank.value}) - "
                f"{member.specialization}")
    print("=========================================")
    print("Expected validation error:")
    try:
        space = SpaceMission(
            mission_id="M0192",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2030-08-11T12:30:12",
            duration_days=400,
            crew=[
                CrewMember(
                    member_id="AS1332",
                    name="Jhon Wick",
                    rank="cadet",
                    age=20,
                    specialization="Mission Command",
                    years_experience=6,
                    ),
                CrewMember(
                    member_id="AS1432",
                    name="Alice Johnson",
                    rank="officer",
                    age=25,
                    specialization="Engineering",
                    years_experience=9,
                    ),
                CrewMember(
                    member_id="AS1102",
                    name="arah Connor",
                    rank="lieutenant",
                    age=29,
                    specialization="Navigation",
                    years_experience=2,
                    ),
                ],
            budget_millions=500
            )
    except ValidationError as e:
        e = e.errors()
        for er in e:
            print(er["msg"].replace("Value error, ", ""))
