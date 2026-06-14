#                ┌─────────┐
#                │  START  │
#                └────┬────┘
#                     │
#                     ▼
#        ┌─────────────────────────┐
#        │   Classify User Query   │
#        └───────────┬─────────────┘
#                    │
#         ┌──────────┴──────────┐
#         │                     │
#         ▼                     ▼
# ┌────────────────┐   ┌────────────────┐
# │ Technical Path │   │   Sales Path   │
# └───────┬────────┘   └───────┬────────┘
#         │                    │
#         ▼                    ▼
# ┌────────────────┐   ┌────────────────┐
# │ Generate Tech  │   │ Generate Sales │
# │    Response    │   │    Response    │
# └───────┬────────┘   └───────┬────────┘
#         │                    │
#         └─────────┬──────────┘
#                   │
#                   ▼
#             ┌─────────┐
#             │   END   │
#             └─────────┘
#








from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Define State
class AgentState(TypedDict):
    query: str
    category: str
    response: str


# Node 1: Classify User Query
def classify_query(state: AgentState):
    query = state["query"].lower()

    if any(word in query for word in ["error", "bug", "issue"]):
        category = "technical"
    else:
        category = "sales"

    return {"category": category}


# Node 2: Technical Support
def technical_support(state: AgentState):
    return {
        "response": "This query has been routed to Technical Support."
    }


# Node 3: Sales Support
def sales_support(state: AgentState):
    return {
        "response": "This query has been routed to Sales Support."
    }


# Conditional Edge Function
def route_query(state: AgentState):
    return state["category"]


# Create Graph
builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("classify", classify_query)
builder.add_node("technical", technical_support)
builder.add_node("sales", sales_support)

# Add Edges
builder.add_edge(START, "classify")

# Conditional Routing
builder.add_conditional_edges(
    "classify",
    route_query,
    {
        "technical": "technical",
        "sales": "sales",
    },
)

builder.add_edge("technical", END)
builder.add_edge("sales", END)

# Compile Graph
graph = builder.compile()

# Execute Graph
result = graph.invoke(
    {"query": "I am wanted renewal my subscription"}
)

print(result)