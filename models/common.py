from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from models.enums import RecordType, SourceSystem


class StandardModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )


class Identifier(StandardModel):
    kind: str = Field(..., description="Identifier type such as nct_id, pmid, doi.")
    value: str


class SourceReference(StandardModel):
    system: SourceSystem = SourceSystem.UNKNOWN
    record_type: RecordType
    source_id: str | None = None
    source_url: HttpUrl | None = None
    retrieved_at: datetime | None = None
    raw_payload_version: str | None = None


class Provenance(StandardModel):
    source: SourceReference
    raw_fields: dict[str, Any] = Field(
        default_factory=dict,
        description="Original field values from the upstream source, keyed by raw field name.",
    )


class Organization(StandardModel):
    name: str
    normalized_name: str | None = None
    country: str | None = None


class DateRange(StandardModel):
    start_date: date | None = None
    end_date: date | None = None


class Location(StandardModel):
    facility: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
