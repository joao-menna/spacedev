export interface IMessage {
  id: string;
  owner: "copilot" | "you";
  text: string;
}
