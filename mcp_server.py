# server.py
import os
from typing import Literal, Optional

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

MCP_MODE = os.getenv("MCP_MODE", "cloud").strip().lower()
IS_LOCAL_MODE = MCP_MODE == "local"

mcp = FastMCP(
    "local-python-tools",
    host="127.0.0.1" if IS_LOCAL_MODE else "0.0.0.0",
    port=int(os.getenv("MCP_PORT", os.getenv("PORT", "8000"))),
    streamable_http_path="/mcp",
    stateless_http=IS_LOCAL_MODE,
    json_response=IS_LOCAL_MODE,
)


class CompetitorTrialQuery(BaseModel):
    indication: str = Field(..., description="Disease or condition, e.g. NSCLC")
    phase: Optional[Literal["Phase 1", "Phase 2", "Phase 3"]] = Field(
        default=None,
        description="Optional clinical phase filter"
        
    )
    geography: Optional[str] = Field(
        default=None,
        description="Optional geography filter, e.g. Europe or United States"
    )
    include_upcoming: bool = Field(
        default=True,
        description="Whether to include not-yet-recruiting or upcoming studies"
    )


@mcp.tool()
def find_competitor_trials(
    indication: str,
    phase: Optional[str] = None,
    geography: Optional[str] = None,
    include_upcoming: bool = True
) -> dict:
    """
    Find competitor clinical trials for a given indication, with optional phase and geography filters.
    Returns structured JSON.
    """
    # Replace with your real implementation
    return {
        "indication": indication,
        "phase": phase,
        "geography": geography,
        "include_upcoming": include_upcoming,
        "results": [
            {"trial_id": "NCT123", "drug": "Drug A", "status": "Recruiting"},
            {"trial_id": "NCT456", "drug": "Drug B", "status": "Not yet recruiting"},
        ],
    }


@mcp.tool()
def benchmark_trial_design(
    sample_size: int,
    comparator_type: Literal["placebo", "standard_of_care", "active_comparator"],
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
) -> dict:
    """
    Benchmark a candidate trial design against historical patterns.
    """
    return {
        "sample_size": sample_size,
        "comparator_type": comparator_type,
        "age_range": [age_min, age_max],
        "benchmark_summary": "Sample size is within the normal range for this category."
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
