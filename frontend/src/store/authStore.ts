import { create } from 'zustand';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  user: { username: string; role: string } | null;
  login: (token: string, username: string, role: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null,
  isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('admin_token') : false,
  user: typeof window !== 'undefined' && localStorage.getItem('admin_token') ? { username: 'admin', role: 'admin' } : null, // Mock user for now
  login: (token, username, role) => {
    localStorage.setItem('admin_token', token);
    set({ token, isAuthenticated: true, user: { username, role } });
  },
  logout: () => {
    localStorage.removeItem('admin_token');
    set({ token: null, isAuthenticated: false, user: null });
  },
}));
