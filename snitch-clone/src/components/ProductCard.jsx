import { Link } from 'react-router-dom';
import { useState } from 'react';

const CATEGORY_FALLBACKS = {
  'T-Shirts': [
    'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
    'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&q=80',
    'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&q=80',
    'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&q=80',
  ],
  'Shirts': [
    'https://images.unsplash.com/photo-1596755094514-f87e32f85e23?w=800&q=80',
    'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80',
    'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&q=80',
    'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=800&q=80',
  ],
  'Trousers': [
    'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80',
    'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800&q=80',
    'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&q=80',
    'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80',
  ],
};

const DEFAULT_FALLBACKS = [
  'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&q=80',
  'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80',
];

function getFallback(product) {
  const pool = CATEGORY_FALLBACKS[product.category_name] || DEFAULT_FALLBACKS;
  return pool[product.id % pool.length];
}

export default function ProductCard({ product }) {
  const [hovered, setHovered] = useState(false);

  // List API returns primary_image as a URL string (or null)
  // Detail API returns images[] array — handle both shapes
  const primaryUrl = product.primary_image
    || (Array.isArray(product.images) && product.images.length > 0
        ? (product.images.find((i) => i.is_primary) ?? product.images[0])?.image
        : null)
    || getFallback(product);

  const price = Number(product.discount_price ?? product.selling_price ?? product.base_price ?? product.price ?? 0);
  const original = product.base_price && product.discount_price ? Number(product.base_price) : null;
  const isOnSale = original && original > price;

  return (
    <Link
      to={`/product/${product.slug}`}
      className="group block border border-snitch-border"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="relative aspect-[2/3] overflow-hidden bg-snitch-surface border-b border-snitch-border">
        {isOnSale && (
          <span className="absolute top-2 left-2 z-10 px-2 py-1 text-[10px] font-bold uppercase tracking-wider bg-snitch-red text-white">
            SALE
          </span>
        )}
        <img
          src={hovered ? (getFallback({ ...product, id: (product.id ?? 0) + 1 }) ) : primaryUrl}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
          onError={(e) => { e.target.src = DEFAULT_FALLBACKS[0]; }}
        />
      </div>
      <div className="p-4 bg-white">
        <h3 className="text-sm font-bold truncate">{product.name}</h3>
        <div className="mt-2 flex items-center gap-2">
          <span className={`text-sm font-bold ${isOnSale ? 'text-snitch-red' : 'text-black'}`}>
            ₹ {price.toLocaleString('en-IN')}
          </span>
          {isOnSale && (
            <span className="text-xs text-snitch-muted line-through">
              ₹ {original.toLocaleString('en-IN')}
            </span>
          )}
        </div>
        {product.category_name && (
          <p className="text-[10px] text-snitch-muted uppercase tracking-wider mt-1">{product.category_name}</p>
        )}
      </div>
    </Link>
  );
}
