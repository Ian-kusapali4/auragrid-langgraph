from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_analysis
import uvicorn

app = FastAPI(title="AuraGrid LangGraph Brain")

class NodeData(BaseModel):
    nodeId: str
    nodeName: str
    batteryLevel: int
    powerStatus: str
    trustScore: float
    taskId: str = None

@app.get("/")
def root():
    return {"status": "AuraGrid LangGraph Brain is running"}

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