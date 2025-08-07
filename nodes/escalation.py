import csv
from datetime import datetime
from langchain_core.runnables import RunnableLambda

def escalate(inputs):
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "subject": inputs["subject"],
        "description": inputs["description"],
        "failed_draft": inputs["draft"],
        "review_feedback": inputs.get("review_feedback", "")
    }
    with open("escalation_log.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(row)
    return {"escalated": True, **inputs}

escalation_node = RunnableLambda(escalate)
