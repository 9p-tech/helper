# Snitch Clone - Frontend

This is a pixel-perfect React clone of the Snitch.co.in fashion website, built with Vite, React 18, and Tailwind CSS. It follows a minimalist, high-contrast "boxed" aesthetic as defined by the project's design system.

## Features

- **Home Page**: Hero banners, category grid, new arrivals carousel.
- **Shop (PLP)**: Dynamic category filtering, size/price filters, responsive grid layout.
- **Product Detail Page (PDP)**: Image gallery with thumbnail selection, size picker, add-to-cart functionality.
- **Cart**: Sidebar summary, item quantity adjustment, subtotal/tax calculations.
- **Checkout**: Form validation (including specific `+91` WhatsApp number validation).
- **Order Confirmation**: Prominent display of generated Order ID.

## Tech Stack

- **React 18** (Vite template)
- **Tailwind CSS** (for styling, utilizing a custom configuration mapped to `DESIGN.md`)
- **React Router v6** (for routing)
- **Lucide React** (for minimalist icons)
- **Context API** (for global cart state management)
- **Axios** (pre-installed for future backend integration)

## Setup Instructions

1. **Prerequisites**: Ensure you have Node.js installed (v18+ recommended).
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Run the Development Server**:
   ```bash
   npm run dev
   ```
4. **Access the App**: Open your browser and navigate to `http://localhost:5173`.

## Design System

The application strictly adheres to the `.stitch/DESIGN.md` guidelines:
- **Typography**: `Montserrat` for headings (Extra Bold/Uppercase), `Inter` for UI and body text.
- **Colors**: Monochromatic scheme (Black `#000000`, White `#FFFFFF`, Surface `#F9F9F9`, Border `#E5E5E5`) with an Accent Red (`#D93025`).
- **Shapes**: Sharp geometric edges (`0px` border-radius).
- **Elevation**: Flat design with `1px` solid borders instead of drop shadows.

## Future Backend Integration

The app uses `src/data/mockData.js` to simulate a backend. The structure and components are designed to easily map to a real API (e.g., `http://localhost:8000/api`) once it is available. To integrate, replace the mock data imports with `axios` fetch calls within `useEffect` hooks in the respective pages.
