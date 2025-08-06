import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface ProductInCart {
  _id: string;
  name: string;
  price: number;
  image: string;
  quantity: number;
}

interface CartState {
  items: ProductInCart[];
  addItem: (product: Omit<ProductInCart, 'quantity'>) => void;
  removeItem: (productId: string) => void;
  updateItemQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
  getTotalItems: () => number;
  getTotalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (product) => {
        set((state) => {
          const existingItem = state.items.find((item) => item._id === product._id);
          if (existingItem) {
            return {
              items: state.items.map((item) =>
                item._id === product._id ? { ...item, quantity: item.quantity + 1 } : item
              ),
            };
          } else {
            return {
              items: [...state.items, { ...product, quantity: 1 }],
            };
          }
        });
      },
      removeItem: (productId) => {
        set((state) => ({
          items: state.items.filter((item) => item._id !== productId),
        }));
      },
      updateItemQuantity: (productId, quantity) => {
        set((state) => ({
          items: state.items.map((item) =>
            item._id === productId ? { ...item, quantity: quantity } : item
          ),
        }));
      },
      clearCart: () => set({ items: [] }),
      getTotalItems: () => get().items.reduce((total, item) => total + item.quantity, 0),
      getTotalPrice: () => get().items.reduce((total, item) => total + item.price * item.quantity, 0),
    }),
    {
      name: 'cart-storage', // unique name
      storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
    }
  )
);
