from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', blank=False, unique=True)
    email = models.CharField(max_length=254, verbose_name='Почта', blank=False, unique=True)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    USERNAME_FIELD = 'username'

    def full_name(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    def __str__(self):
        self.full_name()


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=True)
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    year = models.IntegerField(verbose_name='Год произовдства', blank=True)
    country = models.CharField(max_length=254, verbose_name='Страна производства', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
                                default=0.00)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=1)
    photo_file = models.ImageField(max_length=254, upload_to=get_name_file,
                                   blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название', blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=(('new', 'Новый'), ('confirmed', 'Подтверждёные'), ('canceled', 'Отменённый')),
                              default='user')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    reason = models.TextField(verbose_name='Причина отказа', blank=True)
    product = models.ManyToManyField(Product, through='ItemInOrder', related_name='orders')

    def __str__(self):
        return self.date.crime() + ' | ' + self.user.full_name()


class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
                                default=0.00)


class Cart(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=1)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ' - ' + str(self.count)
