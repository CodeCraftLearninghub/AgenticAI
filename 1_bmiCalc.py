#
#   pip install langgraph
#   pip install ipython
#
#   INPUT  ->  | BMI CALC | -> OUTPUT 
#   


from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BMIState(TypedDict):
    weight:float
    height:float
    bmi:float

def calculate_bmi(state:BMIState) -> BMIState:
    weight = state['weight']
    height = state['height']

    bmi = weight/(height**2)

    state['bmi']= bmi
    return state

# Define the Graph
graph = StateGraph(BMIState)

#add nodes to the graph
graph.add_node('calculate_bmi',calculate_bmi)


# add edges
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', END)


# compile workflow
workflow = graph.compile()

# lets test
inital_values = {'weight':90, 'height':1.33}

result = workflow.invoke(inital_values)

print(result)
