import { MessageContext } from "contexts/message";
import { useContext } from "react";
import { Message } from "./Message";

interface MessagesContainerProps {
  loading?: boolean;
}

export function MessagesContainer({ loading = false }: MessagesContainerProps) {
  const { messages } = useContext(MessageContext)!;

  return (
    <div className="flex flex-col">
      {messages.map((value) => (
        <Message key={value.id} message={value} />
      ))}
      {loading && <p>Loading...</p>}
    </div>
  );
}
