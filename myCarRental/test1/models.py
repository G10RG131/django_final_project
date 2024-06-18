from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, phone, email, name, surname, password=None):
        if not phone:
            raise ValueError('The Phone Number field is required')
        user = self.model(phone=phone, email=email, name=name, surname=surname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, name, surname, password=None):
        user = self.create_user(phone, email, name, surname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    fuel_capacity = models.PositiveIntegerField()
    picture1 = models.ImageField(upload_to='staticfiles/car_images/', blank=False, null=False)
    picture2 = models.ImageField(upload_to='staticfiles/car_images/', blank=True, null=True)
    picture3 = models.ImageField(upload_to='staticfiles/car_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class RentalHistory(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_time = models.DateTimeField()
    paid_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.name} rented {self.car.id} {self.car.model}"


class LikedCars(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} liked {self.car.id} {self.car.model}"


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.car}"
