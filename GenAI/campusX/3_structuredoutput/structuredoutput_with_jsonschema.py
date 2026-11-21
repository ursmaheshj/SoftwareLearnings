from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    # model="Qwen/Qwen3-Embedding-0.6B-GGUF:Q8_0",   # Optional: llama-server uses whichever model is loaded
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    temperature=0.7,
)

# ----------------Output schema with JSON
review_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Write down all the key themes discussed in this review"
    },
    "summary": {
      "type": "string",
      "description": "Brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": [
        "pos",
        "neg"
      ],
      "description": "Return sentiment of review either negative or positive"
    },
    "pros": {
      "type": ["array","null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the pros inside a list"
    },
    "cons": {
      "type": ["array","null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the cons inside a list"
    }
  },
  "required": [
    "key_themes",
    "summary",
    "sentiment"
  ]
}

# ---------------creation of structured output model 
structured_model = chat_model.with_structured_output(review_schema)

# ----------------Simple ChatBot 
while True:
    user_input = input("you:")
    if user_input == '':
        user_input = "The hardware is great, but the software feels bloated. There are too many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other brands. Hoping for a software update to fix this."
        # user_input = "lightning fast-whether Im gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver. The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera-the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality. However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung One UI still comes with bloatware-why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow. I s Pros: Insanely powerful processor (great for gaming and productivity) Stunning 200MP camera with incredible zoom capabilities Long battery life with fast charging"
    if user_input.lower() == 'exit':
        break

    result = structured_model.invoke(user_input)
    print("AI: ",result)
