from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ads.models import Ad


class Command(BaseCommand):
    help = "Очищает БД и создаёт 3 тестовых пользователя + 10 тестовых объявлений"

    def handle(self, *args, **kwargs):
        Ad.objects.all().delete()
        self.stdout.write("🗑️ Все объявления удалены.")

        User.objects.filter(is_superuser=False).delete()
        self.stdout.write("🗑️ Все обычные пользователи удалены.")

        users_data = [
            {"username": "alice", "email": "alice@example.com"},
            {"username": "bob", "email": "bob@example.com"},
            {"username": "carol", "email": "carol@example.com"},
        ]

        users = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password="testpass123"
            )
            users.append(user)
            self.stdout.write(f"👤 Пользователь {user.username} создан.")

        ads_data = [
            {"title": "Смартфон Samsung", "description": "Рабочий, есть трещина на экране.", "category": "Электроника", "condition": "new"},
            {"title": "Куртка зимняя", "description": "Тёплая, размер M.", "category": "Одежда", "condition": "used"},
            {"title": "Рюкзак городской", "description": "Почти новый, вместительный.", "category": "Аксессуары", "condition": "new"},
            {"title": "Ноутбук Lenovo", "description": "Для работы и учёбы. SSD 256 ГБ.", "category": "Электроника", "condition": "used"},
            {"title": "Детская коляска", "description": "Удобная и лёгкая.", "category": "Товары для детей", "condition": "used"},
            {"title": "Игровая приставка", "description": "PlayStation 4, 2 геймпада.", "category": "Электроника", "condition": "used"},
            {"title": "Сноуборд", "description": "Подходит для начинающих.", "category": "Спорт", "condition": "new"},
            {"title": "Учебники по математике", "description": "Полный комплект за 10 класс.", "category": "Книги", "condition": "used"},
            {"title": "Стул офисный", "description": "Эргономичный, серый цвет.", "category": "Мебель", "condition": "new"},
            {"title": "Микроволновка", "description": "Рабочая, 700 Вт.", "category": "Бытовая техника", "condition": "used"},
        ]

        for i, ad_data in enumerate(ads_data):
            ad = Ad.objects.create(
                user=users[i % len(users)],
                title=ad_data["title"],
                description=ad_data["description"],
                category=ad_data["category"],
                condition=ad_data["condition"],
                image_url="https://www.svgrepo.com/show/508699/landscape-placeholder.svg"
            )
            self.stdout.write(f"📦 Объявление \"{ad.title}\" создано.")

        self.stdout.write(self.style.SUCCESS("✅ Готово: база наполнена тестовыми данными."))
