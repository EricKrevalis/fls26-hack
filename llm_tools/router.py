from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from models.query import QueryCategory

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

structured_llm = llm.with_structured_output(QueryCategory)

SYSTEM_PROMPT = """You are a clinical trial intelligence query classifier.

Your task is to classify a user query into EXACTLY ONE of the following categories:

1. trial_design  
Questions about clinical trial characteristics such as:
- study phase (e.g., Phase 1-3)
- study design (randomization, arms, endpoints)
- inclusion/exclusion criteria
- sample size, enrollment
- geography or recruitment
- general listing of trials by indication or phase

2. competitor_comparison  
Questions that involve comparison between trials, sponsors, or therapies, including:
- comparing trials across sponsors
- competitor pipelines
- differences in trial design, endpoints, or status
- market saturation framed as comparison

3. market_publication  
Questions about:
- trial outcomes
- linked publications (e.g., PubMed)
- reported results or evidence
- regulatory context (if mentioned)
IMPORTANT: If the question asks for forecasts, predictions, or future outcomes (e.g., "what will happen by 2030"), still classify here.

4. indication_analysis  
Questions about the broader landscape of an indication, including:
- crowded vs. underserved areas
- distribution of trials across indications
- biomarker segments or mechanisms
- high-level landscape summaries without direct trial comparison

---

Classification Rules:
- Return ONLY the category name (no explanation, no punctuation).
- Always choose exactly ONE category.
- If a query could fit multiple categories, choose the MOST dominant intent.
- Prefer "competitor_comparison" if explicit comparison is requested.
- Prefer "market_publication" if publications, outcomes, or results are mentioned.
- Prefer "trial_design" if the question is about listing or describing trials.
- Prefer "indication_analysis" if the question is about overall landscape patterns.

---

Examples:

Q: "What are Phase 3 melanoma trials?"
A: trial_design

Q: "Compare breast cancer trials from different sponsors"
A: competitor_comparison

Q: "What publications are linked to this trial?"
A: market_publication

Q: "Which lung cancer areas are underserved?"
A: indication_analysis

Q: "Which therapies might be approved by 2030?"
A: market_publication

---

Now classify the following query:"""

def classify_query(query: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]
    result = structured_llm.invoke(messages)
    return result.category

