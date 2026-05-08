import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        try {
          const { data } = await axios.post('/api/auth/token/refresh/', { refresh });
          localStorage.setItem('access_token', data.access);
          original.headers.Authorization = `Bearer ${data.access}`;
          return api(original);
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
    }
    return Promise.reject(err);
  }
);

export default api;

// ── Auth ──────────────────────────────────────────
export const register = (data) => api.post('/auth/register/', data);
export const login = (data) => api.post('/auth/login/', data);
export const getMe = () => api.get('/auth/me/');

// ── Catalog ───────────────────────────────────────
export const getCategories = () => api.get('/categories/');
export const getProducts = (params) => api.get('/products/', { params });
export const getProduct = (slug) => api.get(`/products/${slug}/`);
export const getReviews = (slug) => api.get(`/products/${slug}/reviews/`);
export const postReview = (slug, data) => api.post(`/products/${slug}/reviews/`, data);

// ── Orders ────────────────────────────────────────
export const quickCheckout = (data) => api.post('/orders/quick-checkout/', data);
export const getOrders = () => api.get('/orders/');
export const getOrder = (id) => api.get(`/orders/${id}/`);

// ── Coupon ────────────────────────────────────────
export const applyCoupon = (data) => api.post('/coupons/apply/', data);
