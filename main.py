import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from Work_flow.Build_Graph import auragrid_brain
from Work_flow.Graph_State_Schema import GridState

app = FastAPI(title="AuraGrid LangGraph Brain")

class NodeData(BaseModel):
    nodeId: str
    nodeName: str
    batteryLevel: int
    powerStatus: str
    trustScore: float
    taskId: str = None

# Ensure this specific block is present and spelled correctly:
@app.get("/")
def root():
    return {"status": "AuraGrid LangGraph Brain is running"}

def run_analysis(node_data: dict) -> dict:
    state = GridState(
        node_id=node_data.get("nodeId", "unknown"),
        node_name=node_data.get("nodeName", "Unknown Node"),
        battery_level=node_data.get("batteryLevel", 100),
        power_status=node_data.get("powerStatus", "stable"),
        trust_score=node_data.get("trustScore", 100.0),
        task_id=node_data.get("taskId"),
        target_node_id=None,
        target_node_name=None,
        migration_status=None,
        narration=None,
        current_state="MONITORING"
    )
    return auragrid_brain.invoke(state)

@app.post("/analyze")
def analyze_node(data: NodeData):
    result = run_analysis(data.dict())
    return {
        "state": result["current_state"],
        "narration": result["narration"],
        "migrationStatus": result.get("migration_status"),
        "targetNode": result.get("target_node_name")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)