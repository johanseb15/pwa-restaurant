import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Restaurant PWA',
  description: 'Order management PWA for restaurants.',
  manifest: '/manifest.json',
  themeColor: '#007AFF',
};

export default function RootLayout({
  children,
}: { 
  children: React.ReactNode;
}) {
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    checkAuth();
    // Optionally, set up an interval to check periodically
    const interval = setInterval(checkAuth, 60 * 1000); // Check every minute
    return () => clearInterval(interval);
  }, [checkAuth]);

  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <div className="fixed bottom-4 right-4">
          <a href="/cart" className="bg-blue-500 text-white p-4 rounded-full shadow-lg hover:bg-blue-600 transition-colors">
            View Cart
          </a>
        </div>
      </body>
    </html>
  );
}
