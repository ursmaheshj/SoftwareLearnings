from langchain_openai import OpenAIEmbeddings

embedding_model = OpenAIEmbeddings(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="Qwen/Qwen3-Embedding-0.6B-GGUF:Q8_0",   # Optional: llama-server uses whichever model is loaded
    dimensions=32
)

embeddings = embedding_model.embed_query("Delhi is capital of india")
print(embeddings)
print(len(embeddings))