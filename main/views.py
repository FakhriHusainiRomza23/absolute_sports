from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.html import strip_tags
import datetime
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)


    context = {
        'npm' : '2406436972',
        'name': request.user.username,
        'class': 'PBP B',
        'product_list' : product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        messages.success(request, f'Product "{product_entry.name}" has been created successfully!')
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'is_featured': product.is_featured,
            'is_hot': product.is_product_hot,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def show_json_mine(request):
    product_list = Product.objects.filter(user=request.user)
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'is_featured': product.is_featured,
            'is_hot': product.is_product_hot,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
def show_json_mine_flutter(request):
    if request.method != 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid method'
        }, status=405)

    username = request.GET.get('username')
    if not username:
        return JsonResponse({
            'status': 'error',
            'message': 'Username parameter is required.'
        }, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'User not found.'
        }, status=404)

    product_list = Product.objects.filter(user=user)
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'is_featured': product.is_featured,
            'is_hot': product.is_product_hot,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'products': data
    })

def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'is_featured': product.is_featured,
            'is_hot': product.is_product_hot,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    form = ProductForm(request.POST or None, instance=product)
    
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, f'Product "{product.name}" has been updated successfully!')
        return redirect('main:show_main')

    context = {
        'form': form,
        'product': product
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_product_entry_ajax(request):
    if request.method == 'POST':
        name = strip_tags(request.POST.get("name", "")) # strip HTML tags!
        description = strip_tags(request.POST.get("description", "")) # strip HTML tags!
        category = request.POST.get("category", "")
        price = request.POST.get("price", "0")
        thumbnail = request.POST.get("thumbnail", "")
        is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
        user = request.user

        # Convert price to integer
        try:
            price = int(price) if price else 0
        except ValueError:
            price = 0

        new_product = Product(
            name=name, 
            description=description,
            category=category,
            price=price,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponse(b"INVALID METHOD", status=405)

@csrf_exempt
@login_required(login_url='/login')
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    if request.method == 'POST':
        name = strip_tags(request.POST.get("name", ""))
        description = strip_tags(request.POST.get("description", ""))
        category = request.POST.get("category", "")
        price = request.POST.get("price", "0")
        thumbnail = request.POST.get("thumbnail", "")
        is_featured = request.POST.get("is_featured") == 'on'

        # Convert price to integer
        try:
            price = int(price) if price else 0
        except ValueError:
            price = 0

        product.name = name
        product.description = description
        product.category = category
        product.price = price
        product.thumbnail = thumbnail
        product.is_featured = is_featured
        product.save()

        return HttpResponse(b"UPDATED", status=200)
    
    elif request.method == 'GET':
        data = {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'price': product.price,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
        }
        return JsonResponse(data)
    
    return HttpResponse(b"INVALID METHOD", status=405)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    return HttpResponse(b"DELETED", status=200)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response_payload = {
                'status': 'success',
                'message': 'Login successful!',
                'redirect_url': reverse('main:show_main'),
                'username': user.username,
                'user_id': user.pk,
            }
            request.session['login_payload'] = {
                'username': user.username,
                'user_id': user.pk,
            }
            response = JsonResponse(response_payload)
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password.'
            }, status=401)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return JsonResponse({
                'status': 'error',
                'message': 'Passwords do not match.'
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Username already exists.'
            }, status=400)
            
        try:
            user = User.objects.create_user(username=username, password=password1)
            return JsonResponse({
                'status': 'success',
                'message': 'Account created successfully!',
                'redirect_url': reverse('main:login')
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Registration failed. Please try again.'
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
@login_required(login_url='/login')
def logout_ajax(request):
    if request.method == 'POST':
        logout(request)
        response = JsonResponse({
            'status': 'success',
            'message': 'Logout successful!',
            'redirect_url': reverse('main:login')
        })
        response.delete_cookie('last_login')
        return response
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        username = data.get("username")
        price_raw = data.get("price")

        if price_raw in (None, ""):
            return JsonResponse({
                "status": "error",
                "message": "Price is required."
            }, status=400)

        try:
            price = int(price_raw)
        except (TypeError, ValueError):
            return JsonResponse({
                "status": "error",
                "message": "Price must be a whole number."
            }, status=400)

        if price < 0:
            return JsonResponse({
                "status": "error",
                "message": "Price cannot be negative."
            }, status=400)
        user = request.user if request.user.is_authenticated else None

        if not user and username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "User not found."
                }, status=404)

        if not user:
            return JsonResponse({
                "status": "error",
                "message": "Unable to determine user. Include a valid username or login first."
            }, status=401)
        
        new_product = Product(
            name=name, 
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)