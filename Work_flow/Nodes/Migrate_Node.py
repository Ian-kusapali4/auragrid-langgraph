import os
import requests
from dotenv import load_dotenv
from Work_flow.Graph_State_Schema import GridState


load_dotenv()

COORDINATOR_URL = os.getenv("COORDINATOR_URL")

def migrate(state: GridState) -> GridState:
    """MIGRATING — Find best node and move the task"""
    print(f"🔄 MIGRATING: Finding best available node for task {state.get('task_id', 'unknown')}...")
    
    # 🛡️ Guardrail: Hard exit if configuration is missing
    if not COORDINATOR_URL:
        print("❌ Configuration Error: COORDINATOR_URL is not set in the environment.")
        return {
            **state,
            "current_state": "MIGRATING",
            "migration_status": "FAILED",
            "narration": "Migration failed: Internal configuration error (Missing Coordinator URL)."
        }
        
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
                "narration": f"Migration attempt failed. Coordinator responded with status: {response.status_code}."
            }
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return {
            **state,
            "current_state": "MIGRATING",
            "migration_status": "FAILED",
            "narration": f"Migration failed due to a network or system error: {str(e)}"
        }