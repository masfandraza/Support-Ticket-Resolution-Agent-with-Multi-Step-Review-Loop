from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3")

def generate_draft(inputs):
    context = "\n".join(inputs["context"])
    subject = inputs["subject"]
    description = inputs["description"]
    feedback = inputs.get("review_feedback", "")

    prompt = f"""You are a support agent responding to a customer ticket.

Subject: {subject}
Description: {description}

Relevant Knowledge:
{context}

Write a clear and helpful response to the user.

{"Make sure to address the following feedback from the reviewer: " + feedback if feedback else ""}
"""

    result = llm.invoke([HumanMessage(content=prompt)])
    return {"draft": result.content.strip(), **inputs}

draft_generator_node = RunnableLambda(generate_draft)
