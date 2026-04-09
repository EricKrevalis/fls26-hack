from __future__ import annotations

from models import TrialSearchFilters, TrialSearchResponse
from api_clients import ClinicalTrialsGovClient, PubMedClient


class TrialSearchService:
    def __init__(self):
        self.ctgov = ClinicalTrialsGovClient()
        self.pubmed = PubMedClient(email="your_email@example.com")

    def search(self, filters: TrialSearchFilters, include_pubmed: bool = True) -> TrialSearchResponse:
        results = []

        ctgov_results = self.ctgov.search(filters)
        results.extend(ctgov_results)

        if include_pubmed:
            pubmed_results = self.pubmed.search(filters)
            results.extend(pubmed_results)

        seen = set()
        deduped = []
        for record in results:
            key = (record.source, record.source_id)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(record)

        return TrialSearchResponse(
            query=filters,
            total_results=len(deduped),
            results=deduped,
        )