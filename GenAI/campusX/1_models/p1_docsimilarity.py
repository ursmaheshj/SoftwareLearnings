from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embedding_model = OpenAIEmbeddings(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="Qwen/Qwen3-Embedding-0.6B-GGUF:Q8_0",   # Optional: llama-server uses whichever model is loaded
    dimensions=32
)

docs = [
    "Python is a high-level interpreted language known for its readability and extensive standard library. It is widely used in web development, data science, and automation.",
    "Java is a statically typed, object-oriented language that compiles to bytecode. It runs on the JVM and is popular for enterprise applications and Android development.",
    "Rust is a systems programming language focused on memory safety without garbage collection. It is used in systems programming, game engines, and WebAssembly.",
    "JavaScript is the scripting language of the web, running in browsers and on servers via Node.js. It supports both functional and object-oriented programming paradigms.",
    "Go is a statically typed compiled language designed at Google for concurrent programming. It has simple syntax and is popular for cloud infrastructure and microservices.",
    "Data science is an interdisciplinary field that uses statistics, machine learning, and programming to extract insights from data. Common tools include Python, R, and SQL.",
    "Machine learning is a subset of artificial intelligence that enables systems to learn patterns from data. Deep learning uses neural networks with many layers.",
    "Web development involves building websites and web applications using HTML, CSS, and JavaScript on the frontend, and various server-side languages on the backend.",
    "Cloud computing provides on-demand access to shared pools of configurable computing resources like servers, storage, and databases over the internet.",
    "DevOps is a set of practices combining software development and IT operations to shorten the development lifecycle and deliver software faster and more reliably.",
]

query = "Where is python used"   

docsembeddings = embedding_model.embed_documents(docs)
queryembeddings = embedding_model.embed_query(query)

scores = cosine_similarity([queryembeddings],docsembeddings)[0]

index, score = sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]

print(scores)
print(query)
print(docs[index])
print(score)