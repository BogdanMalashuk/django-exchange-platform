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
            {"username": "dave", "email": "dave@example.com"},
            {"username": "eve", "email": "eve@example.com"},
            {"username": "frank", "email": "frank@example.com"},
            {"username": "grace", "email": "grace@example.com"},
            {"username": "heidi", "email": "heidi@example.com"},
            {"username": "ivan", "email": "ivan@example.com"},
            {"username": "judy", "email": "judy@example.com"},
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
            {"title": "Смартфон Samsung", "description": "Рабочий, есть трещина на экране.", "category": "electronics",
             "condition": "used"},
            {"title": "Ноутбук HP", "description": "Производительный ноутбук для работы.", "category": "electronics",
             "condition": "new"},
            {"title": "Футболка Nike", "description": "Размер L, почти новая.", "category": "clothing",
             "condition": "used"},
            {"title": "Куртка зимняя", "description": "Очень тёплая, размер M.", "category": "clothing",
             "condition": "new"},
            {"title": "Рюкзак городской", "description": "Почти новый, много карманов.", "category": "accessories",
             "condition": "new"},
            {"title": "Сумка на плечо", "description": "Кожаная, в отличном состоянии.", "category": "accessories",
             "condition": "used"},
            {"title": "Детская кроватка", "description": "Из массива дерева.", "category": "kids", "condition": "used"},
            {"title": "Коляска 2-в-1", "description": "Удобная и лёгкая для прогулок.", "category": "kids",
             "condition": "new"},
            {"title": "Гантели по 5 кг", "description": "Идеальны для домашних тренировок.", "category": "sport",
             "condition": "used"},
            {"title": "Фитнес-резинки", "description": "Набор из 5 штук, новые.", "category": "sport",
             "condition": "new"},
            {"title": "Учебник по физике", "description": "За 11 класс, в хорошем состоянии.", "category": "books",
             "condition": "used"},
            {"title": "Сборник тестов ЕГЭ", "description": "2024 год, как новый.", "category": "books",
             "condition": "new"},
            {"title": "Стул офисный", "description": "Эргономичная спинка, серый цвет.", "category": "furniture",
             "condition": "new"},
            {"title": "Письменный стол", "description": "Деревянный, с ящиками.", "category": "furniture",
             "condition": "used"},
            {"title": "Микроволновка LG", "description": "Рабочая, 800 Вт.", "category": "appliances",
             "condition": "used"},
            {"title": "Холодильник Samsung", "description": "На гарантии, двухкамерный.", "category": "appliances",
             "condition": "new"},
            {"title": "Умные часы", "description": "С поддержкой уведомлений и шагомера.", "category": "electronics",
             "condition": "new"},
            {"title": "Пылесос ручной", "description": "Удобный для быстрой уборки.", "category": "appliances",
             "condition": "used"},
            {"title": "Шапка зимняя", "description": "Вязаная, тёплая.", "category": "clothing", "condition": "new"},
            {"title": "Перчатки кожаные", "description": "Размер S, мягкие.", "category": "accessories",
             "condition": "used"},
            {"title": "Плавательный круг", "description": "Для детей 3–6 лет.", "category": "kids", "condition": "new"},
            {"title": "Мяч футбольный", "description": "Размер 5, как новый.", "category": "sport", "condition": "new"},
            {"title": "Книга «Война и мир»", "description": "Том 1, старое издание.", "category": "books",
             "condition": "used"},
            {"title": "Кровать двуспальная", "description": "Металлический каркас.", "category": "furniture",
             "condition": "used"},
            {"title": "Блендер стационарный", "description": "С тремя скоростями.", "category": "appliances",
             "condition": "new"},
            {"title": "Планшет Lenovo", "description": "Для интернета и чтения книг.", "category": "electronics",
             "condition": "used"},
            {"title": "Брюки джинсовые", "description": "Светло-синие, размер 48.", "category": "clothing",
             "condition": "used"},
            {"title": "Кроссовки Adidas", "description": "Почти не носил.", "category": "clothing", "condition": "new"},
            {"title": "Скакалка с трекером", "description": "Учитывает количество прыжков.", "category": "sport",
             "condition": "new"},
            {"title": "Детская игрушка", "description": "Музыкальная, работает от батареек.", "category": "kids",
             "condition": "used"},
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
