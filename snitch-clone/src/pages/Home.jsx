import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getProducts, getCategories } from '../api';
import ProductCard from '../components/ProductCard';

const HERO = 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=2000&q=80';
const CAT_IMAGES = {
  'T-Shirts': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80',
  'Shirts':   'https://images.unsplash.com/photo-1596755094514-f87e32f85e23?w=600&q=80',
  'Trousers': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&q=80',
  'default':  'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&q=80',
};

export default function Home() {
  const [featured, setFeatured] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    getProducts({ is_featured: true, page_size: 4 })
      .then((r) => setFeatured((r.data.results ?? r.data).slice(0, 4)));
    getCategories()
      .then((r) => setCategories(r.data.results ?? r.data));
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero */}
      <section className="relative h-[80vh] w-full overflow-hidden">
        <img src={HERO} alt="Hero" className="absolute inset-0 w-full h-full object-cover" />
        <div className="absolute inset-0 bg-black/20" />
        <div className="absolute inset-0 flex flex-col items-center justify-center text-white p-4">
          <h2 className="text-xs font-bold tracking-[0.2em] mb-4 uppercase">Summer 25 Collection</h2>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-heading font-extrabold tracking-tighter text-center mb-8">
            THE NEW STANDARD
          </h1>
          <Link to="/shop"
            className="px-8 py-4 bg-white text-black text-xs font-bold uppercase tracking-wider hover:bg-snitch-surface transition-colors">
            Shop Men
          </Link>
        </div>
      </section>

      {/* Categories */}
      <section className="py-20 px-4 sm:px-8 max-w-[1440px] mx-auto w-full border-t border-snitch-border">
        <div className="flex justify-between items-end mb-10">
          <h2 className="text-3xl font-heading font-extrabold tracking-tighter uppercase">Shop by Category</h2>
          <Link to="/shop" className="text-xs font-bold tracking-widest uppercase border-b border-black pb-1 hover:text-snitch-muted hover:border-snitch-muted transition-colors">
            View All
          </Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
          {(categories.length > 0 ? categories : [
            { slug: 't-shirts', name: 'T-Shirts' },
            { slug: 'shirts', name: 'Shirts' },
            { slug: 'trousers', name: 'Trousers' },
          ]).map((cat) => (
            <Link key={cat.slug} to={`/shop?category=${cat.slug}`}
              className="group block relative aspect-[3/4] overflow-hidden border border-snitch-border">
              <img
                src={cat.image || CAT_IMAGES[cat.name] || CAT_IMAGES.default}
                alt={cat.name}
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-6">
                <span className="text-white font-bold text-lg uppercase tracking-wider">{cat.name}</span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* New Arrivals */}
      <section className="py-20 px-4 sm:px-8 bg-snitch-surface border-t border-b border-snitch-border">
        <div className="max-w-[1440px] mx-auto w-full">
          <div className="flex justify-between items-end mb-10">
            <h2 className="text-3xl font-heading font-extrabold tracking-tighter uppercase">New Arrivals</h2>
            <Link to="/shop" className="text-xs font-bold tracking-widest uppercase border-b border-black pb-1 hover:text-snitch-muted hover:border-snitch-muted transition-colors">
              Shop New
            </Link>
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            {featured.length > 0
              ? featured.map((p) => <ProductCard key={p.id} product={p} />)
              : [...Array(4)].map((_, i) => (
                  <div key={i} className="border border-snitch-border animate-pulse">
                    <div className="aspect-[2/3] bg-snitch-surface" />
                    <div className="p-4 space-y-2">
                      <div className="h-3 bg-snitch-border rounded w-3/4" />
                      <div className="h-3 bg-snitch-border rounded w-1/4" />
                    </div>
                  </div>
                ))
            }
          </div>
        </div>
      </section>

      {/* Promo Banner */}
      <section className="h-[60vh] relative overflow-hidden bg-black flex items-center justify-center">
        <div className="absolute inset-0 opacity-50 bg-[url('https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=2000&q=80')] bg-cover bg-center mix-blend-overlay" />
        <div className="relative z-10 text-center px-4">
          <h2 className="text-4xl md:text-5xl font-heading font-extrabold text-white tracking-tighter uppercase mb-6">
            Redefining Basics
          </h2>
          <Link to="/shop"
            className="inline-block px-8 py-4 bg-white text-black text-xs font-bold uppercase tracking-wider hover:bg-snitch-surface transition-colors border-2 border-white">
            Discover the Collection
          </Link>
        </div>
      </section>
    </div>
  );
}
