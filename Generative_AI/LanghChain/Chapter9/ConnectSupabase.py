import os
from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_ollama import OllamaEmbeddings
from supabase.client import Client,create_client

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase:Client  = create_client(supabase_url,supabase_key)

embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")

vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents"
)


query = "what is this document about?"

# seed
vector_store.add_texts(
    texts=["Test doc about LangChain + Supabase using mxbai-embed-large."],
    metadatas=[{"topic": "langchain"}],
)


matched_docs = vector_store.similarity_search("what is this document about?", k=3)
print(matched_docs[0].page_content)
