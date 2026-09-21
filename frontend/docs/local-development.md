# Local browser development

Start the Core API separately on port 26866. In PowerShell, from `frontend`:

```powershell
npm.cmd ci
$env:BUILD_TARGET = "web"
$env:COWORK_SERVER_PORT = "26866"
npm.cmd run dev:renderer -- --open
```

For local development with your own provider key, create the gitignored
`src/renderer/.env.local` containing:

```dotenv
VITE_SKIP_AUTH=true
```

Restart Vite and open http://localhost:5173/ directly. This opt-in only applies
to development builds on localhost, 127.0.0.1 or IPv6 loopback. Production builds
ignore it. Configure your model provider during onboarding.

To use Keycloak locally instead, remove the flag and configure the identity
server client's Valid Redirect URIs and Web Origins to match your local URL.
Changing this repository cannot change the upstream client's allowlist.

## Dependency security update (2026-09-15)

The lockfile was updated to compatible patched dependencies; Electron required
an upgrade from 39 to 44.3.0. The obsolete optional appdmg dependency was removed;
the custom macOS DMG script now uses the existing electron-builder DMG layout
and prepackaged application support. PostCSS exports CommonJS to match the
package's existing module configuration.

Validation: npm audit reported zero vulnerabilities; main-process TypeScript
compilation and production web build passed; local auth opt-in checks covered
development, production, disabled flag, remote host, and IPv6 loopback.
The web build still reports existing asset, eval, and chunk-size warnings.
Full desktop workflows and macOS DMG packaging were not exercised on this Windows
machine. A clean audit is not a complete application security review.
