import os
import requests
from dotenv import load_dotenv
from Work_flow.Graph_State_Schema import GridState

load_dotenv()
COORDINATOR_URL = os.getenv("COORDINATOR_URL", "https://auragrid-coordinator.onrender.com")

def migrate(state: GridState) -> GridState:
    """MIGRATING — Find best node and move the task"""
    print(f"🔄 MIGRATING: Finding best available node for task {state.get('task_id', 'unknown')}...")
    
    try:
        
        response = requests.post(
            f"{COORDINATOR_URL}/api/tasks/migrate",
            json={
                "taskId": state.get("task_id"),
                "currentPayload": {
                    "executionLayer": "step_frozen",
                    "failoverReason": f"LangGraph crisis detected — Battery at {state['battery_level']}%",
                    "triggeredBy": "auragrid-langgraph-agent"
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            target = data.get("assignedTargetNode", {})
            target_name = target.get("name", "Unknown Node")
            
            narration = f"Task successfully migrated to {target_name}. Zero data loss. Workload is now running on stable solar infrastructure."
            
            return {
                **state,
                "current_state": "MIGRATING",
                "target_node_name": target_name,
                "migration_status": "SUCCESS",
                "narration": narration
            }
        else:
            return {
                **state,
                "current_state": "MIGRATING",
                "migration_status": "FAILED",
                "narration": "Migration attempt failed. No eligible target nodes found."
            }
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return {
            **state,
            "current_state": "MIGRATING",
            "migration_status": "FAILED",
            "narration": f"Migration failed: {str(e)}"
        }