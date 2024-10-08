import { BASE_URL } from "constants";

class ChatService {
  async chat(
    prompt: string,
    chat_id: string,
    chunkCallback: (chunk: string) => void,
    finishedCallback: (response: string) => void
  ): Promise<string> {
    const res = await fetch(`${BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt, chat_id }),
    });

    if (!res.body || res.status !== 200) {
      throw new Error("");
    }

    const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
    const chunks = [];

    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        const response = chunks.join("");
        finishedCallback(response);
        return response;
      }

      chunks.push(value);
      chunkCallback(value);
    }
  }
}

export const chatService = new ChatService();
