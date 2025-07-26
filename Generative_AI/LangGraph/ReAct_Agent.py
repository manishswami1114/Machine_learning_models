from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The Foundational class of all message types in langhchain
from langchain_core.messages import ToolMessage # Passes data back to llm after it calls a tool such as the content and the tool_call   
from langchain_core.messages import SystemMessage # Message for providing instuctions to the LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages  # Reducer Function 
from langgraph.graph import StateGraph ,END
from langgraph.prebuilt import ToolNode

load_dotenv()

# Annoted - provides additional context without affecting the type itself   
class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]
    
    
@tool
def add(a:int,b:int):
    """This is a addition function that add 2 numbers together"""
    return a+b


def subtract(a:int,b:int):
    """This is a subtraction function that subtract 2 numbers together"""
    return a-b


def multiply(a:int,b:int):
    """This is a multiplication function that multiply 2 numbers together"""
    return a*b


tools=[add,subtract,multiply]

model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

def model_call(state:AgentState)->AgentState:
    system_prompt = SystemMessage(content=
                                  "you are my AI assistant , please answer my quary to the best of your ability.")
    response=model.invoke([system_prompt])+state["messages"]
    return {"messages":[response]} 


def should_continue(state: AgentState):
    messages=state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
    
graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)


tool_node = ToolNode(tools=tools)
graph.add_node('tools',tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        'continue':'tools',
        'end':END
    },
)

graph.add_edge('tools','our_agent')
app= graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()
            

inputs = {'messages':[('user','Add 34+21. Add 3+4 and also tell me a joke ')]} # in this we giving two cmd of reaction and action 
print_stream(app.stream(inputs,stream_mode='values'))
