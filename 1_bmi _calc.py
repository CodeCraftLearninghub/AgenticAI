# pip install langgraph

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BMIState( TypedDict):
    weight:float
    height:float
    bmi:float

def calc_bmi(state:BMIState) -> BMIState:
    weight= state['weight']
    height=state['height']
    cal_bmi = weight/(height**2)
    state['bmi']=cal_bmi;
    return state



# Define the Graph
graph = StateGraph(BMIState)

# create node
graph.add_node('calculate_bmi', calc_bmi)

graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', END)

workflow = graph.compile()

initial_values = {'weight':90, 'height':1.33}

response  = workflow.invoke(initial_values)

print(response)







