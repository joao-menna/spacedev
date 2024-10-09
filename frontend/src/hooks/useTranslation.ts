import { TranslationContext } from "contexts/translation";
import { useContext } from "react";

export function useTranslation() {
  const translation = useContext(TranslationContext);
  return translation;
}
