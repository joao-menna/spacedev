import { LANGUAGE } from "constants";
import { Translation } from "interfaces";

class TranslationService {
  async getStrings(): Promise<Translation> {
    const strings = await import(`./../i18n/${LANGUAGE}.json`);
    const translation: Translation = strings.default;

    return translation;
  }
}

export const translationService = new TranslationService();
