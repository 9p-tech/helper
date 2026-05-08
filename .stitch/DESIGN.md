# Snitch Clone Design System

## Core Identity
A premium, minimalist, high-contrast eCommerce brand heavily inspired by snitch.co.in. The overall aesthetic is sharp, modern, and heavily relies on black-and-white contrast, large edge-to-edge imagery, and stark typography.

## Global Tokens

### Typography
- **Primary Font**: `Inter`, sans-serif (used for all body text, buttons, and navigation)
- **Heading Font**: `Montserrat`, sans-serif (used for large hero headers and prominent section titles)
- **Weights**: 
  - Regular (400) for body text and descriptions
  - Medium (500) for navigation and buttons
  - Bold (700) for product titles, prices, and headings
  - Extra Bold (800) for "Order ID" on confirmation pages and prominent banners

### Colors
- **Primary**: `#000000` (Pure Black)
- **Primary Foreground**: `#FFFFFF`
- **Background**: `#FFFFFF` (Pure White)
- **Surface**: `#F9F9F9` (Very light gray for alternating sections or cart drawers)
- **Border**: `#E5E5E5` (Light gray for dividers, borders)
- **Muted Text**: `#737373` (For secondary information, old prices, descriptions)
- **Accent/Sale**: `#D93025` (Red for Sale tags, error states, and urgent CTA accents)

### Spacing & Grid
- **Spacing Scale**: Base 4px (4, 8, 12, 16, 24, 32, 48, 64)
- **Container Max Width**: `1440px` with `padding-x: 16px` on mobile, `32px` on desktop.
- **Product Grid**: 
  - Desktop: 4 columns
  - Tablet: 3 columns
  - Mobile: 2 columns

### Shapes & Borders
- **Border Radius**: Sharp edges (`0px`) or very subtle (`2px`). Snitch uses a very boxed, sharp aesthetic.
- **Borders**: 1px solid `#E5E5E5` for form inputs, sidebars, and dividers.

## Component Specifications

### 1. Product Cards
- **Image Aspect Ratio**: `2:3` (Tall, portrait images suited for fashion).
- **Hover Effects**: Subtly fade in the secondary image on hover, or slightly scale up the primary image.
- **Badges**: Rectangular, absolute positioned at top-left.
  - "NEW": Black background, white text.
  - "BESTSELLER": White background, black text, 1px black border.
  - "SALE": Red background, white text.
- **Details**: Product title in bold, price below it. No decimals for INR (e.g., `₹ 1,299`). Old price has line-through and muted color.

### 2. Navigation Bar
- **Layout**: Logo centered. Hamburger menu & Search on left (mobile), categories on left (desktop). Icons (Search, Profile, Cart) on the right.
- **Style**: Sticky top, pure white background, 1px bottom border.
- **Cart Icon**: Should display a small circular badge with the item count if > 0.

### 3. Buttons
- **Primary Button**: Black background, White text, 0px border radius, bold text, uppercase. Hover: Dark gray (`#1A1A1A`).
- **Secondary Button**: White background, Black text, 1px solid black border, 0px border radius. Hover: Black background, White text.
- **Size Selector Pills**: Rectangular pills. Unselected: White bg, gray border. Selected: Black bg, white text.

### 4. Forms & Inputs
- **Inputs**: 1px solid `#E5E5E5` border, `0px` radius, padding `12px 16px`. Focus state: 1px solid `#000000` (no outline ring).
- **Labels**: Small, uppercase, bold, black text above the input.

### 5. Product Detail Page (PDP)
- **Gallery**: Left side. On desktop, large stacked images or vertical thumbnails + main image. On mobile, a horizontal swipeable carousel.
- **Right Sidebar**: Sticky on desktop. Contains Title, Price, Tax info, Size selector, "Add to Cart" (Primary button), "Buy Now" (Secondary button), and accordion for Description/Details.

### 6. Animations
- Smooth, fast transitions (`200ms ease-in-out`).
- Cart drawer slides in from the right.
- Mega menus slide down from the navbar.
