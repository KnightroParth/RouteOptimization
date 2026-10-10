import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MapPin, Brain, Route, Shield, Zap, BarChart3 } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (role) => {
    if (role === 'mr') {
      setEmail('mr@demo.com');
      setPassword('demo123');
    } else {
      setEmail('manager@demo.com');
      setPassword('demo123');
    }
  };

  const features = [
    { icon: <Brain size={16} />, text: 'AI-powered visit priority prediction' },
    { icon: <Route size={16} />, text: 'OR-Tools optimized daily routes' },
    { icon: <MapPin size={16} />, text: 'Interactive route visualization' },
    { icon: <BarChart3 size={16} />, text: 'Performance analytics dashboards' },
    { icon: <Zap size={16} />, text: 'Time-window aware scheduling' },
    { icon: <Shield size={16} />, text: 'Role-based access control' },
  ];

  return (
    <div className="login-page">
      <div className="login-left">
        <div style={{ marginBottom: 28 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24 }}>
            <div style={{
              width: 36, height: 36, borderRadius: 8,
              background: '#fafafa', color: '#09090b',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <MapPin size={20} />
            </div>
            <span style={{ fontSize: 12, fontWeight: 500, color: '#71717a', letterSpacing: 0.5 }}>
              MR Route Optimization
            </span>
          </div>
          <h1>
            Visit Planning &<br />
            <span>Route Optimization</span>
          </h1>
          <p>
            Intelligent prioritization of medical representative visits using
            Machine Learning, with optimized daily routes via OR-Tools.
          </p>
        </div>

        <div className="login-features">
          {features.map((f, i) => (
            <div className="login-feature" key={i}>
              <div className="login-feature-icon">{f.icon}</div>
              {f.text}
            </div>
          ))}
        </div>
      </div>

      <div className="login-right">
        <div className="login-card">
          <h2>Sign in</h2>
          <p>Enter your credentials to access your account</p>

          {error && <div className="login-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input
                id="login-email"
                type="email"
                className="form-input"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                id="login-password"
                type="password"
                className="form-input"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button id="login-submit" type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <><span className="spinner light" /> Signing in...</> : 'Sign in'}
            </button>
          </form>

          <div className="separator" />

          <p style={{ fontSize: 13, color: '#71717a', marginBottom: 8, textAlign: 'center' }}>
            Quick access with demo accounts
          </p>
          <div style={{ display: 'flex', gap: 8 }}>
            <button type="button" className="btn btn-outline btn-sm" onClick={() => fillDemo('mr')} style={{ flex: 1 }}>
              MR Login
            </button>
            <button type="button" className="btn btn-outline btn-sm" onClick={() => fillDemo('manager')} style={{ flex: 1 }}>
              Manager Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
