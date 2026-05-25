import os, sys, ssl
from fastmcp import FastMCP
from pymongo import MongoClient
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
mcp = FastMCP("StadiumTools")
@mcp.tool()
def get_gate_telemetry(gate_id: str) -> str:
    if "gate_a" in gate_id.lower(): return "ALERT: 48,000 fans queued at Gate_A. Backlog extending 200m."
    return f"STATUS NORMAL: Flow at {gate_id} is nominal."
@mcp.tool()
def trigger_crowd_diversion(sector_id: str, promotion_type: str = "diversion digital") -> str:
    return f"SUCCESS: Broadcasted 15,000 {promotion_type} vouchers to {sector_id}."
@mcp.tool()
def report_physical_blockage(location: str) -> str:
    if any(k in location.lower() for k in ["corridor", "plaza", "bus"]): return "OBSTRUCTION DETECTED: Transit bus mechanical failure blocking corridor near Gate_A."
    return f"Sweep complete for {location}. No active blockages."
def _get_historical_db():
    uri = os.getenv("MONGO_URI")
    if not uri: raise ValueError("MONGO_URI missing.")
    return MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)["sovereign_grid"]
@mcp.tool()
def get_historical_blockages(location: str = "main transit corridor") -> str:
    try:
        res = list(_get_historical_db()["incident_historical"].find({"location": {"$regex": location, "$options": "i"}}).limit(3))
        if not res: return f"No records found for {location}"
        return " | ".join([f"[{d.get('date', '2026-03-12')}] {d.get('description', 'Failure')}" for d in res])
    except Exception as e: return f"DB Error: {e}"
@mcp.tool()
def search_unstructured_feeds(query: str) -> str: return "Search complete. 0 anomalies."
if __name__ == "__main__": mcp.run(transport="stdio")
