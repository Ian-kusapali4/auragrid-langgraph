from Work_flow.Graph_State_Schema import GridState

def detect_crisis(state: GridState) -> GridState:
    """CRISIS_DETECTED — Power drop spotted"""
    print(f"🚨 CRISIS DETECTED: {state['node_name']} is UNSTABLE! Battery: {state['battery_level']}%")
    
    narration = f"Grid instability detected on {state['node_name']}. Battery critical at {state['battery_level']}%. Initiating failover protocol."
    
    return {
        **state,
        "current_state": "CRISIS_DETECTED",
        "narration": narration
    }