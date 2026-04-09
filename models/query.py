from pydantic import Field

from models.common import StandardModel
from models.enums import QueryCategoryValue


class QueryCategory(StandardModel):
    category: QueryCategoryValue = Field(..., description="The dominant intent category for the query.")
