import { createContext, PropsWithChildren, useEffect, useState } from "react";
import { translationService } from "services";
import { Translation } from "interfaces";
import { LANGUAGE } from "constants";

export const TranslationContext = createContext<Translation | null>(null);

export function TranslationProvider({ children }: PropsWithChildren) {
  const [translation, setTranslation] = useState<Translation | null>(null);

  useEffect(() => {
    if (!translation) {
      return;
    }

    document.documentElement.lang = LANGUAGE.replace("_", "-");
    loadTranslation();
  }, [translation]);

  const loadTranslation = async () => {
    const strings = await translationService.getStrings();

    setTranslation(strings);
  };

  return (
    <TranslationContext.Provider value={translation}>
      {children}
    </TranslationContext.Provider>
  );
}
