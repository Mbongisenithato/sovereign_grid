import os
import sys
from google.adk import Agent

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.environ.get("GOOGLE_API_KEY"):
    from dotenv import load_dotenv
    load_dotenv()

# Clean single-source import
from tools.stadium_tools import (
    get_gate_telemetry, 
    trigger_crowd_diversion, 
    report_physical_blockage,
    get_historical_blockages,
    search_unstructured_feeds
)

root_agent = Agent(
    name="sovereign_event_grid",
    model="gemini-2.5-flash",
    instruction=(
        "You are the master orchestration engine for the Sovereign Event Grid. "
        "Your role is to handle venue security, monitor transportation corridors, "
        "and maintain crowd safety. Use 'get_gate_telemetry' to check crowd conditions, "
        "use 'trigger_crowd_diversion' to clear fan congestion, and use 'report_physical_blockage' "
        "to investigate structural or vehicular incidents blocking stadium pathways. "
        "Additionally, utilize 'get_historical_blockages' to query previous incidents and patterns, "
        "and use 'search_unstructured_feeds' to scan multi-agency data for context. "
        "If an incident cannot be solved purely by digital tools (e.g., a broken-down vehicle), "
        "provide a tactical action plan (like deploying ground crews or towing services) "
        "while simultaneously using your diversion tools to mitigate crowd build-up around the hazard."
    ),
    tools=[
        get_gate_telemetry, 
        trigger_crowd_diversion, 
        report_physical_blockage, 
        get_historical_blockages, 
        search_unstructured_feeds
    ]
)