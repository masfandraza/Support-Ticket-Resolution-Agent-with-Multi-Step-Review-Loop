from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3")

def classify_ticket(inputs):
    prompt = f"""Classify the support ticket below into one of: Billing, Technical, Security, General.

Subject: {inputs['subject']}
Description: {inputs['description']}

Respond ONLY with the category name."""
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"category": result.content.strip(), **inputs}

classifier_node = RunnableLambda(classify_ticket)
