from enum import Enum


class StrEnum(str, Enum):
    """String-backed enum for stable serialized values."""


class SourceSystem(StrEnum):
    CLINICALTRIALS_GOV = "clinicaltrials_gov"
    PUBMED = "pubmed"
    INTERNAL_CSV = "internal_csv"
    INTERNAL_API = "internal_api"
    MANUAL = "manual"
    UNKNOWN = "unknown"


class RecordType(StrEnum):
    TRIAL = "trial"
    PUBLICATION = "publication"
    INDICATION = "indication"
    SPONSOR = "sponsor"


class TrialPhase(StrEnum):
    EARLY_PHASE_1 = "early_phase_1"
    PHASE_1 = "phase_1"
    PHASE_1_2 = "phase_1_2"
    PHASE_2 = "phase_2"
    PHASE_2_3 = "phase_2_3"
    PHASE_3 = "phase_3"
    PHASE_4 = "phase_4"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"


class TrialStatus(StrEnum):
    NOT_YET_RECRUITING = "not_yet_recruiting"
    RECRUITING = "recruiting"
    ACTIVE_NOT_RECRUITING = "active_not_recruiting"
    ENROLLING_BY_INVITATION = "enrolling_by_invitation"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"
    UNKNOWN = "unknown"


class InterventionType(StrEnum):
    DRUG = "drug"
    BIOLOGICAL = "biological"
    DEVICE = "device"
    PROCEDURE = "procedure"
    BEHAVIORAL = "behavioral"
    DIAGNOSTIC_TEST = "diagnostic_test"
    RADIATION = "radiation"
    OTHER = "other"
    UNKNOWN = "unknown"


class QueryCategoryValue(StrEnum):
    TRIAL_DESIGN = "trial_design"
    COMPETITOR_COMPARISON = "competitor_comparison"
    MARKET_PUBLICATION = "market_publication"
    INDICATION_ANALYSIS = "indication_analysis"
