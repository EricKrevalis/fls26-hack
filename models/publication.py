from datetime import date

from pydantic import Field, HttpUrl

from models.common import Identifier, Organization, Provenance, StandardModel


class PublicationAuthor(StandardModel):
    full_name: str
    affiliation: Organization | None = None


class PublicationRecord(StandardModel):
    title: str
    abstract: str | None = None
    journal: str | None = None
    publication_date: date | None = None
    identifiers: list[Identifier] = Field(default_factory=list)
    linked_trial_ids: list[str] = Field(default_factory=list)
    authors: list[PublicationAuthor] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    outcome_summary: str | None = None
    url: HttpUrl | None = None
    provenance: Provenance
