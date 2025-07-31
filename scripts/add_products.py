from store.models import Product, Category
import random

base_names = ['Модель', 'Серия', 'Линия', 'Комфорт', 'Дизайн', 'Эко', 'Люкс', 'Мини', 'Макси']
categories = list(Category.objects.all())

if not categories:
    print("⚠️ Нет категорий — добавьте их сначала!")
else:
    Product.objects.all().delete()
    print("🧹 Старые товары удалены.")

    for i in range(1, 51):
        title = f"{random.choice(base_names)} {i}"
        category = random.choice(categories)
        description = f"Описание для товара {title}"
        price = round(random.uniform(1000, 50000), 2)
        width = random.randint(50, 300)
        height = random.randint(50, 250)
        depth = random.randint(30, 200)

        Product.objects.create(
            title=title,
            category=category,
            description=description,
            price=price,
            width=width,
            height=height,
            depth=depth
        )

        print(f"✅ Добавлен: {title} ({category.name}) — {price}₽, {width}x{height}x{depth} см")

print("🎉 Готово! 50 товаров добавлены.")
