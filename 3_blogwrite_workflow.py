
# TOPIC -> LLM (outline) -> LLM (final blocg conent) -> responsefrom langgraph.graph import StateGraph, START, END

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key = os.getenv("GROQ_API_KEY")
)

class BlogState(TypedDict):
    title : str
    outline: str
    content : str

def create_outline(state: BlogState)-> BlogState:
    title = state['title']
    outline = model.invoke(f'Generate detailed outline for - {title}')

    state['outline'] = outline

    return state


def crate_blog(state: BlogState)-> BlogState:
    title = state['title']
    outline = state['outline']

    prompt = f'Write a detailed blog on the title - {title} using the follwing outline \n {outline}'

    content = model.invoke(prompt).content

    state['content'] = content
  
    return state


graph = StateGraph(BlogState)

graph.add_node('outline_node', create_outline)
graph.add_node('blog_node', crate_blog)

graph.add_edge(START,'outline_node' )
graph.add_edge('outline_node', 'blog_node')
graph.add_edge('blog_node', END)

workflow = graph.compile()

response = workflow.invoke({'title': 'Rise of Cricket'})

print(response['content'])