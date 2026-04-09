from pydantic import Field

from models.common import Identifier, StandardModel


class Indication(StandardModel):
    name: str
    normalized_name: str | None = None
    therapeutic_area: str | None = None
    biomarkers: list[str] = Field(default_factory=list)
    synonyms: list[str] = Field(default_factory=list)
    ontology_ids: list[Identifier] = Field(default_factory=list)
