import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="border-t border-snitch-border bg-white pt-16 pb-8">
      <div className="max-w-[1440px] mx-auto px-4 sm:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <div>
            <h3 className="text-xl font-heading font-extrabold tracking-tighter mb-4">SNITCH</h3>
            <p className="text-sm text-snitch-muted leading-relaxed">
              Premium fashion for the modern individual. Quality basics, elevated design.
            </p>
          </div>
          
          <div>
            <h4 className="font-bold text-sm mb-4 uppercase tracking-wider">Shop</h4>
            <ul className="space-y-3">
              <li><Link to="/shop?category=New" className="text-sm text-snitch-muted hover:text-black transition-colors">New Arrivals</Link></li>
              <li><Link to="/shop?category=Shirts" className="text-sm text-snitch-muted hover:text-black transition-colors">Shirts</Link></li>
              <li><Link to="/shop?category=T-Shirts" className="text-sm text-snitch-muted hover:text-black transition-colors">T-Shirts</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-sm mb-4 uppercase tracking-wider">Help</h4>
            <ul className="space-y-3">
              <li><Link to="#" className="text-sm text-snitch-muted hover:text-black transition-colors">Track Order</Link></li>
              <li><Link to="#" className="text-sm text-snitch-muted hover:text-black transition-colors">Returns & Exchanges</Link></li>
              <li><Link to="#" className="text-sm text-snitch-muted hover:text-black transition-colors">Customer Service</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-sm mb-4 uppercase tracking-wider">Stay in touch</h4>
            <div className="flex border border-snitch-border rounded-none focus-within:border-black transition-colors">
              <input 
                type="email" 
                placeholder="Enter your email" 
                className="w-full px-4 py-3 text-sm focus:outline-none bg-snitch-surface"
              />
              <button className="px-6 py-3 bg-black text-white text-xs font-bold uppercase tracking-wider hover:bg-opacity-90">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        <div className="border-t border-snitch-border pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs text-snitch-muted">&copy; 2026 SNITCH CLONE. All rights reserved.</p>
          <div className="flex gap-4">
            <Link to="#" className="text-xs text-snitch-muted hover:text-black">Privacy Policy</Link>
            <Link to="#" className="text-xs text-snitch-muted hover:text-black">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
