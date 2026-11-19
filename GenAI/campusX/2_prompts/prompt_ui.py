import streamlit as st
from langchain_core.prompts import load_prompt
from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",  # Required by the OpenAI client, ignored by llama-server
    model="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M",   # Optional: llama-server uses whichever model is loaded
    temperature=0.7,
)

st.header("Paper Summarizer")

paper_input = st.selectbox("Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "	Deep residual learning for image recognition (He et al., ResNet)", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] )

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

# template
template = load_prompt('paper_summarizer_template.json')


if st.button('Summarize'):
    # prompt = template.invoke({
    #     'paper_input':paper_input,
    #     'style_input':style_input,
    #     'length_input':length_input
    # })
    # result = chat_model.invoke(prompt)
    
    chain = template | chat_model
    result = chain.invoke({
        'paper_input':paper_input,
        'style_input':style_input,
        'length_input':length_input
    })
    st.write(result.content)