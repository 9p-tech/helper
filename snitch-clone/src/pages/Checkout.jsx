import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { quickCheckout } from '../api';
import Button from '../components/Button';

const FALLBACK = 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80';

export default function Checkout() {
  const { cart, clearCart, loginUser } = useApp();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: '', full_name: '', whatsapp_number: '+91',
    line1: '', line2: '', city: '', state: '', pincode: '', phone: '+91',
  });
  const [coupon, setCoupon] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const subtotal = cart.reduce((sum, item) => sum + (Number(item.price) * item.quantity), 0);
  const shipping = subtotal >= 499 ? 0 : 49;
  const total = subtotal + shipping;

  const getImg = (item) => {
    const imgs = item.images ?? [];
    const primary = imgs.find((i) => i.is_primary) ?? imgs[0];
    return primary?.image || FALLBACK;
  };

  if (cart.length === 0) return (
    <div className="max-w-[1440px] mx-auto px-4 py-20 text-center">
      <h1 className="text-2xl font-bold mb-4">Your cart is empty</h1>
      <Button onClick={() => navigate('/shop')}>Return to Shop</Button>
    </div>
  );

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const wp = form.whatsapp_number.trim();
    if (!/^\+91\d{10}$/.test(wp)) {
      setError('WhatsApp number must be +91 followed by 10 digits.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        email: form.email.trim(),
        full_name: form.full_name.trim(),
        whatsapp_number: wp,
        address: {
          line1: form.line1.trim(),
          line2: form.line2.trim(),
          city: form.city.trim(),
          state: form.state.trim(),
          pincode: form.pincode.trim(),
          phone: form.phone.trim() || wp,
        },
        items: cart.map((item) => ({
          variant_id: Number(item.variantId),
          quantity: item.quantity,
        })),
        coupon_code: coupon.trim(),
      };

      const res = await quickCheckout(payload);
      const { order_id, total_amount, access, refresh } = res.data;

      if (access) loginUser(null, access, refresh);
      clearCart();
      navigate('/order-confirmation', { state: { orderId: order_id, total: Number(total_amount) } });
    } catch (err) {
      const data = err.response?.data;
      if (data?.errors) {
        setError(Object.entries(data.errors).map(([k, v]) => `${k}: ${v}`).join(' | '));
      } else if (data?.error) {
        setError(data.error);
      } else {
        setError('Something went wrong. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-8 md:py-16">
      <div className="flex flex-col lg:flex-row gap-8 lg:gap-16">
        <div className="flex-1 lg:max-w-[600px]">
          <h1 className="text-3xl font-heading font-extrabold tracking-tighter uppercase mb-8">Checkout</h1>

          <form onSubmit={handleSubmit} className="space-y-8">
            {error && (
              <div className="bg-snitch-red text-white p-4 text-sm font-bold">{error}</div>
            )}

            <div className="space-y-4">
              <h2 className="text-sm font-bold uppercase tracking-widest border-b border-snitch-border pb-2">Contact Information</h2>
              <input type="email" name="email" required placeholder="Email address"
                value={form.email} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              <input type="text" name="full_name" required placeholder="Full Name"
                value={form.full_name} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              <div>
                <input type="text" name="whatsapp_number" required placeholder="WhatsApp Number (+91...)"
                  value={form.whatsapp_number} onChange={handleChange}
                  className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
                <p className="text-[10px] text-snitch-muted mt-1 uppercase tracking-wider">Required for order updates & returns. Format: +91XXXXXXXXXX</p>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-sm font-bold uppercase tracking-widest border-b border-snitch-border pb-2">Shipping Address</h2>
              <input type="text" name="line1" required placeholder="Address Line 1"
                value={form.line1} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              <input type="text" name="line2" placeholder="Address Line 2 (Optional)"
                value={form.line2} onChange={handleChange}
                className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              <div className="grid grid-cols-3 gap-4">
                <input type="text" name="city" required placeholder="City"
                  value={form.city} onChange={handleChange}
                  className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
                <input type="text" name="state" required placeholder="State"
                  value={form.state} onChange={handleChange}
                  className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
                <input type="text" name="pincode" required placeholder="PIN Code"
                  value={form.pincode} onChange={handleChange}
                  className="w-full px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm" />
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-sm font-bold uppercase tracking-widest border-b border-snitch-border pb-2">Coupon Code</h2>
              <div className="flex gap-3">
                <input type="text" placeholder="Enter coupon code"
                  value={coupon} onChange={(e) => setCoupon(e.target.value)}
                  className="flex-1 px-4 py-3 border border-snitch-border bg-snitch-surface focus:outline-none focus:border-black text-sm uppercase" />
              </div>
            </div>

            <Button type="submit" className="w-full h-14" disabled={loading}>
              {loading ? 'Placing Order...' : `Place Order — ₹ ${total.toLocaleString('en-IN')}`}
            </Button>
          </form>
        </div>

        <div className="flex-1 bg-snitch-surface p-6 sm:p-8 border border-snitch-border self-start sticky top-24">
          <h2 className="text-lg font-heading font-extrabold uppercase tracking-widest mb-6 border-b border-snitch-border pb-4">
            Order Summary
          </h2>
          <div className="space-y-4 mb-6 max-h-[40vh] overflow-y-auto">
            {cart.map((item) => (
              <div key={item.variantId} className="flex gap-4">
                <div className="relative w-16 h-24 border border-snitch-border bg-white shrink-0">
                  <img src={getImg(item)} alt={item.name} className="w-full h-full object-cover"
                    onError={(e) => { e.target.src = FALLBACK; }} />
                  <span className="absolute -top-2 -right-2 bg-black text-white w-5 h-5 flex items-center justify-center rounded-full text-[10px] font-bold">
                    {item.quantity}
                  </span>
                </div>
                <div className="flex flex-col justify-center flex-1">
                  <p className="text-xs font-bold truncate pr-4">{item.name}</p>
                  <p className="text-[10px] text-snitch-muted uppercase tracking-wider">{item.size} / {item.color}</p>
                </div>
                <div className="flex items-center">
                  <p className="text-sm font-bold">₹ {(Number(item.price) * item.quantity).toLocaleString('en-IN')}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="border-t border-snitch-border pt-6 space-y-4 text-sm">
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
            <div className="flex justify-between border-t border-snitch-border pt-4 mt-4">
              <span className="font-bold uppercase tracking-widest">Total</span>
              <span className="text-xl font-bold">₹ {total.toLocaleString('en-IN')}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
