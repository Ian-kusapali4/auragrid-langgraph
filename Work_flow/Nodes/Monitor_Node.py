from Work_flow.Graph_State_Schema import GridState

def monitor(state: GridState) -> GridState:
    """MONITORING — Watch the node's power status"""
    print(f"👁️  MONITORING: {state['node_name']} | Battery: {state['battery_level']}% | Power: {state['power_status']}")
    
    narration = f"Monitoring {state['node_name']}. Battery at {state['battery_level']}%. Grid status: {state['power_status']}."
    
    
    return {
        **state,
        "current_state": "MONITORING",
        "narration": narration
    }