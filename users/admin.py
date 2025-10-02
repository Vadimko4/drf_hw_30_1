from django.contrib import admin


from users.models import User, Payment


@admin.register(User)  # Регистрируем модель
class UserAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'email',)


@admin.register(Payment)  # Регистрируем модель
class PaymentAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'user', 'amount','course', 'lesson', 'date', 'type')
    # По чему будем делать фильтрацию
    list_filter = ('id', 'course', 'user')
    # По чему у нас будет поиск
    search_fields = ('user', 'course')
