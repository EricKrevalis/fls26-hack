from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field


class TrialSearchFilters(BaseModel):
    indication: Optional[str] = Field(default=None, description="Disease or condition")
    phase: list[str] = Field(default_factory=list, description="Trial phases")
    geography: list[str] = Field(default_factory=list, description="Countries or regions")
    sponsor: Optional[str] = Field(default=None, description="Sponsor name")
    min_sample_size: Optional[int] = Field(default=None, ge=0)
    max_sample_size: Optional[int] = Field(default=None, ge=0)
    date_from: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    date_to: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    status: list[str] = Field(default_factory=list)
    study_terms: list[str] = Field(default_factory=list)


class NormalizedRecord(BaseModel):
    source: Literal["clinicaltrials_gov", "pubmed"]
    record_type: Literal["trial", "publication"]
    source_id: str

    title: Optional[str] = None
    official_title: Optional[str] = None

    indication: list[str] = Field(default_factory=list)
    intervention_names: list[str] = Field(default_factory=list)
    phase: list[str] = Field(default_factory=list)

    sponsor: Optional[str] = None
    status: Optional[str] = None
    geography: list[str] = Field(default_factory=list)
    sample_size: Optional[int] = None

    start_date: Optional[str] = None
    primary_completion_date: Optional[str] = None
    completion_date: Optional[str] = None
    publication_date: Optional[str] = None

    url: Optional[str] = None
    abstract: Optional[str] = None
    linked_trial_ids: list[str] = Field(default_factory=list)

    source_confidence: Literal["high", "medium", "low"] = "high"
    missing_fields: list[str] = Field(default_factory=list)


class TrialSearchResponse(BaseModel):
    query: TrialSearchFilters
    total_results: int
    results: list[NormalizedRecord]