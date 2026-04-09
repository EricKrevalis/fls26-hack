from __future__ import annotations

import re
from typing import Any, Optional
import requests

from models import TrialSearchFilters, NormalizedRecord


def extract_nct_ids(text: Optional[str]) -> list[str]:
    if not text:
        return []
    return sorted(set(re.findall(r"\bNCT\d{8}\b", text, flags=re.IGNORECASE)))


class ClinicalTrialsGovClient:
    BASE_URL = "https://clinicaltrials.gov/api/v2"

    def __init__(self, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout

    def search(self, filters: TrialSearchFilters, page_size: int = 100, max_pages: int = 3) -> list[NormalizedRecord]:
        params: dict[str, Any] = {
            "format": "json",
            "countTotal": "true",
            "pageSize": min(page_size, 1000),
            "fields": ",".join([
                "protocolSection.identificationModule.nctId",
                "protocolSection.identificationModule.briefTitle",
                "protocolSection.identificationModule.officialTitle",
                "protocolSection.conditionsModule.conditions",
                "protocolSection.armsInterventionsModule.interventions",
                "protocolSection.designModule.phases",
                "protocolSection.designModule.enrollmentInfo",
                "protocolSection.statusModule.overallStatus",
                "protocolSection.statusModule.startDateStruct",
                "protocolSection.statusModule.primaryCompletionDateStruct",
                "protocolSection.statusModule.completionDateStruct",
                "protocolSection.contactsLocationsModule.locations",
                "protocolSection.sponsorCollaboratorsModule.leadSponsor",
                "protocolSection.sponsorCollaboratorsModule.collaborators",
            ]),
        }

        if filters.indication:
            params["query.cond"] = filters.indication

        if filters.status:
            params["filter.overallStatus"] = ",".join(filters.status)

        records: list[NormalizedRecord] = []
        next_page_token: Optional[str] = None
        pages = 0

        while True:
            if next_page_token:
                params["pageToken"] = next_page_token

            response = self.session.get(f"{self.BASE_URL}/studies", params=params, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()

            for study in payload.get("studies", []):
                record = self._normalize(study)

                if filters.phase:
                    if not set(p.lower() for p in record.phase).intersection(p.lower() for p in filters.phase):
                        continue

                if filters.geography:
                    if not set(g.lower() for g in record.geography).intersection(g.lower() for g in filters.geography):
                        continue

                if filters.sponsor:
                    if filters.sponsor.lower() not in (record.sponsor or "").lower():
                        continue

                if filters.min_sample_size is not None:
                    if record.sample_size is None or record.sample_size < filters.min_sample_size:
                        continue

                if filters.max_sample_size is not None:
                    if record.sample_size is None or record.sample_size > filters.max_sample_size:
                        continue

                records.append(record)

            next_page_token = payload.get("nextPageToken")
            pages += 1

            if not next_page_token or pages >= max_pages:
                break

        return records

    def _normalize(self, study: dict[str, Any]) -> NormalizedRecord:
        protocol = study.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        conds = protocol.get("conditionsModule", {})
        arms = protocol.get("armsInterventionsModule", {})
        design = protocol.get("designModule", {})
        status = protocol.get("statusModule", {})
        locations_mod = protocol.get("contactsLocationsModule", {})
        sponsor_mod = protocol.get("sponsorCollaboratorsModule", {})

        interventions = [
            item["name"]
            for item in arms.get("interventions", [])
            if isinstance(item, dict) and item.get("name")
        ]

        countries = sorted({
            loc.get("country")
            for loc in locations_mod.get("locations", [])
            if isinstance(loc, dict) and loc.get("country")
        })

        lead_sponsor = sponsor_mod.get("leadSponsor", {}) or {}
        sponsor_name = lead_sponsor.get("name")

        sample_size = None
        enrollment_info = design.get("enrollmentInfo", {}) or {}
        count = enrollment_info.get("count")
        if count is not None:
            try:
                sample_size = int(count)
            except (ValueError, TypeError):
                sample_size = None

        return NormalizedRecord(
            source="clinicaltrials_gov",
            record_type="trial",
            source_id=ident.get("nctId", ""),
            title=ident.get("briefTitle"),
            official_title=ident.get("officialTitle"),
            indication=conds.get("conditions", []) or [],
            intervention_names=interventions,
            phase=design.get("phases", []) or [],
            sponsor=sponsor_name,
            status=status.get("overallStatus"),
            geography=countries,
            sample_size=sample_size,
            start_date=(status.get("startDateStruct") or {}).get("date"),
            primary_completion_date=(status.get("primaryCompletionDateStruct") or {}).get("date"),
            completion_date=(status.get("completionDateStruct") or {}).get("date"),
            url=f"https://clinicaltrials.gov/study/{ident.get('nctId')}" if ident.get("nctId") else None,
            source_confidence="high",
        )


class PubMedClient:
    EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, email: str, tool: str = "trial_mcp_server", api_key: Optional[str] = None, timeout: int = 30):
        self.email = email
        self.tool = tool
        self.api_key = api_key
        self.session = requests.Session()
        self.timeout = timeout

    def search(self, filters: TrialSearchFilters, retmax: int = 50) -> list[NormalizedRecord]:
        term_parts = []

        if filters.indication:
            term_parts.append(f'("{filters.indication}"[Title/Abstract] OR "{filters.indication}"[MeSH Terms])')

        if filters.study_terms:
            for term in filters.study_terms:
                term_parts.append(f'"{term}"[Title/Abstract]')

        term_parts.append("(clinical trial[Publication Type] OR trial[Title])")

        if filters.sponsor:
            term_parts.append(f'"{filters.sponsor}"[Title/Abstract]')

        term = " AND ".join(term_parts)

        params = {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retmax": str(retmax),
            "tool": self.tool,
            "email": self.email,
        }
        if self.api_key:
            params["api_key"] = self.api_key

        search_resp = self.session.get(f"{self.EUTILS_BASE}/esearch.fcgi", params=params, timeout=self.timeout)
        search_resp.raise_for_status()
        id_list = search_resp.json().get("esearchresult", {}).get("idlist", [])

        if not id_list:
            return []

        fetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml",
            "tool": self.tool,
            "email": self.email,
        }
        if self.api_key:
            fetch_params["api_key"] = self.api_key

        fetch_resp = self.session.get(f"{self.EUTILS_BASE}/efetch.fcgi", params=fetch_params, timeout=self.timeout)
        fetch_resp.raise_for_status()

        # Für den ersten Schritt könnt ihr hier noch simpel bleiben und später XML sauber parsen.
        # Vorläufig nur grobe Records zurückgeben.
        return [
            NormalizedRecord(
                source="pubmed",
                record_type="publication",
                source_id=pmid,
                title=f"PubMed article {pmid}",
                sponsor=None,
                source_confidence="low",
            )
            for pmid in id_list
        ]