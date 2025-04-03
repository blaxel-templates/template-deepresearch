from pydantic import BaseModel


class DeepSearchInput(BaseModel):
    inputs: str
    recursion_limit: int = 50
    report_plan_depth: int = 8