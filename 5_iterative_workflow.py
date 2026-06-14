#                ┌─────────┐
#                │  START  │
#                └────┬────┘
#                     │
#                     ▼
#         ┌────────────────────┐
#  |----->│   Take Quiz        │
#  |      └─────────┬──────────┘
#  |                │
#  |                ▼
#  |      ┌────────────────────┐
#  |      │   Evaluate Score   │
#  |      └─────────┬──────────┘
#  |                 │
#  |       ┌─────────┴───────────┐
#  |       │                     │
#  | Score < 70            Score >= 70
#  |       │                     │
#  |       ▼                     ▼
# ┌────────────────┐    ┌─────────────┐
# │ Study Material │    │    PASS     │
# └───────┬────────┘    └──────┬──────┘
#                              │
#                              │
#                              │
#                              ▼
#                             END
#                                        


from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random


class QuizState(TypedDict):
    score: int
    attempts: int


def take_quiz(state):
    score = random.randint(40, 100)

    print(f"Quiz Score: {score}")

    return {
        "score": score,
        "attempts": state.get("attempts", 0) + 1
    }


def study_material(state):
    print("Studying material...")
    return {}


def check_score(state):
    if state["score"] >= 70:
        return "pass"
    return "retry"


builder = StateGraph(QuizState)

builder.add_node("quiz", take_quiz)
builder.add_node("study", study_material)

builder.add_edge(START, "quiz")

builder.add_conditional_edges(
    "quiz",
    check_score,
    {
        "pass": END,
        "retry": "study"
    }
)

builder.add_edge("study", "quiz")

graph = builder.compile()

result = graph.invoke(
    {
        "attempts": 0
    }
)

print(result)