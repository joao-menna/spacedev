import TextAreaAutosize from "react-textarea-autosize";
import { FormEvent, KeyboardEvent, useRef, useState } from "react";

import { usePromptPlaceholder } from "../hooks";

interface PromptTextArea {
  onSubmit: (value: string) => void;
}

export function PromptTextArea({ onSubmit }: PromptTextArea) {
  const [value, setValue] = useState<string>("");
  const placeholder = usePromptPlaceholder();
  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = (ev: FormEvent) => {
    ev.preventDefault();

    if (!value || !value.trim()) {
      return;
    }

    onSubmit(value.trim());

    setValue("");
  };

  const handleKeyDown = (ev: KeyboardEvent<HTMLTextAreaElement>) => {
    if (ev.key !== "Enter") {
      return;
    }

    if (ev.shiftKey) {
      return;
    }

    ev.preventDefault();

    formRef.current?.requestSubmit();
  };

  return (
    <form onSubmit={handleSubmit} ref={formRef}>
      <TextAreaAutosize
        maxRows={8}
        autoFocus
        placeholder={placeholder}
        onChange={(e) => setValue(e.target.value)}
        value={value}
        onKeyDown={handleKeyDown}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
