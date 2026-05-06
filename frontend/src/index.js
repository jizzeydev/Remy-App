import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";
import { bootCapacitor } from "@/lib/capacitorBoot";

// Inicializa plugins nativos antes de renderizar (no-op en web).
// Es fire-and-forget — no bloqueamos el render por si Capacitor tarda.
bootCapacitor();

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
