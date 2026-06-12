
#   INPUT  ->  | LLM | -> OUTPUT 

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key = os.getenv("GROQ_API_KEY")
)

class LLMState(TypedDict):
    question: str
    answer : str

def llm_fun(state: LLMState) -> LLMState:
    question = state['question']

    prompt = f'Answer the following question... {question}'

    answer = llm.invoke(prompt).content

    state['answer']= answer

    return state

graph = StateGraph(LLMState)

graph.add_node('llm_node', llm_fun)

graph.add_edge(START, 'llm_node')
graph.add_edge('llm_node', END)

workflow = graph.compile()

response  = workflow.invoke({'question':"write something about india in 50 words"})

print(response['answer'])
