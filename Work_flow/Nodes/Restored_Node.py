from Work_flow.Graph_State_Schema import GridState

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