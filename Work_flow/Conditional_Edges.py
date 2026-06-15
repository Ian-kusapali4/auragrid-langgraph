from Work_flow.Graph_State_Schema import GridState

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