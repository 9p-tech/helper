import { createContext, useContext, useState, useEffect } from 'react';
import { getMe } from '../api';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [cart, setCart] = useState(() => {
    try { return JSON.parse(localStorage.getItem('cart') || '[]'); } catch { return []; }
  });
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Persist cart to localStorage
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  // Restore session on load
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      getMe()
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => setAuthLoading(false));
    } else {
      setAuthLoading(false);
    }
  }, []);

  const loginUser = (userData, access, refresh) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    setUser(userData);
  };

  const logoutUser = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  const addToCart = (product, size, color, variantId, quantity = 1) => {
    setCart((prev) => {
      const key = `${variantId}`;
      const existing = prev.find((item) => item.variantId === key);
      if (existing) {
        return prev.map((item) =>
          item.variantId === key ? { ...item, quantity: item.quantity + quantity } : item
        );
      }
      return [...prev, { ...product, size, color, variantId: key, quantity }];
    });
  };

  const removeFromCart = (variantId) => {
    setCart((prev) => prev.filter((item) => item.variantId !== String(variantId)));
  };

  const updateQuantity = (variantId, quantity) => {
    if (quantity < 1) { removeFromCart(variantId); return; }
    setCart((prev) =>
      prev.map((item) => (item.variantId === String(variantId) ? { ...item, quantity } : item))
    );
  };

  const clearCart = () => setCart([]);

  return (
    <AppContext.Provider value={{
      cart, addToCart, removeFromCart, updateQuantity, clearCart,
      user, loginUser, logoutUser, authLoading,
    }}>
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => useContext(AppContext);
