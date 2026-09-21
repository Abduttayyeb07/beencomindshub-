import { useState, useEffect } from 'react';
import SetupScreen from './pages/arcade/SetupScreen';
import CoworkApp from './CoworkApp';
import { host } from './platform/host';
import './styles.css';

// Pre-app gate. The model provider is configured server-side (the managed
// Bedrock gateway), so there is nothing for the user to pick before using the
// app: the title, terms, coworker, theme and provider ("POWER UP") screens are
// all gone. The only screen left is Setup, which installs the Python runtime
// on a fresh desktop machine. On web the FastAPI host IS the install, so Setup
// never appears there.
type Page = 'loading' | 'setup' | 'terminal';

export default function App() {
  const [page, setPage] = useState<Page>('loading');

  useEffect(() => {
    async function init() {
      try {
        // Both halves of "ready to start the server": is the anton CLI
        // installed, AND are the Python deps the bundled FastAPI server
        // needs importable from the tool venv. On web both are reported true.
        const status = await host.checkInstall();
        setPage(!status.antonInstalled || !status.serverDepsReady ? 'setup' : 'terminal');
      } catch {
        // Backend unreachable (not yet started, or restarting). Open the app
        // anyway: it shows its own connection error and recovers once the
        // server is back. Routing to an onboarding screen here would put the
        // user in front of a provider picker for what is only an outage.
        setPage('terminal');
      }
    }
    init();
  }, []);

  const isMac = host.isMac();

  return (
    <>
      {/* Top-of-window drag overlay for the Setup screen, which has no
          draggable chrome of its own. The app provides drag via its sidebar
          header, and the overlay would block the sidebar's top ~38px. */}
      {isMac && page === 'setup' && <div className="titlebar-drag" />}

      {page === 'loading' && (
        <div style={{ position: 'fixed', inset: 0, background: '#0a0a13' }} />
      )}

      {page === 'setup' && <SetupScreen onComplete={() => setPage('terminal')} />}

      {page === 'terminal' && <CoworkApp />}
    </>
  );
}
