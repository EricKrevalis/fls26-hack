from datetime import date

from pydantic import Field

from models.common import DateRange, Identifier, Location, Organization, Provenance, StandardModel
from models.enums import InterventionType, TrialPhase, TrialStatus
from models.indication import Indication


class Intervention(StandardModel):
    name: str
    type: InterventionType = InterventionType.UNKNOWN
    description: str | None = None


class TrialArm(StandardModel):
    name: str
    arm_type: str | None = None
    description: str | None = None
    interventions: list[Intervention] = Field(default_factory=list)


class EligibilityCriteria(StandardModel):
    inclusion: list[str] = Field(default_factory=list)
    exclusion: list[str] = Field(default_factory=list)
    min_age: str | None = None
    max_age: str | None = None
    sex: str | None = None


class OutcomeMeasure(StandardModel):
    name: str
    description: str | None = None
    timeframe: str | None = None
    outcome_type: str | None = None


class TrialRecord(StandardModel):
    title: str
    brief_summary: str | None = None
    identifiers: list[Identifier] = Field(default_factory=list)
    sponsor: Organization | None = None
    collaborators: list[Organization] = Field(default_factory=list)
    indications: list[Indication] = Field(default_factory=list)
    phase: TrialPhase = TrialPhase.UNKNOWN
    status: TrialStatus = TrialStatus.UNKNOWN
    study_design: str | None = None
    enrollment: int | None = None
    dates: DateRange = Field(default_factory=DateRange)
    primary_completion_date: date | None = None
    locations: list[Location] = Field(default_factory=list)
    arms: list[TrialArm] = Field(default_factory=list)
    primary_outcomes: list[OutcomeMeasure] = Field(default_factory=list)
    secondary_outcomes: list[OutcomeMeasure] = Field(default_factory=list)
    eligibility: EligibilityCriteria | None = None
    provenance: Provenance
