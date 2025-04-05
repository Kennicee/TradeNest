from django.core.management.base import BaseCommand
from marketplace.models import Product

class Command(BaseCommand):
    help = 'Assigns default titles to products that have no title.'

    def handle(self, *args, **kwargs):
        products = Product.objects.filter(title__isnull=True) | Product.objects.filter(title="")
        count = 0

        for i, product in enumerate(products, start=1):
            product.title = f"Untitled Product {i}"
            product.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} product(s).'))
