import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { login, register } from '../api';
import Button from '../components/Button';

export default function Login() {
  const { loginUser } = useApp();
  const navigate = useNavigate();
  const [mode, setMode] = useState('login'); // 'login' | 'register'
  const [form, setForm] = useState({ email: '', password: '', username: '', full_name: '', whatsapp_number: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      let res;
      if (mode === 'login') {
        res = await login({ email: form.email, password: form.password });
        loginUser(res.data.user, res.data.access, res.data.refresh);
      } else {
        if (!form.username) { setError('Username is required'); setLoading(false); return; }
        res = await register({
          email: form.email,
          password: form.password,
          username: form.username,
          full_name: form.full_name,
          whatsapp_number: form.whatsapp_number,
        });
        // After register, log in
        const loginRes = await login({ email: form.email, password: form.password });
        loginUser(loginRes.data.user, loginRes.data.access, loginRes.data.refresh);
      }
      navigate('/');
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const msg = typeof data === 'string' ? data
          : Object.values(data).flat().join(' ');
        setError(msg);
      } else {
        setError('Something went wrong. Try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1440px] mx-auto px-4 py-20 min-h-[70vh] flex flex-col items-center justify-center">
      <div className="w-full max-w-[400px]">
        <h1 className="text-3xl font-heading font-extrabold tracking-tighter uppercase mb-2 text-center">
          {mode === 'login' ? 'Sign In' : 'Create Account'}
        </h1>
        <p className="text-sm text-snitch-muted mb-8 text-center">
          {mode === 'login' ? 'Enter your details to sign in.' : 'Join Snitch for exclusive drops.'}
        </p>

        {error && (
          <div className="bg-snitch-red text-white p-3 text-sm font-bold mb-4">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'register' && (
            <>
              <input type="text" name="username" placeholder="Username" required
                value={form.username} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              <input type="text" name="full_name" placeholder="Full Name"
                value={form.full_name} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              <input type="text" name="whatsapp_number" placeholder="WhatsApp (+91...)"
                value={form.whatsapp_number} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
            </>
          )}
          <input type="email" name="email" placeholder="Email" required
            value={form.email} onChange={handleChange}
            className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
          <input type="password" name="password" placeholder="Password" required
            value={form.password} onChange={handleChange}
            className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
          <Button type="submit" className="w-full h-14 mt-2" disabled={loading}>
            {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </Button>
        </form>

        <div className="mt-8 pt-8 border-t border-snitch-border text-center">
          <p className="text-sm text-snitch-muted mb-4">
            {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
          </p>
          <Button variant="outline" className="w-full h-14"
            onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError(''); }}>
            {mode === 'login' ? 'Create Account' : 'Sign In'}
          </Button>
        </div>
      </div>
    </div>
  );
}
