from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Contact(BaseModel):
    id: Optional[str] = None
    filename: str
    original_name: str
    upload_date: Optional[str] = None
    text_content: str = ""
    page_content: int = 0
    word_count: int = 0
    status: str = "uploaded"

    def model_post_init(self, __context):
        if not self.upload_date:
            self.upload_date = datetime.now().isoformat()


class CaluseAnalysis(BaseModel):
    clause_title: str
    clause_text: str
    explanation: str
    is_standard: bool

class RiskFlag(BaseModel):
    risk_title: str
    description: str
    risk_level: RiskLevel
    recommendation: str
    clause_reference: str = ""

class AnalysisResult(BaseModel):
    id: Optional[str] = None
    contract_id : str
    analysis_date: str = ""
    summary: str = ""
    contract_type: str = ""
    key_clauses: list[CaluseAnalysis] = []
    risk_flags: list[RiskFlag] = []
    overall_risk_level: RiskLevel = RiskLevel.LOW
    recommendation: list[str] = []

    def model_post_init(self, __context):
        if not self.analysis_date:
            self.analysis_date = datetime.now().isoformat()
