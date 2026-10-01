import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { apiFetch } from '../services/api';
import { User } from '../types';

type AuthContextValue = {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  ready: boolean;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('socialflow_token'));
  const [user, setUser] = useState<User | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!token) {
      setReady(true);
      setUser(null);
      return;
    }

    apiFetch<User>('/auth/me', {}, token)
      .then((me) => setUser(me))
      .catch(() => {
        localStorage.removeItem('socialflow_token');
        setToken(null);
        setUser(null);
      })
      .finally(() => setReady(true));
  }, [token]);

  const value = useMemo<AuthContextValue>(() => ({
    user,
    token,
    ready,
    async login(email: string, password: string) {
      const authResponse = await apiFetch<{ access_token: string; token_type: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      localStorage.setItem('socialflow_token', authResponse.access_token);
      setToken(authResponse.access_token);
    },
    async register(name: string, email: string, password: string) {
      await apiFetch<{ id: number }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      });
    },
    logout() {
      localStorage.removeItem('socialflow_token');
      setToken(null);
      setUser(null);
    },
  }), [ready, token, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
