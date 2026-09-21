// Web entrypoint — mounts the same gated <App /> as Electron.
//
// App.tsx runs the onboarding gates (Intro → Terms → Setup →
// Onboarding → cowork). Each gate's bridge call now goes through
// `host.*`, which routes to ~/.anton/.env via FastAPI in web and via
// window.antontron in Electron. Setup auto-completes on web (the
// FastAPI host running this code IS the install).
//
// Cloud-hosted instances (behind the Cloudflare Worker auth gate) skip
// the Keycloak wrapper entirely — the user already authenticated via
// the MindsHub dashboard, and the Worker's session cookie gates access.
// Keycloak is only needed for standalone web dev (localhost).
//
// Same as main.tsx:
//   - First-paint theme bootstrap (avoids palette flash).
//   - Tailwind + cowork tokens loaded in the same order.

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import './cowork/styles/tailwind.css';
import './cowork/styles/globals.css';
import './cowork/styles/skin-8bit.css';
import './styles.css';
import App from './App';
import { keycloak, scheduleWebTokenRefresh } from './lib/keycloak';
import { loadSkin } from './lib/skins';
import { host } from './platform/host';
import { syncSettingsToDb } from './lib/syncSettings';

// Cloud-hosted instances are accessed via the Cloudflare Worker, which
// already authenticates users via a session cookie minted from their
// MindsHub Keycloak JWT. The SPA doesn't need its own Keycloak login.
// Detect cloud hosting by checking if the hostname is NOT localhost/loopback.
const isCloudHosted = (() => {
  const h = window.location.hostname.replace(/^\[|\]$/g, '');
  return h !== 'localhost' && h !== '127.0.0.1' && h !== '::1';
})();

// Explicit local development opt-in for BYOK without upstream SSO.
// Never bypass authentication in a production build based on this flag.
const skipLocalAuth = import.meta.env.DEV
  && !isCloudHosted
  && import.meta.env.VITE_SKIP_AUTH === 'true';

// Self-hosted deployments with no MindsHub account (docker/web.Dockerfile)
// opt out of the SSO login at build time. Unlike VITE_SKIP_AUTH this is
// honoured in production builds: it is a deliberate deployment setting, not a
// dev toggle, and it has to be spelled out to take effect. Access control for
// such a deployment comes from the network, since the API has no auth itself.
const authDisabled = import.meta.env.VITE_AUTH_MODE === 'none';

// First paint is always dark: the light theme was removed, and honouring a
// stale saved "light" here would flash it before the app forces dark.
document.body.dataset.theme = 'dark';
document.body.dataset.skin = loadSkin();
document.body.classList.add('gf-theme-dark');

const cleanRedirectUri = `${window.location.protocol}//${window.location.host}${window.location.pathname}`;
const initOptions = { onLoad: 'login-required' as const, pkceMethod: 'S256', checkLoginIframe: false, redirectUri: cleanRedirectUri };

const MINDS_ENV_LINES = (token: string) => [
  `ANTON_OPENAI_API_KEY=${token}`,
  `ANTON_MINDS_API_KEY=${token}`,
  `ANTON_OPENAI_BASE_URL=https://api.mindshub.ai/v1`,
];

/** Write MindsHub tokens to both .env (legacy) and the backend DB. */
async function saveMindsToken(token: string): Promise<void> {
  const lines = MINDS_ENV_LINES(token);
  await host.saveSettings(lines.join('\n'));
  await syncSettingsToDb(lines);
}

let stopRefresh: (() => void) | null = null;

function handleKeycloakEvent(event: string): void {
  if (event === 'onAuthSuccess') {
    stopRefresh?.();
    if (keycloak.token) {
      saveMindsToken(keycloak.token).then(() => {
        // After MindsHub credentials are saved, reload so App.tsx
        // re-runs its init and detects the now-configured provider.
        window.location.reload();
      }).catch(() => {});
    }
    stopRefresh = scheduleWebTokenRefresh(async (token) => {
      await saveMindsToken(token);
    });
  } else if (event === 'onAuthLogout' || event === 'onAuthError') {
    stopRefresh?.();
    stopRefresh = null;
  }
}

const root = document.getElementById('root')!;

if (isCloudHosted || skipLocalAuth || authDisabled) {
  // Cloud uses its gateway; opted-in local development and auth-disabled
  // self-hosted builds go straight to the app.
  createRoot(root).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
} else {
  // Local dev: Keycloak handles auth + token refresh.
  createRoot(root).render(
    <StrictMode>
      <ReactKeycloakProvider authClient={keycloak} initOptions={initOptions} onEvent={handleKeycloakEvent}>
        <App />
      </ReactKeycloakProvider>
    </StrictMode>
  );
}
