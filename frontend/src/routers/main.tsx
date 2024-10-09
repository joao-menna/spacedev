import { createBrowserRouter } from "react-router-dom";
import { ChatPage } from "pages";
import { MainLayout } from "layouts/main";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        path: "",
        element: <ChatPage />,
      },
    ],
  },
]);
