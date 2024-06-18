from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.template import loader
from .forms import CarForm
from .forms import PhoneAuthenticationForm
from .forms import UserRegistrationForm
from .models import Car
from .models import RentalHistory, LikedCars
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Like
from django.contrib import messages


def test1(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())


def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})


def login_view(request):
    if request.method == 'POST':
        form = PhoneAuthenticationForm(request, data=request.POST)
        if form.is_valid():

            phone = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = PhoneAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("asdgsadg")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, "Added new car.")

            return redirect('home')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    rented_cars = RentalHistory.objects.filter(user=user)
    liked_cars = Car.objects.filter(like__user=request.user)
    uploaded_cars = Car.objects.filter(owner=user)

    context = {
        'user': user,
        'rented_cars': rented_cars,
        'liked_cars': liked_cars,
        'uploaded_cars': uploaded_cars
    }

    return render(request, 'profile.html', context)


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this car.")
    car.delete()
    return redirect('profile')


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, car=car).exists()
    context = {
        'car': car,
        'liked': liked,
    }
    return render(request, 'car_detail.html', context)


@login_required
def like_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    like, created = Like.objects.get_or_create(user=request.user, car=car)
    if not created:
        like.delete()
    return redirect('car_detail', car_id=car_id)
