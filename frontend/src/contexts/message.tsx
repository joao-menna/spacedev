import {
  createContext,
  Dispatch,
  PropsWithChildren,
  SetStateAction,
  useState,
} from "react";
import { IMessage } from "interfaces";
import { v4 } from "uuid";

interface IMessageContext {
  chatId: string;
  messages: IMessage[];
  setMessages: Dispatch<SetStateAction<IMessage[]>>;
  setChatId: Dispatch<SetStateAction<string>>;
}

export const MessageContext = createContext<IMessageContext | null>(null);

export function MessageProvider({ children }: PropsWithChildren) {
  const [chatId, setChatId] = useState<string>(v4());
  const [messages, setMessages] = useState<IMessage[]>([]);

  const defaultValue = {
    chatId,
    messages,
    setMessages,
    setChatId,
  };

  return (
    <MessageContext.Provider value={defaultValue}>
      {children}
    </MessageContext.Provider>
  );
}
