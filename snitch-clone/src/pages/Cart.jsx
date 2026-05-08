import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import Button from '../components/Button';
import { Trash2, Plus, Minus } from 'lucide-react';

const FALLBACK = 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80';

export default function Cart() {
  const { cart, removeFromCart, updateQuantity } = useApp();
  const navigate = useNavigate();

  const subtotal = cart.reduce((sum, item) => sum + (Number(item.price) * item.quantity), 0);
  const shipping = subtotal >= 499 ? 0 : 49;
  const total = subtotal + shipping;

  const getImg = (item) => {
    const imgs = item.images ?? [];
    const primary = imgs.find((i) => i.is_primary) ?? imgs[0];
    return primary?.image || FALLBACK;
  };

  if (cart.length === 0) return (
    <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-20 min-h-[60vh] flex flex-col items-center justify-center">
      <h1 className="text-3xl font-heading font-extrabold tracking-tighter uppercase mb-6">Your Cart is Empty</h1>
      <p className="text-snitch-muted mb-8 text-center max-w-md">Add something amazing to get started.</p>
      <Link to="/shop"><Button>Start Shopping</Button></Link>
    </div>
  );

  return (
    <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-8 md:py-16">
      <h1 className="text-3xl md:text-5xl font-heading font-extrabold tracking-tighter uppercase mb-8 md:mb-12 border-b border-snitch-border pb-8">
        Shopping Cart
      </h1>

      <div className="flex flex-col lg:flex-row gap-8 lg:gap-16">
        <div className="flex-1">
          <div className="hidden md:grid grid-cols-12 gap-4 border-b border-snitch-border pb-4 mb-4 text-xs font-bold uppercase tracking-widest text-snitch-muted">
            <div className="col-span-6">Product</div>
            <div className="col-span-3 text-center">Quantity</div>
            <div className="col-span-3 text-right">Total</div>
          </div>

          <div className="space-y-6">
            {cart.map((item) => (
              <div key={item.variantId} className="flex flex-col md:grid md:grid-cols-12 gap-4 border-b border-snitch-border pb-6">
                <div className="col-span-6 flex gap-4">
                  <div className="w-24 h-36 shrink-0 border border-snitch-border bg-snitch-surface">
                    <img src={getImg(item)} alt={item.name}
                      className="w-full h-full object-cover"
                      onError={(e) => { e.target.src = FALLBACK; }} />
                  </div>
                  <div className="flex flex-col justify-between py-1">
                    <div>
                      <Link to={`/product/${item.slug}`} className="text-sm font-bold block mb-1 hover:underline">
                        {item.name}
                      </Link>
                      <p className="text-sm text-snitch-muted mb-1">Size: {item.size} / {item.color}</p>
                      <p className="text-sm font-bold md:hidden">₹ {Number(item.price).toLocaleString('en-IN')}</p>
                    </div>
                    <button onClick={() => removeFromCart(item.variantId)}
                      className="text-xs text-snitch-muted hover:text-snitch-red flex items-center gap-1 self-start">
                      <Trash2 className="w-3 h-3" /> Remove
                    </button>
                  </div>
                </div>

                <div className="col-span-3 flex items-center justify-start md:justify-center">
                  <div className="flex items-center border border-snitch-border h-10 w-32">
                    <button onClick={() => updateQuantity(item.variantId, item.quantity - 1)}
                      className="w-10 h-full flex items-center justify-center hover:bg-snitch-surface">
                      <Minus className="w-3 h-3" />
                    </button>
                    <span className="flex-1 text-center text-sm font-bold">{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.variantId, item.quantity + 1)}
                      className="w-10 h-full flex items-center justify-center hover:bg-snitch-surface">
                      <Plus className="w-3 h-3" />
                    </button>
                  </div>
                </div>

                <div className="col-span-3 hidden md:flex items-center justify-end">
                  <span className="text-sm font-bold">
                    ₹ {(Number(item.price) * item.quantity).toLocaleString('en-IN')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="w-full lg:w-[400px] shrink-0">
          <div className="bg-snitch-surface border border-snitch-border p-6 md:p-8">
            <h2 className="text-lg font-heading font-extrabold uppercase tracking-widest mb-6 border-b border-snitch-border pb-4">
              Order Summary
            </h2>
            <div className="space-y-4 mb-6 text-sm">
              <div className="flex justify-between">
                <span className="text-snitch-muted">Subtotal</span>
                <span className="font-bold">₹ {subtotal.toLocaleString('en-IN')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-snitch-muted">Shipping</span>
                <span className={`font-bold ${shipping === 0 ? 'text-green-600' : ''}`}>
                  {shipping === 0 ? 'Free' : `₹ ${shipping}`}
                </span>
              </div>
            </div>
            <div className="flex justify-between items-center mb-8 border-t border-snitch-border pt-4">
              <span className="font-bold uppercase tracking-widest">Total</span>
              <span className="text-2xl font-bold">₹ {total.toLocaleString('en-IN')}</span>
            </div>
            <Button onClick={() => navigate('/checkout')} className="w-full h-14">
              Proceed to Checkout
            </Button>
            <div className="mt-4 text-center">
              <Link to="/shop" className="text-xs text-snitch-muted underline hover:text-black">
                Continue Shopping
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
