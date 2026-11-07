import dotenv from 'dotenv';
dotenv.config({ path: '../../.env' });
import readlinesync from 'readline-sync';
import { GoogleGenAI } from "@google/genai";
// -------------------
const ai = new GoogleGenAI({apiKey:process.env.API_KEY});

const history = []

async function genaiChatting(usermessage) {
    history.push({
        role:"user",
        parts:[{text:usermessage}]
    })
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-lite",
    contents:history
  });

  history.push({
        role:"model",
        parts:[{text:response.text}]
    })
    console.log("\n")
  console.log(response.text);
}

async function main() {
    const usermessage = readlinesync.question("Ask me anything?-->")
    await genaiChatting(usermessage)
    main()
}   

await main();