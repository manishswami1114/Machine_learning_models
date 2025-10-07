import asyncio
from langgraph_sdk  import get_client

async def invoke_retrival_assistant():
    
    deployment_url = "http://127.0.0.1:2024"
    client= get_client(url= deployment_url)
    
    try:
        thread = await client.threads.create(
            metadata={
                "user_id":"example_user",
                "session":"retrival_session"
            }
        )
        input_data ={
            "query":"what is this document about?"
        }
        
        async for event in client.runs.stream(
            thread_id = thread["thread_id"],
            assistant_id = "retrival_graph",
            input=input_data,
            stream_mode = "updates"
        ):
            print(f"Receiving event of type:{event.event}")
            print(event.data)
            print("\n")
    except Exception as e:
        print(f"An error occurred:{e}")

asyncio.run(invoke_retrival_assistant())