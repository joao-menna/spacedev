import { IMessage } from "interfaces";

interface MessageProps {
  message: IMessage;
}

export function Message({ message }: MessageProps) {
  return (
    <>
      <p>{message.text}</p>
    </>
  );
}
