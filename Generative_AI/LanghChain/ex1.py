from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(model="llama3.1:8b")

model.invoke("the sky is blue")
