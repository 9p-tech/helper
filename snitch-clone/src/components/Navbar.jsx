import { Link } from 'react-router-dom';
import { Search, User, ShoppingBag, Menu, LogOut } from 'lucide-react';
import { useApp } from '../context/AppContext';

export default function Navbar() {
  const { cart, user, logoutUser } = useApp();
  const cartCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-snitch-border">
      <div className="max-w-[1440px] mx-auto px-4 sm:px-8 h-16 flex items-center justify-between">

        <div className="flex items-center gap-6 flex-1">
          <button className="md:hidden"><Menu className="w-6 h-6" /></button>
          <div className="hidden md:flex items-center gap-6">
            <Link to="/shop" className="text-xs font-bold tracking-widest uppercase hover:border-b border-black py-1">New Arrivals</Link>
            <Link to="/shop?category=shirts" className="text-xs font-bold tracking-widest uppercase hover:border-b border-black py-1">Shirts</Link>
            <Link to="/shop?category=t-shirts" className="text-xs font-bold tracking-widest uppercase hover:border-b border-black py-1">T-Shirts</Link>
            <Link to="/shop?category=trousers" className="text-xs font-bold tracking-widest uppercase hover:border-b border-black py-1">Trousers</Link>
          </div>
        </div>

        <div className="flex-1 text-center flex justify-center">
          <Link to="/" className="text-2xl font-heading font-extrabold tracking-tighter">SNITCH</Link>
        </div>

        <div className="flex items-center justify-end gap-4 sm:gap-6 flex-1">
          <button><Search className="w-5 h-5" /></button>
          {user ? (
            <div className="hidden sm:flex items-center gap-3">
              <span className="text-xs font-bold text-snitch-muted truncate max-w-[100px]">
                {user.profile?.full_name || user.email?.split('@')[0]}
              </span>
              <button onClick={logoutUser} title="Sign out">
                <LogOut className="w-5 h-5 text-snitch-muted hover:text-snitch-red transition-colors" />
              </button>
            </div>
          ) : (
            <Link to="/login" className="hidden sm:block">
              <User className="w-5 h-5" />
            </Link>
          )}
          <Link to="/cart" className="relative">
            <ShoppingBag className="w-5 h-5" />
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-2 bg-snitch-red text-white text-[10px] font-bold w-4 h-4 flex items-center justify-center rounded-full">
                {cartCount}
              </span>
            )}
          </Link>
        </div>
      </div>
    </nav>
  );
}
