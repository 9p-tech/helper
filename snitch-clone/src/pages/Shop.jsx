import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getProducts, getCategories } from '../api';
import ProductCard from '../components/ProductCard';
import { ChevronDown, SlidersHorizontal } from 'lucide-react';

export default function Shop() {
  const [searchParams, setSearchParams] = useSearchParams();
  const categoryFilter = searchParams.get('category');

  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCategories().then((r) => setCategories(r.data.results ?? r.data));
  }, []);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (categoryFilter) params.category__slug = categoryFilter;
    getProducts(params)
      .then((r) => setProducts(r.data.results ?? r.data))
      .finally(() => setLoading(false));
  }, [categoryFilter]);

  return (
    <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-8 md:py-12">
      <div className="mb-8 border-b border-snitch-border pb-8">
        <div className="text-[10px] uppercase tracking-widest text-snitch-muted font-bold mb-4">
          Home / Shop {categoryFilter ? `/ ${categoryFilter}` : ''}
        </div>
        <div className="flex justify-between items-end">
          <h1 className="text-3xl md:text-5xl font-heading font-extrabold tracking-tighter uppercase">
            {categoryFilter || 'All Products'}
          </h1>
          <p className="text-sm text-snitch-muted">{products.length} items</p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <div className="md:hidden flex justify-between border border-snitch-border p-4">
          <span className="text-sm font-bold uppercase tracking-wider flex items-center gap-2">
            <SlidersHorizontal className="w-4 h-4" /> Filters
          </span>
          <ChevronDown className="w-4 h-4" />
        </div>

        <aside className="hidden md:block w-[250px] shrink-0">
          <div className="sticky top-24 space-y-8">
            <div className="border-b border-snitch-border pb-8">
              <h3 className="text-xs font-bold uppercase tracking-widest mb-4">Category</h3>
              <ul className="space-y-3">
                <li>
                  <button onClick={() => setSearchParams({})}
                    className={`text-sm ${!categoryFilter ? 'font-bold text-black' : 'text-snitch-muted hover:text-black'}`}>
                    All Products
                  </button>
                </li>
                {categories.map((cat) => (
                  <li key={cat.id}>
                    <button onClick={() => setSearchParams({ category: cat.slug })}
                      className={`text-sm ${categoryFilter === cat.slug ? 'font-bold text-black' : 'text-snitch-muted hover:text-black'}`}>
                      {cat.name}
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            <div className="border-b border-snitch-border pb-8">
              <h3 className="text-xs font-bold uppercase tracking-widest mb-4">Size</h3>
              <div className="flex flex-wrap gap-2">
                {['XS', 'S', 'M', 'L', 'XL', 'XXL'].map((size) => (
                  <button key={size} className="w-10 h-10 border border-snitch-border flex items-center justify-center text-xs font-bold hover:border-black transition-colors">
                    {size}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-xs font-bold uppercase tracking-widest mb-4">Price</h3>
              <div className="space-y-2">
                {['Under ₹ 1,000', '₹ 1,000 - ₹ 2,000', 'Over ₹ 2,000'].map((label) => (
                  <label key={label} className="flex items-center gap-3">
                    <input type="checkbox" className="w-4 h-4 border-snitch-border rounded-none focus:ring-0" />
                    <span className="text-sm text-snitch-muted">{label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </aside>

        <div className="flex-1">
          {loading ? (
            <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="border border-snitch-border animate-pulse">
                  <div className="aspect-[2/3] bg-snitch-surface" />
                  <div className="p-4 space-y-2">
                    <div className="h-3 bg-snitch-border rounded w-3/4" />
                    <div className="h-3 bg-snitch-border rounded w-1/4" />
                  </div>
                </div>
              ))}
            </div>
          ) : products.length > 0 ? (
            <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 border border-snitch-border bg-snitch-surface">
              <p className="text-snitch-muted">No products found.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
