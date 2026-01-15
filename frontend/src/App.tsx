import { useState, useEffect } from 'react';

/**
 * Main Application Component
 * --------------------------
 * Currently performs a "Hello World" check against the Backend API.
 */
function App() {
  const [status, setStatus] = useState<string>('Checking backend connection...');

  useEffect(() => {
    // Simple fetch to verify Docker networking
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => setStatus(`Backend Status: ${data.status} | Service: ${data.service}`))
      .catch(err => setStatus(`Error connecting to backend: ${err.message}`));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>🚀 CertifyFlow Pilot</h1>
      <div style={{
        padding: '1rem',
        backgroundColor: '#f0f9ff',
        border: '1px solid #bae6fd',
        borderRadius: '8px',
        marginTop: '1rem'
      }}>
        <strong>System Diagnostic:</strong> {status}
      </div>
    </div>
  )
}

export default App