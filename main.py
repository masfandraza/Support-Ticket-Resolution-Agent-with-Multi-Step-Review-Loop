from langgraph.graph import StateGraph, END
from nodes.classifier import classifier_node
from nodes.retriever import retriever_node
from nodes.draft_generator import draft_generator_node
from nodes.reviewer import reviewer_node
from nodes.escalation import escalation_node

# Retry Logic
def should_retry(data):
    return data.get("review_status") == "rejected" and data.get("retry_count", 0) < 2

def increment_retry_count(data):
    return {**data, "retry_count": data.get("retry_count", 0) + 1}

def route_after_review(data):
    if data.get("review_status") == "approved":
        return "__end__"
    elif should_retry(data):
        return "retry"
    else:
        return "escalate"

workflow = StateGraph(dict)

workflow.set_entry_point("classify")

workflow.add_node("classify", classifier_node)
workflow.add_node("retrieve", retriever_node)
workflow.add_node("draft", draft_generator_node)
workflow.add_node("review", reviewer_node)
workflow.add_node("retry", increment_retry_count)
workflow.add_node("escalate", escalation_node)

workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "draft")
workflow.add_edge("draft", "review")
workflow.add_edge("retry", "retrieve")
workflow.add_edge("escalate", END)

workflow.add_conditional_edges("review", route_after_review)

graph = workflow.compile()

if __name__ == "__main__":
    ticket = {
        "subject": "Refund request not processed",
        "description": "I was promised a refund last week but haven't received it yet.",
        "retry_count": 0
    }

    result = graph.invoke(ticket)
    print(result)
