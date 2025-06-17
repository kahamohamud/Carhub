from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CarForm
from .models import Car, Dealer, Wishlist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_dealer:
                Dealer.objects.create(user=user)
            login(request, user)
            return redirect('welcome')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
    return render(request, 'login.html')

def welcome(request):
    return render(request, 'welcome.html')

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})

def dealer_list(request):
    dealers = Dealer.objects.all()
    return render(request, 'dealer_list.html', {'dealers': dealers})

def dealer_detail(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    return render(request, 'dealer_detail.html', {'dealer': dealer})

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.dealer = request.user.dealer
            car.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})
def dealer_list(request):
    query = request.GET.get('q')
    if query:
        dealers = Dealer.objects.filter(user__username__icontains=query)
    else:
        dealers = Dealer.objects.all()
    return render(request, 'dealer_list.html', {'dealers': dealers})

def car_list(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    filters = Q()
    if query:
        filters &= Q(name__icontains=query) | Q(model__icontains=query)
    if min_price:
        filters &= Q(price__gte=min_price)
    if max_price:
        filters &= Q(price__lte=max_price)
    
    cars = Car.objects.filter(filters)
    return render(request, 'car_list.html', {'cars': cars})
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})

@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Wishlist.objects.get_or_create(user=request.user, car=car)
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
@login_required
def manage_cars(request):
    if request.user.is_dealer:
        cars = Car.objects.filter(dealer=request.user.dealer)
        return render(request, 'manage_cars.html', {'cars': cars})
    return redirect('car_list')

@login_required
def update_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user.dealer != car.dealer:
        return redirect('car_list')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('manage_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'add_car.html', {'form': form})

@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.user.dealer == car.dealer:
        car.delete()
    return redirect('manage_cars')
@login_required
def update_profile(request):
    dealer = get_object_or_404(Dealer, user=request.user)
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        if 'image' in request.FILES:
            dealer.image = request.FILES['image']
        request.user.save()
        dealer.save()
        return redirect('welcome')
    return render(request, 'update_profile.html', {'user': request.user, 'dealer': dealer})