import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";
import { bootCapacitor } from "@/lib/capacitorBoot";
import { initMetaPixel } from "@/lib/metaPixel";

// Inicializa plugins nativos antes de renderizar (no-op en web).
// Es fire-and-forget — no bloqueamos el render por si Capacitor tarda.
bootCapacitor();

// fbq init lo antes posible (antes del primer render): así la cookie _fbp
// se setea temprano y los primeros eventos la incluyen → mejor match quality
// en Events Manager.
initMetaPixel();

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
