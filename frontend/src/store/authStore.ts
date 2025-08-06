import { create } from 'zustand';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  user: { id: string; username: string; role: string; restaurant_slug: string } | null;
  expiresAt: number | null; // Timestamp of token expiration
  login: (token: string, user: { id: string; username: string; role: string; restaurant_slug: string }, expiresIn: number) => void;
  logout: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  (set, get) => ({
    token: typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null,
    isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('admin_token') : false,
    user: typeof window !== 'undefined' && localStorage.getItem('admin_token') ? JSON.parse(localStorage.getItem('admin_user') || '{}') : null, // Parse stored user data
    expiresAt: typeof window !== 'undefined' ? parseInt(localStorage.getItem('admin_token_expiresAt') || '0') : null,
    login: (token, user, expiresIn) => {
      const expiresAt = Date.now() + expiresIn * 1000; // expiresIn is in seconds
      localStorage.setItem('admin_token', token);
      localStorage.setItem('admin_user', JSON.stringify(user));
      localStorage.setItem('admin_token_expiresAt', expiresAt.toString());
      set({ token, isAuthenticated: true, user, expiresAt });
    },
    logout: () => {
      localStorage.removeItem('admin_token');
      localStorage.removeItem('admin_user');
      localStorage.removeItem('admin_token_expiresAt');
      set({ token: null, isAuthenticated: false, user: null, expiresAt: null });
    },
    checkAuth: () => {
      const { token, expiresAt, logout } = get();
      if (token && expiresAt && Date.now() > expiresAt) {
        console.log("Token expired. Logging out.");
        logout();
      }
    },
  })
);
