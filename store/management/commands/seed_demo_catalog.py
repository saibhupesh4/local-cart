from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from category.models import Category
from store.models import Product, Variation


DEMO_PRODUCTS = (
    ('ATX Jeans', 'atx-jeans', 'Jeans', 'jeans', 199, 58, '3.jpg', 'ATX-Jeans.jpg'),
    ('RXN Blue Shirt', 'rxn-blue-shirt', 'Shirts', 'shirts', 99, 197, '1.jpg', 'Blue-Shirt.jpg'),
    ('Great Tshirt', 'great-tshirt', 'T Shirt', 't-shirt', 119, 0, '1.jpg', 'Great-Tshirt.jpg'),
    ('Jordan Basketball Shoes', 'jordan-basketball-shoes', 'Shoes', 'shoes', 999, 500, '12.jpg', 'jordan-true-flight-basketball-shoes.jpg'),
    ('Mavi Jeans', 'mavi-jeans', 'Jeans', 'jeans', 499, 1000, '3.jpg', 'Mavi_jeans.jpg'),
    ('Puma Ferrari Shoes', 'puma-ferrari-shoes', 'Shoes', 'shoes', 1099, 499, '12.jpg', 'Puma-Ferrari-Shoes.jpg'),
    ('US Polo Assn Jacket', 'us-polo-assn-jacket', 'Jackets', 'jackets', 899, 300, '2.jpg', 'US-Polo-Assn_Jacket.jpg'),
    ('Wrangler Shirt', 'wrangler-shirt', 'Shirts', 'shirts', 699, 1234, '1.jpg', 'Wrangler-Shirt.jpg'),
)


class Command(BaseCommand):
    help = 'Create the safe local demo catalog and copy its bundled images into media.'

    def handle(self, *args, **options):
        image_source = Path(settings.BASE_DIR) / 'greatkart' / 'static' / 'images' / 'items'
        image_target = Path(settings.MEDIA_ROOT) / 'photos' / 'products'
        image_target.mkdir(parents=True, exist_ok=True)
        products_created = 0
        variations_created = 0

        for name, slug, category_name, category_slug, price, stock, source_name, image_name in DEMO_PRODUCTS:
            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'category_name': category_name},
            )
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'product_name': name,
                    'description': 'Sample demo item for the local store.',
                    'price': price,
                    'stock': stock,
                    'is_available': True,
                    'category': category,
                },
            )
            products_created += int(created)

            source = image_source / source_name
            target = image_target / image_name
            if not source.exists():
                self.stderr.write(self.style.WARNING('Missing bundled image: {}'.format(source)))
            elif not target.exists():
                shutil.copy2(str(source), str(target))
            if not product.images:
                product.images = 'photos/products/{}'.format(image_name)
                product.save(update_fields=['images'])

            category_key = category_slug.lower()
            if 'shoe' in category_key:
                sizes = ('7', '8', '9', '10', '11')
            elif 'jean' in category_key or 'trouser' in category_key:
                sizes = ('30', '32', '34', '36', '38')
            else:
                sizes = ('S', 'M', 'L', 'XL')
            for size in sizes:
                _, was_created = Variation.objects.get_or_create(
                    product=product,
                    variation_category='size',
                    variation_value=size,
                    defaults={'is_active': True},
                )
                variations_created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            'Demo catalog ready: {} products and {} size options added.'.format(
                products_created, variations_created
            )
        ))
