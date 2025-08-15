import os
from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,ToolMessage,SystemMessage,HumanMessage,AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from operator import add as add_messages
from langgraph.graph import StateGraph ,END
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

llm = ChatOpenAI(
    model='gpt-4o-mini',temperature=0 # i want to minimize  hallucination - temperature =0 makes the model output more determine 
     embeddings = OpenAIEmbeddings(
         model="text-embedding-3-small",
     )
          )

pdf_path = "Stock_market_performance_2024.pdf"

pdf_loader = PyPDFLoader(pdf_path)

# checks if the PDf is there 
try:
    pages= pdf_loader.load()
    print(f"PDF loaded of {len(pages)} pages")
except Exception as e:
    print(f"Error loading pdf :{e}")
    raise

# chunking process 

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap =200
)
pages_split - text_splitter.split_documents(pages) #we now apply this to our pages

persist_directory = r"/Generative_AI/LangGraph"
collection_name = "stock_market"


# if our collection does not exist in the directory we create using the os cmd 

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)
    
    
try:
    # here we actually create thr chroma database using embedding model
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory
        collection_name=collection_name
    )
    print(f"Created ChromaDB vector store!")
except Exception as e:
    print(f"Enter setting up ChromaDB: {str(e)}")
    raise


# now we create our retriever 

retriever = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k":5} # k is the amount of chunks to return 
)
@tool 
def retriever_tool(quary:str)->str:
    """ This tool searches and return the information from the stock market perfomance 2024 document ."""
    docs = retriever.invoke(quary)
    
    if not docs:
        return "I found  not relevent information in thd file"
    
    results =[]
    
    for i,doc in enumerate(docs):
        results.append(f"document {i+1}:\n{doc.page_content}")
        
    return "\n\n".join(results)

llm =llm.bind_tools(tools)

class AgentState(TypedDict):
    messages = Annotated[Sequence[BaseMessage],add_messages]
    
    
def should_continue(state:AgentState):
    """Check if the last message contains tool calls."""
    result =state["messages"][-1]
    return hasattr(result,'tool_calls') and len(result.tool_calls)>0


system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""

tools_dict ={our_tool.name:our_tool for our_tool in tools} # Creating a dictionary of our tools 

# LLM Agent 
def call_llm(state: AgentState):
    """Funtion to call the LLM with the current state."""
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)]+messages
    message = llm.invoke(messages)
    return {"messages":[message]}



def take_action(state: AgentState)->AgentState:
    """Execute tool calls from the LLM's response"""
    
    tool_calls = state['messages'][-1].tool_calls
    results =[]
    for i in tool_calls:
        print(f"Calling tool:{t['name']} with quary: {t['args'].get('quary','no query provided')}")
        
        if not t['name'] in tools_dict: # checks if a valid tool in present 
            print(f"\nTool :{t['name']} does not exist.")
            result = "incorrect tool name "
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query',''))
            print(f"result length: {len(str(result))}")
            
        # Append the tool Message
        
        result.append(ToolMessage(tool_call_id=t['id'],name=t['name'],content=str(result)))
    print("Tools Execution Complete . Back to the model!")
    return {"messages":results}


graph = StateGraph(AgentState)
graph.add_node('llm',call_llm)
graph.add_node("retriever_agent",take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {True:'retiever_agent',False:END}
)
graph.add_edge('retriever_agent','llm')
graph.set_entry_point('llm')

rag_agent = graph.compile()

def running_agent():
    print("\n===RAG AGENT===")
    
    while True:
        user_input = input("\n what is your question: ")
        if user_input.lower() in ['exit','quit']:
            break
        messages = [HumanMessage(content=user_input)]
        
        result = rag_agent.invoke({"messages":messages})
        
        print("\n===ANSWER===")
        print(result['messages'][-1].content)
        
        
        
running_agent()