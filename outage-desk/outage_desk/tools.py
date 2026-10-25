"""The tools the agent can use (chapters C8, C10, C11, C15).

Each tool returns plain data plus a "source", so every answer can say exactly
where its facts came from.
"""

from . import approvals, db, docs
from .grid import GridClient, GridUnavailable

_grid = None


def grid():
    global _grid
    if _grid is None:
        _grid = GridClient()
    return _grid


def lookup_account(account_no):
    acc = db.find_account(account_no)
    if not acc:
        return {"found": False, "account_no": str(account_no), "source": "accounts table"}
    acc["medical_priority"] = acc.pop("priority") == "MEDICAL"
    if not acc["area_code"]:
        acc["note"] = "No area on file. Ask the customer for their street address."
    return {"found": True, **acc, "source": f"accounts table, account {acc['account_no']}"}


def get_outage_status(area_code):
    logged = db.open_outage(area_code)
    result = {"area_code": area_code, "outage_log": logged,
              "source": f"outage log {logged['outage_id']}" if logged else "outage log (no open outage)"}
    try:
        live = grid().area_status(area_code)
        result["live_status"] = live
        result["source"] += f"; grid status service, updated {live['updated_at']}"
    except GridUnavailable as e:
        # Say plainly that the live check failed, so nobody quotes a stale time as current.
        result["live_status"] = None
        result["live_error"] = str(e)
    return result


def search_policies(query):
    hits = docs.search(query)
    return {"results": [{"doc": h["doc"], "page": h["page"], "text": h["text"]} for h in hits],
            "source": ", ".join(f"{h['doc']} p.{h['page']}" for h in hits) or "no matching policy"}


def propose_action(kind, account_no, reason):
    return {**approvals.propose(kind, str(account_no), reason), "source": "approvals queue"}


TOOLS = {
    "lookup_account": (lookup_account, "Find a customer by account number. Returns name, area code, "
                       "area name and whether they are on medical priority.", {"account_no": "string"}),
    "get_outage_status": (get_outage_status, "Get the current outage for an area code like S-07: the outage "
                          "log entry plus the live grid status, which has the freshest restore time.",
                          {"area_code": "string"}),
    "search_policies": (search_policies, "Search Larkfield's policy documents (compensation, planned "
                        "maintenance, storm safety). Returns matching pages with document and page number.",
                        {"query": "string"}),
    "propose_action": (propose_action, "Suggest an action for a supervisor to approve. kind is one of "
                       "bill_credit, priority_callback, crew_ticket. You can never approve anything yourself.",
                       {"kind": "string", "account_no": "string", "reason": "string"}),
}


def describe():
    lines = []
    for name, (_, desc, args) in TOOLS.items():
        arg_text = ", ".join(f"{k}: {v}" for k, v in args.items())
        lines.append(f"- {name}({arg_text}): {desc}")
    return "\n".join(lines)
