import { useState, useEffect } from 'react';
import { useAppStore } from '@/store/appStore';
import LoadingSpinner from '@/components/LoadingSpinner';
import EmptyState from '@/components/EmptyState';
import MenuItem from '@/components/MenuItem';
import MenuCategories from '@/components/MenuCategories';

interface Product {
  _id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category_id: string;
}

async function getProducts(categoryId: string | null = null): Promise<Product[]> {
  try {
    const url = categoryId && categoryId !== 'all' 
      ? `${process.env.NEXT_PUBLIC_API_URL}/products?category_id=${categoryId}`
      : `${process.env.NEXT_PUBLIC_API_URL}/products`;

    const res = await fetch(url);
    if (!res.ok) {
      console.error(`Failed to fetch products: ${res.status} ${res.statusText}`);
      throw new Error('Failed to fetch products');
    }
    return res.json();
  } catch (error) {
    console.error("Error fetching products:", error);
    throw error;
  }
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<string>('all');

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        const fetchedProducts = await getProducts(activeCategory);
        setProducts(fetchedProducts);
      } catch (err) {
        setError('Failed to load products. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [activeCategory]);

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4">
        <LoadingSpinner />
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4">
        <EmptyState category={activeCategory} />
      </main>
    );
  }

  if (products.length === 0) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4">
        <EmptyState category={activeCategory} />
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4">
      <h1 className="text-4xl font-bold text-center my-8">Our Menu</h1>
      <MenuCategories activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 w-full max-w-6xl">
        {products.map((product) => (
          <MenuItem key={product._id} item={product} />
        ))}
      </div>
    </main>
  );
}