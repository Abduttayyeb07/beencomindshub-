import { useState, type FormEvent } from 'react';

/**
 * Shared-password sign-in.
 *
 * The password is exchanged for an HttpOnly session cookie, so it is never
 * stored in localStorage and script on the page cannot read the session.
 */
export default function LoginScreen(
  { onSignedIn, emailRequired }: { onSignedIn: () => void; emailRequired: boolean },
) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const incomplete = !password || (emailRequired && !email);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (busy || incomplete) return;
    setBusy(true);
    setError(null);
    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ email, password }),
      });
      if (res.ok) {
        setPassword('');
        onSignedIn();
        return;
      }
      const body = await res.json().catch(() => ({}));
      setError(body.detail || 'Could not sign in.');
    } catch {
      setError('Could not reach the server.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, display: 'flex',
      alignItems: 'center', justifyContent: 'center',
      background: '#0a0a13', color: '#e6e8ef',
      fontFamily: 'Inter, system-ui, sans-serif',
    }}>
      <form
        onSubmit={submit}
        style={{
          width: 320, display: 'flex', flexDirection: 'column', gap: 14,
          padding: 28, borderRadius: 12,
          background: '#11131d', border: '1px solid #232635',
        }}
      >
        <div style={{ fontSize: 18, fontWeight: 600, letterSpacing: '0.01em' }}>Cowork</div>
        {emailRequired && (
          <>
            <label htmlFor="cowork-email" style={{ fontSize: 13, color: '#9aa0b5' }}>
              Email
            </label>
            <input
              id="cowork-email"
              type="email"
              value={email}
              autoFocus
              autoComplete="username"
              onChange={(e) => setEmail(e.target.value)}
              style={{
                padding: '10px 12px', borderRadius: 8, fontSize: 14,
                background: '#0c0e16', color: '#e6e8ef',
                border: `1px solid ${error ? '#7c3244' : '#2a2e40'}`,
              }}
            />
          </>
        )}
        <label htmlFor="cowork-password" style={{ fontSize: 13, color: '#9aa0b5' }}>
          Password
        </label>
        <input
          id="cowork-password"
          type="password"
          value={password}
          autoFocus={!emailRequired}
          autoComplete="current-password"
          onChange={(e) => setPassword(e.target.value)}
          style={{
            padding: '10px 12px', borderRadius: 8, fontSize: 14,
            background: '#0c0e16', color: '#e6e8ef',
            border: `1px solid ${error ? '#7c3244' : '#2a2e40'}`,
          }}
        />
        {error && (
          <div role="alert" style={{ fontSize: 13, color: '#e6899a' }}>{error}</div>
        )}
        <button
          type="submit"
          disabled={busy || incomplete}
          style={{
            padding: '10px 12px', borderRadius: 8, fontSize: 14, fontWeight: 600,
            border: 'none', cursor: busy || incomplete ? 'default' : 'pointer',
            background: busy || incomplete ? '#2a2e40' : '#4c7dfd',
            color: busy || incomplete ? '#7a8099' : '#fff',
          }}
        >
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </div>
  );
}
