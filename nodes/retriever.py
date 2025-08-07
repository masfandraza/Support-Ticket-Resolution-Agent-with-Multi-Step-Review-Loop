import json
from langchain_core.runnables import RunnableLambda

def retrieve_context(inputs):
    category = inputs["category"].lower()
    file_path = f"data/{category}_docs.json"

    with open(file_path, "r") as f:
        docs = json.load(f)

    feedback = inputs.get("review_feedback", "")
    description = inputs.get("description", "")
    subject = inputs.get("subject", "")

    # Refine results using feedback
    if feedback:
        refined_docs = [doc for doc in docs if any(
            kw in doc.lower() for kw in feedback.lower().split())]
        if refined_docs:
            docs = refined_docs

    return {"context": docs, **inputs}

retriever_node = RunnableLambda(retrieve_context)
