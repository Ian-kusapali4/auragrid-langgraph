import os
import requests
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

load_dotenv()

COORDINATOR_URL = os.getenv("COORDINATOR_URL", "https://auragrid-coordinator.onrender.com")

# ── State Definition ──────────────────────────────────────────
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

# ── Node Functions (LangGraph States) ─────────────────────────

def monitor(state: GridState) -> GridState:
    """MONITORING — Watch the node's power status"""
    print(f"👁️  MONITORING: {state['node_name']} | Battery: {state['battery_level']}% | Power: {state['power_status']}")
    
    narration = f"Monitoring {state['node_name']}. Battery at {state['battery_level']}%. Grid status: {state['power_status']}."
    
    return {
        **state,
        "current_state": "MONITORING",
        "narration": narration
    }

def detect_crisis(state: GridState) -> GridState:
    """CRISIS_DETECTED — Power drop spotted"""
    print(f"🚨 CRISIS DETECTED: {state['node_name']} is UNSTABLE! Battery: {state['battery_level']}%")
    
    narration = f"Grid instability detected on {state['node_name']}. Battery critical at {state['battery_level']}%. Initiating failover protocol."
    
    return {
        **state,
        "current_state": "CRISIS_DETECTED",
        "narration": narration
    }

def migrate(state: GridState) -> GridState:
    """MIGRATING — Find best node and move the task"""
    print(f"🔄 MIGRATING: Finding best available node for task {state.get('task_id', 'unknown')}...")
    
    try:
        # Call AuraGrid coordinator to trigger migration
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

def restored(state: GridState) -> GridState:
    """RESTORED — Task is running on new node"""
    target = state.get("target_node_name", "backup node")
    print(f"✅ RESTORED: Workload now live on {target}")
    
    narration = f"System restored. Workload running on {target}. Original node {state['node_name']} is offline and awaiting power restore. Network stable."
    
    return {
        **state,
        "current_state": "RESTORED",
        "narration": narration
    }

# ── Decision Router ───────────────────────────────────────────
def should_migrate(state: GridState) -> str:
    """Decide next state based on power status"""
    battery = state.get("battery_level", 100)
    power = state.get("power_status", "stable").lower()
    
    if power == "unstable" or battery <= 20:
        print(f"⚡ Decision: CRISIS — Battery {battery}%, Status: {power}")
        return "crisis"
    else:
        print(f"✅ Decision: STABLE — Battery {battery}%, Status: {power}")
        return "stable"

def migration_result(state: GridState) -> str:
    """Check if migration succeeded"""
    if state.get("migration_status") == "SUCCESS":
        return "success"
    return "failed"

# ── Build the LangGraph State Machine ─────────────────────────
def build_auragrid_brain():
    graph = StateGraph(GridState)
    
    # Add all 4 states
    graph.add_node("MONITORING",       monitor)
    graph.add_node("CRISIS_DETECTED",  detect_crisis)
    graph.add_node("MIGRATING",        migrate)
    graph.add_node("RESTORED",         restored)
    
    # Entry point
    graph.set_entry_point("MONITORING")
    
    # Routing logic
    graph.add_conditional_edges(
        "MONITORING",
        should_migrate,
        {
            "crisis": "CRISIS_DETECTED",
            "stable": END
        }
    )
    
    graph.add_edge("CRISIS_DETECTED", "MIGRATING")
    
    graph.add_conditional_edges(
        "MIGRATING",
        migration_result,
        {
            "success": "RESTORED",
            "failed": END
        }
    )
    
    graph.add_edge("RESTORED", END)
    
    return graph.compile()

# ── Run the brain ─────────────────────────────────────────────
auragrid_brain = build_auragrid_brain()

def run_analysis(node_data: dict) -> dict:
    """Main function to analyze a node and decide action"""
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
    
    result = auragrid_brain.invoke(state)
    return result