"""C15 your turn: reject a suggestion through the service, first without a reason, then with one.

Apply c15-rejections-need-a-reason.patch first, then from outage-desk/:
  PYTHONPATH=. uv run python ../exercises/solutions/part3/c15_check.py
"""

from fastapi.testclient import TestClient

from outage_desk import approvals
from outage_desk.service import app

c = TestClient(app)
aid = approvals.propose("bill_credit", "9999", "exercise check")["id"]
print("reject, no note:", c.post(f"/approvals/{aid}", json={"approve": False, "supervisor": "Maria Lopez"}).status_code)
print("reject, with note:", c.post(f"/approvals/{aid}", json={"approve": False, "supervisor": "Maria Lopez",
      "note": "outage was planned maintenance"}).json())
