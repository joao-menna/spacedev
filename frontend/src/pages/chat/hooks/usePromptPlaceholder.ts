import { useTranslation } from "hooks";

export function usePromptPlaceholder() {
  const strings = useTranslation();
  const placeholders = strings?.PromptPlaceholders;

  if (!placeholders) {
    return "";
  }

  return placeholders[Math.floor(Math.random() * placeholders.length)];
}
