import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({apiKey:"AIzaSyBMF7-vVs1TZ--ZgrFB4MEc-Eh7yD05YaE"});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-lite",
    contents: "What is array, explain LLM?",
  });
  console.log(response.text);
}

await main();