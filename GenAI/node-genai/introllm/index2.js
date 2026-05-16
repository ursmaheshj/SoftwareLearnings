import dotenv from 'dotenv';
dotenv.config({ path: '../../.env' });
import readlineSync from 'readline-sync';
import { GoogleGenAI } from "@google/genai";
// -------------------
const ai = new GoogleGenAI({apiKey:process.env.API_KEY});

const chat = ai.chats.create({
    model: "gemini-2.5-flash-lite",
    history:[],
  });


async function main() {
    const usermessage = readlineSync.question("Ask me anything?-->")
    const response = await chat.sendMessage({
      message:usermessage
    })
    console.log("\n")
    console.log(response.text);
    main()
}   

await main();