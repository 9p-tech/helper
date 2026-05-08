from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product, ProductVariant


CATEGORIES = [
    {'name': 'T-Shirts', 'slug': 't-shirts', 'display_order': 1},
    {'name': 'Shirts', 'slug': 'shirts', 'display_order': 2},
    {'name': 'Trousers', 'slug': 'trousers', 'display_order': 3},
]

PRODUCTS = [
    {
        'category_slug': 't-shirts',
        'name': 'Acid Wash Oversized Tee',
        'slug': 'acid-wash-oversized-tee',
        'description': 'Premium acid wash oversized tee for the bold look.',
        'material': '100% Cotton',
        'base_price': 999,
        'discount_price': 699,
        'is_featured': True,
        'variants': [
            {'size': 'S', 'color': 'Black', 'color_hex': '#000000', 'stock': 50, 'sku': 'AWT-BLK-S'},
            {'size': 'M', 'color': 'Black', 'color_hex': '#000000', 'stock': 80, 'sku': 'AWT-BLK-M'},
            {'size': 'L', 'color': 'Black', 'color_hex': '#000000', 'stock': 60, 'sku': 'AWT-BLK-L'},
            {'size': 'XL', 'color': 'Black', 'color_hex': '#000000', 'stock': 40, 'sku': 'AWT-BLK-XL'},
            {'size': 'M', 'color': 'White', 'color_hex': '#FFFFFF', 'stock': 70, 'sku': 'AWT-WHT-M'},
            {'size': 'L', 'color': 'White', 'color_hex': '#FFFFFF', 'stock': 55, 'sku': 'AWT-WHT-L'},
        ],
    },
    {
        'category_slug': 't-shirts',
        'name': 'Vintage Graphic Tee',
        'slug': 'vintage-graphic-tee',
        'description': 'Retro-inspired graphic tee with premium print.',
        'material': '100% Cotton',
        'base_price': 799,
        'discount_price': 599,
        'is_featured': True,
        'variants': [
            {'size': 'S', 'color': 'Navy', 'color_hex': '#1F3A5F', 'stock': 40, 'sku': 'VGT-NVY-S'},
            {'size': 'M', 'color': 'Navy', 'color_hex': '#1F3A5F', 'stock': 60, 'sku': 'VGT-NVY-M'},
            {'size': 'L', 'color': 'Navy', 'color_hex': '#1F3A5F', 'stock': 50, 'sku': 'VGT-NVY-L'},
        ],
    },
    {
        'category_slug': 't-shirts',
        'name': 'Minimal Drop Shoulder Tee',
        'slug': 'minimal-drop-shoulder-tee',
        'description': 'Clean minimal design with drop shoulder cut.',
        'material': '100% Pima Cotton',
        'base_price': 1199,
        'discount_price': 899,
        'is_featured': False,
        'variants': [
            {'size': 'M', 'color': 'Cream', 'color_hex': '#F5F0E8', 'stock': 35, 'sku': 'MDS-CRM-M'},
            {'size': 'L', 'color': 'Cream', 'color_hex': '#F5F0E8', 'stock': 45, 'sku': 'MDS-CRM-L'},
            {'size': 'XL', 'color': 'Cream', 'color_hex': '#F5F0E8', 'stock': 30, 'sku': 'MDS-CRM-XL'},
            {'size': 'M', 'color': 'Black', 'color_hex': '#000000', 'stock': 40, 'sku': 'MDS-BLK-M'},
        ],
    },
    {
        'category_slug': 'shirts',
        'name': 'Cuban Collar Shirt',
        'slug': 'cuban-collar-shirt',
        'description': 'Resort-style Cuban collar shirt, perfect for summers.',
        'material': '100% Viscose',
        'base_price': 1499,
        'discount_price': 1199,
        'is_featured': True,
        'variants': [
            {'size': 'S', 'color': 'Sage Green', 'color_hex': '#8FAF82', 'stock': 25, 'sku': 'CCS-SGR-S'},
            {'size': 'M', 'color': 'Sage Green', 'color_hex': '#8FAF82', 'stock': 40, 'sku': 'CCS-SGR-M'},
            {'size': 'L', 'color': 'Sage Green', 'color_hex': '#8FAF82', 'stock': 35, 'sku': 'CCS-SGR-L'},
            {'size': 'M', 'color': 'White', 'color_hex': '#FFFFFF', 'stock': 50, 'sku': 'CCS-WHT-M'},
        ],
    },
    {
        'category_slug': 'shirts',
        'name': 'Linen Casual Shirt',
        'slug': 'linen-casual-shirt',
        'description': 'Breathable linen shirt for everyday wear.',
        'material': '100% Linen',
        'base_price': 1799,
        'discount_price': None,
        'is_featured': False,
        'variants': [
            {'size': 'M', 'color': 'Beige', 'color_hex': '#D4B896', 'stock': 30, 'sku': 'LCS-BGE-M'},
            {'size': 'L', 'color': 'Beige', 'color_hex': '#D4B896', 'stock': 25, 'sku': 'LCS-BGE-L'},
            {'size': 'XL', 'color': 'Beige', 'color_hex': '#D4B896', 'stock': 20, 'sku': 'LCS-BGE-XL'},
        ],
    },
    {
        'category_slug': 'shirts',
        'name': 'Oversized Flannel Shirt',
        'slug': 'oversized-flannel-shirt',
        'description': 'Double-brushed flannel for a cozy oversized fit.',
        'material': '100% Cotton Flannel',
        'base_price': 1999,
        'discount_price': 1599,
        'is_featured': True,
        'variants': [
            {'size': 'M', 'color': 'Red Check', 'color_hex': '#C0392B', 'stock': 20, 'sku': 'OFS-RDC-M'},
            {'size': 'L', 'color': 'Red Check', 'color_hex': '#C0392B', 'stock': 25, 'sku': 'OFS-RDC-L'},
            {'size': 'XL', 'color': 'Red Check', 'color_hex': '#C0392B', 'stock': 15, 'sku': 'OFS-RDC-XL'},
        ],
    },
    {
        'category_slug': 'trousers',
        'name': 'Cargo Jogger Pants',
        'slug': 'cargo-jogger-pants',
        'description': 'Multi-pocket cargo joggers with elastic waist.',
        'material': '98% Cotton 2% Elastane',
        'base_price': 1699,
        'discount_price': 1299,
        'is_featured': True,
        'variants': [
            {'size': 'S', 'color': 'Olive', 'color_hex': '#6B6B3A', 'stock': 30, 'sku': 'CGP-OLV-S'},
            {'size': 'M', 'color': 'Olive', 'color_hex': '#6B6B3A', 'stock': 45, 'sku': 'CGP-OLV-M'},
            {'size': 'L', 'color': 'Olive', 'color_hex': '#6B6B3A', 'stock': 40, 'sku': 'CGP-OLV-L'},
            {'size': 'XL', 'color': 'Olive', 'color_hex': '#6B6B3A', 'stock': 25, 'sku': 'CGP-OLV-XL'},
            {'size': 'M', 'color': 'Black', 'color_hex': '#000000', 'stock': 50, 'sku': 'CGP-BLK-M'},
            {'size': 'L', 'color': 'Black', 'color_hex': '#000000', 'stock': 45, 'sku': 'CGP-BLK-L'},
        ],
    },
    {
        'category_slug': 'trousers',
        'name': 'Slim Fit Chinos',
        'slug': 'slim-fit-chinos',
        'description': 'Tailored slim fit chinos for smart casual looks.',
        'material': '97% Cotton 3% Elastane',
        'base_price': 1899,
        'discount_price': 1499,
        'is_featured': False,
        'variants': [
            {'size': 'S', 'color': 'Khaki', 'color_hex': '#C3B091', 'stock': 20, 'sku': 'SFC-KHK-S'},
            {'size': 'M', 'color': 'Khaki', 'color_hex': '#C3B091', 'stock': 35, 'sku': 'SFC-KHK-M'},
            {'size': 'L', 'color': 'Khaki', 'color_hex': '#C3B091', 'stock': 30, 'sku': 'SFC-KHK-L'},
            {'size': 'M', 'color': 'Navy', 'color_hex': '#1F3A5F', 'stock': 30, 'sku': 'SFC-NVY-M'},
        ],
    },
    {
        'category_slug': 'trousers',
        'name': 'Wide Leg Linen Trousers',
        'slug': 'wide-leg-linen-trousers',
        'description': 'Relaxed wide-leg linen trousers for summer vibes.',
        'material': '100% Linen',
        'base_price': 2199,
        'discount_price': 1799,
        'is_featured': False,
        'variants': [
            {'size': 'S', 'color': 'White', 'color_hex': '#FFFFFF', 'stock': 15, 'sku': 'WLT-WHT-S'},
            {'size': 'M', 'color': 'White', 'color_hex': '#FFFFFF', 'stock': 25, 'sku': 'WLT-WHT-M'},
            {'size': 'L', 'color': 'White', 'color_hex': '#FFFFFF', 'stock': 20, 'sku': 'WLT-WHT-L'},
        ],
    },
    {
        'category_slug': 't-shirts',
        'name': 'Tie-Dye Boxy Tee',
        'slug': 'tie-dye-boxy-tee',
        'description': 'Hand-crafted tie-dye in a relaxed boxy cut.',
        'material': '100% Cotton',
        'base_price': 1099,
        'discount_price': 849,
        'is_featured': True,
        'variants': [
            {'size': 'S', 'color': 'Multicolor', 'color_hex': '#9B59B6', 'stock': 20, 'sku': 'TDB-MLC-S'},
            {'size': 'M', 'color': 'Multicolor', 'color_hex': '#9B59B6', 'stock': 30, 'sku': 'TDB-MLC-M'},
            {'size': 'L', 'color': 'Multicolor', 'color_hex': '#9B59B6', 'stock': 25, 'sku': 'TDB-MLC-L'},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample categories, products, and variants'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data,
            )
            cat_map[cat.slug] = cat
            status = 'created' if created else 'exists'
            self.stdout.write(f'  [{status}] {cat.name}')

        self.stdout.write('Seeding products...')
        for prod_data in PRODUCTS:
            variants = prod_data.pop('variants')
            category = cat_map[prod_data.pop('category_slug')]

            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={**prod_data, 'category': category},
            )
            status = 'created' if created else 'exists'
            self.stdout.write(f'  [{status}] {product.name}')

            for v in variants:
                ProductVariant.objects.get_or_create(
                    sku=v['sku'],
                    defaults={**v, 'product': product},
                )

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(CATEGORIES)} categories, {len(PRODUCTS)} products seeded.'
        ))
