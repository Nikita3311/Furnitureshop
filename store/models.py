from django.db import models
from decimal import Decimal
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название товара")
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    width = models.PositiveIntegerField(verbose_name="Ширина (см)")
    height = models.PositiveIntegerField(verbose_name="Высота (см)")
    depth = models.PositiveIntegerField(verbose_name="Глубина (см)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Cart:
    def __init__(self, request):
        self.session = request.session # сохраняем сессию
        cart = self.session.get('cart') # пробуем получить корзину
        if not cart:
            cart = self.session['cart'] = {}  # если корзины нет — создаём пустую
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            product = Product.objects.get(id=product_id)
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': quantity
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            item['product'] = product
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())