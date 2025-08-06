import create from 'zustand';
import api from '../services/api';

const useAppStore = create((set) => ({
  cart: [],
  user: null,
  isAuthenticated: false,
  loading: true,

  setCart: (cart) => set({ cart }),

  addToCart: (item, quantity) => {
    set((state) => {
      const existingItem = state.cart.find((cartItem) => cartItem.id === item.id);
      if (existingItem) {
        return {
          cart: state.cart.map((cartItem) =>
            cartItem.id === item.id ? { ...cartItem, quantity: cartItem.quantity + quantity } : cartItem
          ),
        };
      } else {
        return { cart: [...state.cart, { ...item, quantity }] };
      }
    });
  },

  login: async (userData) => {
    try {
      const res = await api.post('/auth/login', userData);
      const { token } = res.data;
      localStorage.setItem('token', token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const userRes = await api.get('/auth/verify');
      set({ user: userRes.data, isAuthenticated: true });
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const res = await api.get('/auth/verify');
        set({ user: res.data, isAuthenticated: true, loading: false });
      } else {
        set({ loading: false });
      }
    } catch (err) {
      console.error(err);
      set({ loading: false });
    }
  },
}));

export { useAppStore };
