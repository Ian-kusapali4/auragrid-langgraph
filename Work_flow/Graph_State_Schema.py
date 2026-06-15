from typing import TypedDict, Optional

class GridState(TypedDict):
    node_id: str
    node_name: str
    battery_level: int
    power_status: str
    trust_score: float
    task_id: Optional[str]
    target_node_id: Optional[str]
    target_node_name: Optional[str]
    migration_status: Optional[str]
    narration: Optional[str]
    current_state: str