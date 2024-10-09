import { MessageContext } from "contexts/message";
import { useContext, useState } from "react";
import { chatService } from "services";
import { v4 } from "uuid";

import { MessagesContainer, PromptTextArea } from "./components";

export function ChatPage() {
  const { chatId, setMessages } = useContext(MessageContext)!;
  const [loading, setLoading] = useState<boolean>(false);

  const finishedCallback = (response: string) => {
    setMessages((state) => {
      state.push({ id: v4(), owner: "copilot", text: response });
      return state;
    });

    setLoading(false);
  };

  const handleSubmit = async (value: string) => {
    setMessages((state) => {
      state.push({ id: v4(), owner: "you", text: value });
      return state;
    });

    setLoading(true);
    chatService.chat(value, chatId, () => {}, finishedCallback);
  };

  return (
    <div className="flex flex-col">
      <PromptTextArea onSubmit={handleSubmit} />
      <MessagesContainer loading={loading} />
    </div>
  );
}
