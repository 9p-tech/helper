import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { getProduct } from '../api';
import { useApp } from '../context/AppContext';
import Button from '../components/Button';
import { ChevronRight, Truck, RefreshCw } from 'lucide-react';

// Category-specific fallback images (same pool as ProductCard)
const CAT_IMAGES = {
  'T-Shirts': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
  'Shirts':   'https://images.unsplash.com/photo-1596755094514-f87e32f85e23?w=800&q=80',
  'Trousers': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80',
};
const FALLBACK = 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&q=80';

export default function ProductDetail() {
  const { id: slug } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useApp();

  // ── ALL HOOKS MUST BE AT THE TOP — never after an early return ──
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [imageIdx, setImageIdx] = useState(0);

  useEffect(() => {
    setLoading(true);
    setSelectedVariant(null);
    setSelectedColor(null);
    setImageIdx(0);
    getProduct(slug)
      .then((r) => setProduct(r.data))
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false));
  }, [slug]);

  // ── Early returns AFTER all hooks ──
  if (loading) {
    return (
      <div className="max-w-[1440px] mx-auto p-8 flex gap-8 animate-pulse">
        <div className="w-2/3 aspect-[3/4] bg-snitch-surface rounded" />
        <div className="w-1/3 space-y-4 pt-4">
          <div className="h-6 bg-snitch-border rounded w-3/4" />
          <div className="h-8 bg-snitch-border rounded w-1/2" />
          <div className="h-4 bg-snitch-border rounded w-full" />
          <div className="h-4 bg-snitch-border rounded w-2/3" />
        </div>
      </div>
    );
  }

  if (notFound || !product) {
    return <div className="text-center py-20 text-snitch-muted">Product not found.</div>;
  }

  // ── Derived values (computed after data is available) ──
  const images = product.images ?? [];
  const catName = product.category?.name ?? '';
  const catFallback = CAT_IMAGES[catName] || FALLBACK;
  const currentImg = images[imageIdx]?.image || catFallback;

  const price = Number(product.discount_price ?? product.base_price ?? 0);
  const original = product.base_price && product.discount_price ? Number(product.base_price) : null;
  const isOnSale = original && original > price;

  // Group variants by color
  const colorMap = {};
  (product.variants ?? []).forEach((v) => {
    if (!colorMap[v.color]) colorMap[v.color] = [];
    colorMap[v.color].push(v);
  });
  const colors = Object.keys(colorMap);
  const sizesForColor = selectedColor ? (colorMap[selectedColor] ?? []) : (product.variants ?? []);

  const handleAddToCart = () => {
    if (!selectedVariant) { alert('Please select a size'); return; }
    if (selectedVariant.stock < 1) { alert('Out of stock'); return; }
    addToCart(
      { id: product.id, name: product.name, slug: product.slug, price, images },
      selectedVariant.size,
      selectedVariant.color,
      selectedVariant.id,
    );
    navigate('/cart');
  };

  return (
    <div className="max-w-[1440px] mx-auto">
      {/* Breadcrumb */}
      <div className="px-4 sm:px-8 py-4 border-b border-snitch-border">
        <div className="text-[10px] uppercase tracking-widest text-snitch-muted font-bold flex items-center gap-2">
          <span>Home</span><ChevronRight className="w-3 h-3" />
          <span>Shop</span><ChevronRight className="w-3 h-3" />
          <span className="text-black">{product.name}</span>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row border-b border-snitch-border">
        {/* Image gallery */}
        <div className="w-full lg:w-2/3 flex flex-col md:flex-row border-r border-snitch-border">
          {/* Thumbnails */}
          {images.length > 1 && (
            <div className="hidden md:flex flex-col gap-4 p-4 w-24 shrink-0 border-r border-snitch-border">
              {images.map((img, i) => (
                <button key={i} onClick={() => setImageIdx(i)}
                  className={`aspect-[2/3] border overflow-hidden ${imageIdx === i ? 'border-black' : 'border-snitch-border'}`}>
                  <img src={img.image || catFallback} alt="" className="w-full h-full object-cover"
                    onError={(e) => { e.target.src = catFallback; }} />
                </button>
              ))}
            </div>
          )}

          {/* Main image */}
          <div className="w-full bg-snitch-surface relative aspect-[3/4] md:aspect-auto min-h-[400px]">
            <img src={currentImg} alt={product.name}
              className="absolute inset-0 w-full h-full object-cover object-top"
              onError={(e) => { e.target.src = catFallback; }} />
          </div>
        </div>

        {/* Product info */}
        <div className="w-full lg:w-1/3 p-6 sm:p-10 flex flex-col">
          {catName && (
            <span className="text-[10px] font-bold uppercase tracking-widest text-snitch-muted mb-2">{catName}</span>
          )}

          <h1 className="text-3xl font-heading font-extrabold tracking-tighter uppercase mb-4">
            {product.name}
          </h1>

          <div className="flex items-center gap-3 mb-8 pb-8 border-b border-snitch-border">
            <span className={`text-2xl font-bold ${isOnSale ? 'text-snitch-red' : 'text-black'}`}>
              ₹ {price.toLocaleString('en-IN')}
            </span>
            {isOnSale && (
              <span className="text-lg text-snitch-muted line-through">
                ₹ {original.toLocaleString('en-IN')}
              </span>
            )}
            {isOnSale && original && (
              <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1">
                {Math.round((1 - price / original) * 100)}% OFF
              </span>
            )}
          </div>

          {/* Color selector */}
          {colors.length > 0 && (
            <div className="mb-6">
              <span className="text-xs font-bold uppercase tracking-widest block mb-3">
                Color{selectedColor ? `: ${selectedColor}` : ''}
              </span>
              <div className="flex flex-wrap gap-2">
                {colors.map((color) => {
                  const hex = colorMap[color][0]?.color_hex ?? '#888';
                  const isSelected = selectedColor === color;
                  return (
                    <button key={color} onClick={() => { setSelectedColor(color); setSelectedVariant(null); }}
                      title={color}
                      className={`w-9 h-9 rounded-full border-2 transition-all ${isSelected ? 'border-black ring-2 ring-offset-1 ring-black' : 'border-snitch-border'}`}
                      style={{ backgroundColor: hex }} />
                  );
                })}
              </div>
            </div>
          )}

          {/* Size selector */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <span className="text-xs font-bold uppercase tracking-widest">Select Size</span>
              {!selectedVariant && (
                <span className="text-[10px] text-snitch-red uppercase tracking-wider">Required</span>
              )}
            </div>
            {sizesForColor.length === 0 ? (
              <p className="text-sm text-snitch-muted">No variants available.</p>
            ) : (
              <div className="flex flex-wrap gap-3">
                {sizesForColor.map((v) => {
                  const isSelected = selectedVariant?.id === v.id;
                  const outOfStock = v.stock === 0;
                  return (
                    <button key={v.id} onClick={() => !outOfStock && setSelectedVariant(v)}
                      disabled={outOfStock}
                      title={outOfStock ? 'Out of stock' : `${v.size} – ${v.stock} left`}
                      className={`relative w-14 h-14 border flex items-center justify-center text-sm font-bold transition-colors
                        ${outOfStock
                          ? 'opacity-30 cursor-not-allowed border-snitch-border line-through'
                          : isSelected
                            ? 'border-black bg-black text-white'
                            : 'border-snitch-border hover:border-black'
                        }`}>
                      {v.size}
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          <Button onClick={handleAddToCart} className="w-full mb-6 h-14 text-sm">
            Add to Cart
          </Button>

          {product.description && (
            <p className="text-sm text-snitch-muted mb-6 leading-relaxed">{product.description}</p>
          )}

          {product.material && (
            <p className="text-xs text-snitch-muted mb-2">
              <span className="font-bold uppercase tracking-widest text-black">Material: </span>{product.material}
            </p>
          )}

          {product.care_instructions && (
            <p className="text-xs text-snitch-muted mb-6">
              <span className="font-bold uppercase tracking-widest text-black">Care: </span>{product.care_instructions}
            </p>
          )}

          <div className="mt-auto space-y-4 pt-8 border-t border-snitch-border">
            <div className="flex items-center gap-3 text-sm text-snitch-muted">
              <Truck className="w-5 h-5 shrink-0 text-black" />
              <span>Free shipping on orders over ₹499</span>
            </div>
            <div className="flex items-center gap-3 text-sm text-snitch-muted">
              <RefreshCw className="w-5 h-5 shrink-0 text-black" />
              <span>7-day replacement via WhatsApp bot</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
