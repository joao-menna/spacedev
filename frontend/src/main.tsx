import { RouterProvider } from "react-router-dom";
import { createRoot } from "react-dom/client";
import { router } from "routers/main";
import { StrictMode } from "react";

import "./index.css";
import { TranslationProvider } from "contexts/translation";
import { MessageProvider } from "contexts/message";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <TranslationProvider>
      <MessageProvider>
        <RouterProvider router={router} />
      </MessageProvider>
    </TranslationProvider>
  </StrictMode>
);
