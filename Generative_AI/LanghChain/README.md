# Learning LangChain with Free Alternatives

## 🚀 Quick Start with Ollama (Recommended)

### Step 1: Install Ollama
```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/download
```

### Step 2: Install Python Dependencies
```bash
pip install langchain langchain-community ollama
```

### Step 3: Download a Model
```bash
# Choose one of these models:
ollama pull llama2      # Good all-around model
ollama pull mistral     # Better performance, larger
ollama pull codellama   # Great for coding
ollama pull phi2        # Smaller, faster
```

### Step 4: Run Examples
```bash
```

## 🌐 Alternative Free Options

### 1. HuggingFace Inference API
- **Cost**: Free tier available
- **Setup**: Get API token from https://huggingface.co/settings/tokens
- **Models**: Many free models available

### 2. Google Colab
- **Cost**: Free with GPU access
- **Setup**: Run in browser, no local setup needed
- **Limits**: Time limits, but great for learning

### 3. Replicate
- **Cost**: Free tier available
- **Setup**: Get API token from https://replicate.com
- **Models**: Access to many open-source models

## 📚 Learning Path

### Beginner Level
1. Start with `ollama_example.py` - Basic LLM usage
2. Learn about prompts and chains
3. Experiment with different models

### Intermediate Level
1. Study `advanced_examples.py` - Agents, memory, sequential chains
2. Build custom prompt templates
3. Work with conversation memory

### Advanced Level
1. Create custom agents with tools
2. Build RAG (Retrieval-Augmented Generation) systems
3. Implement custom chains and callbacks

## 🛠️ Key LangChain Concepts

### Chains
- **LLMChain**: Basic chain for single LLM calls
- **SequentialChain**: Multiple chains in sequence
- **ConversationChain**: Chat with memory

### Agents
- **Zero-shot**: No examples needed
- **ReAct**: Reasoning and acting
- **Custom**: Build your own

### Memory
- **ConversationBufferMemory**: Simple chat memory
- **ConversationSummaryMemory**: Summarized memory
- **VectorStoreMemory**: Semantic memory

### Tools
- **Search**: DuckDuckGo, Google
- **Calculator**: Math operations
- **Custom**: Build your own tools

## 💡 Tips for Learning

1. **Start Simple**: Begin with basic LLM calls
2. **Experiment**: Try different models and prompts
3. **Build Incrementally**: Add features one by one
4. **Use Examples**: Study the provided code examples
5. **Join Community**: LangChain Discord and GitHub discussions

## 🔧 Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
ollama list

# Restart Ollama
ollama serve

# Check model status
ollama show llama2
```

### Common Errors
- **Model not found**: Run `ollama pull model_name`
- **Connection refused**: Ensure Ollama is running
- **Memory issues**: Use smaller models like `phi2`

## 📖 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [HuggingFace Models](https://huggingface.co/models)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)


Happy Learning! 🚀 