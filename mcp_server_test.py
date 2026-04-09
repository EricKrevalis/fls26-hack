from mcp.server.fastmcp import FastMCP

from research-paper.models import TrialSearchFilters, TrialSearchResponse
from research-paper.trial_service import TrialSearchService

mcp = FastMCP("Clinical Trial Research Server")
service = TrialSearchService()


@mcp.tool()
def search_clinical_trials(
    indication: str | None = None,
    phase: list[str] | None = None,
    geography: list[str] | None = None,
    sponsor: str | None = None,
    min_sample_size: int | None = None,
    max_sample_size: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    status: list[str] | None = None,
    study_terms: list[str] | None = None,
    include_pubmed: bool = True,
):
    """
    Search clinical trials and related publications using normalized filters.
    """
    filters = TrialSearchFilters(
        indication=indication,
        phase=phase or [],
        geography=geography or [],
        sponsor=sponsor,
        min_sample_size=min_sample_size,
        max_sample_size=max_sample_size,
        date_from=date_from,
        date_to=date_to,
        status=status or [],
        study_terms=study_terms or [],
    )
    return service.search(filters=filters, include_pubmed=include_pubmed)



if __name__ == "__main__":
    mcp.run()