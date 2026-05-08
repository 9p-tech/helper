import { useLocation, Link, Navigate } from 'react-router-dom';
import Button from '../components/Button';
import { CheckCircle } from 'lucide-react';

export default function OrderConfirmation() {
  const location = useLocation();
  const { orderId, total } = location.state || {};

  if (!orderId) {
    return <Navigate to="/" />;
  }

  return (
    <div className="max-w-[1440px] mx-auto px-4 py-20 min-h-[70vh] flex flex-col items-center justify-center">
      <div className="max-w-[600px] w-full bg-snitch-surface border border-snitch-border p-8 md:p-12 text-center">
        <CheckCircle className="w-16 h-16 mx-auto mb-6 text-black" />
        
        <h1 className="text-3xl md:text-4xl font-heading font-extrabold uppercase tracking-tighter mb-4">
          Order Confirmed
        </h1>
        <p className="text-sm text-snitch-muted mb-8">
          Thank you for your purchase. We've received your order and are getting it ready to ship. You will receive an email and a WhatsApp message with tracking details once it's on the way.
        </p>

        <div className="bg-white border border-snitch-border p-6 mb-8">
          <p className="text-xs font-bold uppercase tracking-widest text-snitch-muted mb-2">Order ID</p>
          {/* MASSIVE PROMINENT ORDER ID DISPLAY */}
          <div className="text-4xl md:text-6xl font-heading font-extrabold tracking-tighter text-black py-4 break-words">
            {orderId}
          </div>
          <div className="border-t border-snitch-border mt-4 pt-4 flex justify-between items-center text-sm">
            <span className="font-bold text-snitch-muted uppercase tracking-widest">Amount Paid</span>
            <span className="font-bold">₹ {total?.toLocaleString('en-IN')}</span>
          </div>
        </div>

        <Link to="/shop">
          <Button className="w-full h-14">Continue Shopping</Button>
        </Link>
      </div>
    </div>
  );
}
