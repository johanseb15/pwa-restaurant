import React from 'react';
import { useCartStore } from '@/store/cartStore';
import CartItem from '@/components/CartItem';
import EmptyState from '@/components/EmptyState';

const CartPage: React.FC = () => {
  const cartItems = useCartStore((state) => state.items);
  const clearCart = useCartStore((state) => state.clearCart);
  const totalItems = useCartStore((state) => state.getTotalItems());
  const totalPrice = useCartStore((state) => state.getTotalPrice());

  if (cartItems.length === 0) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4">
        <EmptyState message="Your cart is empty." icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-12 h-12"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-1.653-1.806 47.949 47.949 0 0 0-9.919-1.009c-1.579-.665-3.162-.665-4.741 0M12 18.75a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" /></svg>} />
      </main>
    );
  }

  return (
    <main className="min-h-screen p-4">
      <h1 className="text-4xl font-bold text-center my-8">Your Cart</h1>
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow-lg">
        <div className="space-y-4">
          {cartItems.map((item) => (
            <CartItem key={item._id} item={item} />
          ))}
        </div>
        <div className="mt-6 pt-4 border-t border-gray-200 flex justify-between items-center">
          <span className="text-xl font-semibold">Total ({totalItems} items):</span>
          <span className="text-2xl font-bold text-blue-600">${totalPrice.toFixed(2)}</span>
        </div>
        <div className="mt-6 flex justify-end space-x-4">
          <button
            onClick={clearCart}
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-full font-medium transition-colors"
          >
            Clear Cart
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full font-medium transition-colors"
          >
            Proceed to Checkout
          </button>
        </div>
      </div>
    </main>
  );
};

export default CartPage;
