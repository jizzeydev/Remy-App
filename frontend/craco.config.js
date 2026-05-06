// craco.config.js
const path = require("path");

// Cargar .env files en el ORDEN correcto de CRA (mayor → menor prioridad):
//   .env.<NODE_ENV>.local  >  .env.local  >  .env.<NODE_ENV>  >  .env
// Antes había `require("dotenv").config()` solo, que cargaba `.env` primero
// y dejaba el localhost en process.env. Cuando CRA después intenta cargar
// `.env.production`, dotenv (sin `override`) ve la var ya seteada y la salta
// → el build de production tenía REACT_APP_BACKEND_URL=http://localhost:8001
// embebido, rompiendo todo deployment fuera de dev (Vercel y Capacitor).
const dotenv = require("dotenv");
const NODE_ENV = process.env.NODE_ENV || "development";
[
  `.env.${NODE_ENV}.local`,
  ".env.local",
  `.env.${NODE_ENV}`,
  ".env",
].forEach((f) => {
  // dotenv NO sobrescribe vars existentes — el primero gana. Por eso
  // iteramos del más específico (mayor prioridad) al genérico.
  dotenv.config({ path: path.resolve(__dirname, f) });
});

// Environment variable overrides
const config = {
  enableHealthCheck: process.env.ENABLE_HEALTH_CHECK === "true",
};

// Conditionally load health check modules only if enabled
let WebpackHealthPlugin;
let setupHealthEndpoints;
let healthPluginInstance;

if (config.enableHealthCheck) {
  WebpackHealthPlugin = require("./plugins/health-check/webpack-health-plugin");
  setupHealthEndpoints = require("./plugins/health-check/health-endpoints");
  healthPluginInstance = new WebpackHealthPlugin();
}

const webpackConfig = {
  eslint: {
    configure: {
      extends: ["plugin:react-hooks/recommended"],
      rules: {
        "react-hooks/rules-of-hooks": "error",
        "react-hooks/exhaustive-deps": "warn",
      },
    },
  },
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    configure: (webpackConfig) => {

      // Add ignored patterns to reduce watched directories
        webpackConfig.watchOptions = {
          ...webpackConfig.watchOptions,
          ignored: [
            '**/node_modules/**',
            '**/.git/**',
            '**/build/**',
            '**/dist/**',
            '**/coverage/**',
            '**/public/**',
        ],
      };

      // Add health check plugin to webpack if enabled
      if (config.enableHealthCheck && healthPluginInstance) {
        webpackConfig.plugins.push(healthPluginInstance);
      }
      return webpackConfig;
    },
  },
};

webpackConfig.devServer = (devServerConfig) => {
  // Add health check endpoints if enabled
  if (config.enableHealthCheck && setupHealthEndpoints && healthPluginInstance) {
    const originalSetupMiddlewares = devServerConfig.setupMiddlewares;

    devServerConfig.setupMiddlewares = (middlewares, devServer) => {
      // Call original setup if exists
      if (originalSetupMiddlewares) {
        middlewares = originalSetupMiddlewares(middlewares, devServer);
      }

      // Setup health endpoints
      setupHealthEndpoints(devServer, healthPluginInstance);

      return middlewares;
    };
  }

  return devServerConfig;
};

module.exports = webpackConfig;
