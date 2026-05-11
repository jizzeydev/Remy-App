# Meta Pixel + Conversions API — setup Remy

Cómo dejar operativo el tracking de conversiones de Meta Ads (Facebook + Instagram) para `remy.seremonta.store`.

## Resumen del diseño

Doble track (recomendado por Meta): cada evento se dispara **dos veces** con el mismo `event_id` para que Meta deduplique.

1. **Pixel (browser-side)** — script en [frontend/public/index.html](../frontend/public/index.html), inicializado con `REACT_APP_META_PIXEL_ID`. Helper en [frontend/src/lib/metaPixel.js](../frontend/src/lib/metaPixel.js).
2. **Conversions API (server-side)** — `httpx` a `graph.facebook.com`. Servicio en [backend/services/meta_pixel_service.py](../backend/services/meta_pixel_service.py). Endpoint forwarder en [backend/routes/meta_pixel.py](../backend/routes/meta_pixel.py) (`POST /api/meta/track`).

El server-side es **autoritativo** para `Subscribe` / `Purchase` (se dispara desde el webhook de Mercado Pago — no se puede falsificar y resiste ad-blockers / iOS ITP).

## Eventos que ya están cableados

| Evento | Dónde se dispara | Browser | Server | Notas |
|---|---|---|---|---|
| `PageView` | Cada cambio de ruta en SPA | ✓ | ✓ | App.js → `MetaPixelRouteTracker` |
| `Lead` | Registro de usuario nuevo (Google) | — | ✓ | `routes/auth.py` |
| `CompleteRegistration` | Registro de usuario nuevo | — | ✓ | `routes/auth.py` |
| `StartTrial` | Registro con trial habilitado | — | ✓ | `routes/auth.py` |
| `InitiateCheckout` | Carga de `/subscribe` con plan | ✓ | ✓ | `pages/SubscribePage.js` |
| `Subscribe` | Pago MP aprobado | — | ✓ | Webhook MP (`routes/payments.py`) |
| `Purchase` | Pago MP aprobado | — | ✓ | Webhook MP (`routes/payments.py`) |

`Subscribe` y `Purchase` se firman con `event_id = mp_sub_<payment_id>` / `mp_pur_<payment_id>` para que Meta deduplique reentregas del webhook.

## Setup paso a paso (en Meta Events Manager)

### 1. Crear el Pixel dedicado para Remy

1. Entrar a [business.facebook.com/events_manager](https://business.facebook.com/events_manager) con la cuenta de Se Remonta.
2. **Data Sources → Add → Web → Connect**.
3. Nombre: `Remy — remy.seremonta.store`. URL: `https://remy.seremonta.store`.
4. Copiar el **Pixel ID** (15-16 dígitos).

> No reutilizar el Pixel de `seremonta.store`: querés conversiones limpias por subdominio para optimizar campañas separadas.

### 2. Generar Access Token para Conversions API

1. En el Pixel recién creado: **Settings → Conversions API → Generate access token**.
2. Guardar el token. **No tiene expiración** salvo que lo rotes manualmente.

### 3. Configurar variables de entorno

**Frontend** ([frontend/.env.production](../frontend/.env.production) y/o el entorno de Vercel):
```
REACT_APP_META_PIXEL_ID=<pixel_id>
```

**Backend** ([backend/.env](../backend/.env) y/o Render env vars):
```
META_PIXEL_ID=<mismo pixel_id>
META_ACCESS_TOKEN=<access token de paso 2>
META_TEST_EVENT_CODE=          # vacío en prod; rellenar solo para QA
```

### 4. QA en Events Manager → Test events

1. En el Pixel → **Test events**.
2. Copiar el **Test Event Code** (tipo `TEST12345`).
3. Setear `META_TEST_EVENT_CODE` en backend localmente.
4. Reiniciar backend, navegar Remy en local. Los eventos aparecen en la consola de Test events en tiempo real.
5. **Importante**: borrar `META_TEST_EVENT_CODE` antes de desplegar a prod (si queda, los eventos NO cuentan para optimización de ads — quedan solo en la pestaña de test).

### 5. Configurar deduplicación

Cuando los primeros eventos lleguen vía Pixel + CAPI, en **Events Manager → Overview → Diagnostics** debería aparecer "Duplicate events detected — deduplicated by event_id". Si no aparece, revisar que el `event_id` viaja igual en ambos canales.

### 6. Configurar conversiones para campañas

1. En **Ads Manager → Campañas**, al crear una campaña tipo "Sales" o "Leads":
2. Performance goal: **Maximize number of conversions** o **Maximize value of conversions**.
3. Conversion event: elegir entre los que ya están cableados:
   - **Lead campaigns** → optimizar por `CompleteRegistration` o `StartTrial`.
   - **Sales campaigns** → optimizar por `Subscribe` (suscripción recurrente) o `Purchase`.

## Vericación rápida (smoke test)

```bash
# 1. Levantar backend y frontend localmente con META_TEST_EVENT_CODE seteado.
# 2. Abrir Remy en el browser con la extensión "Meta Pixel Helper" instalada.
# 3. Navegar / → /auth → login → /biblioteca → /subscribe.
# 4. Verificar en Pixel Helper: PageView, InitiateCheckout, (si registro nuevo) Lead/CompleteRegistration/StartTrial.
# 5. En Events Manager → Test events: ver los mismos eventos con event_id matcheando.
```

## Cuándo desactivar el tracking

Para QA o si Meta corta el access token: dejar `META_PIXEL_ID` y `META_ACCESS_TOKEN` vacíos. El sistema entero queda como no-op silencioso, no hay errores en logs, no hay requests fallidos al graph API.

## Privacidad

- Email, nombre y `user_id` se envían **hasheados con SHA-256** (requerimiento de Meta para PII).
- Hashing en [backend/services/meta_pixel_service.py:`_hash`](../backend/services/meta_pixel_service.py).
- No enviamos teléfono ni dirección — Remy no los pide.
- IP y user-agent **no se hashean** (Meta los pide en plano para attribution).
