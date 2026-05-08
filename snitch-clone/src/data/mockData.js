export const categories = [
  { id: 'c1', name: 'Shirts', image: 'https://images.unsplash.com/photo-1596755094514-f87e32f85e23?w=800&q=80' },
  { id: 'c2', name: 'T-Shirts', image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80' },
  { id: 'c3', name: 'Trousers', image: 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80' },
  { id: 'c4', name: 'Co-ords', image: 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&q=80' }
];

export const products = [
  {
    id: 'p1',
    name: 'Black Regular Fit Solid Shirt',
    price: 1299,
    originalPrice: 1999,
    category: 'Shirts',
    badge: 'NEW',
    images: [
      'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80',
      'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&q=80'
    ],
    sizes: ['S', 'M', 'L', 'XL'],
    colors: ['#000000', '#ffffff'],
    description: 'A classic black solid shirt crafted from premium cotton.'
  },
  {
    id: 'p2',
    name: 'Olive Green Oversized T-Shirt',
    price: 999,
    originalPrice: null,
    category: 'T-Shirts',
    badge: 'BESTSELLER',
    images: [
      'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&q=80',
      'https://images.unsplash.com/photo-1583744368321-7278278216c2?w=800&q=80'
    ],
    sizes: ['M', 'L', 'XL'],
    colors: ['#556b2f', '#000000'],
    description: 'Comfortable oversized fit with drop shoulders.'
  },
  {
    id: 'p3',
    name: 'Beige Chino Trousers',
    price: 1499,
    originalPrice: 2499,
    category: 'Trousers',
    badge: 'SALE',
    images: [
      'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80',
      'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800&q=80'
    ],
    sizes: ['30', '32', '34', '36'],
    colors: ['#f5f5dc'],
    description: 'Tailored fit chinos perfect for a smart-casual look.'
  },
  {
    id: 'p4',
    name: 'Navy Blue Checkered Shirt',
    price: 1199,
    originalPrice: 1599,
    category: 'Shirts',
    badge: null,
    images: [
      'https://images.unsplash.com/photo-1596755094514-f87e32f85e23?w=800&q=80',
      'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80'
    ],
    sizes: ['S', 'M', 'L'],
    colors: ['#000080'],
    description: 'Classic checkered shirt for everyday wear.'
  }
];

export const homeBanners = [
  {
    id: 'b1',
    title: 'THE NEW STANDARD',
    subtitle: 'SUMMER 24 COLLECTION',
    image: 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=2000&q=80'
  }
];
