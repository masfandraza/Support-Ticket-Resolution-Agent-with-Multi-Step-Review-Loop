import os
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3")

def review_draft(inputs):
    test_mode = os.getenv("TEST_MODE")

    if test_mode == "approve":
        return {"review_status": "approved", **inputs}
    elif test_mode == "reject":
        return {
            "review_status": "rejected",
            "review_feedback": "Forced rejection for test mode.",
            **inputs
        }

    # Real review logic (default)
    prompt = f"""You are a reviewer checking support responses.

Review the draft below for accuracy, tone, and policy compliance.

Draft Response:
{inputs['draft']}

Guidelines:
- Do not promise refunds unless approved
- Avoid risky technical or security suggestions
- Be polite and helpful

Respond with:
✅ Approved - if it's good
❌ Rejected - and explain what should be improved
"""
    result = llm.invoke([HumanMessage(content=prompt)])
    response = result.content.strip()

    if "✅" in response:
        return {"review_status": "approved", **inputs}
    else:
        return {
            "review_status": "rejected",
            "review_feedback": "Needs improvement",
            **inputs
        }

reviewer_node = RunnableLambda(review_draft)
