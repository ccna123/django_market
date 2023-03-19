from django.shortcuts import render, redirect
from main.models import Item, Inventory, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.forms import RegisterForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg
from django.template.loader import render_to_string
import json
from urllib.parse import urlencode


def home_page(request):
    return render(request, template_name='main/home.html')


@login_required()
def market_page(request):
    if request.method == 'GET':

        item_rating = Item.objects.annotate(
            avg_rating=Avg('inventory__rating_score'))

        search_item = request.GET.get('search-item')
        if search_item:
            searched_item = Item.objects.filter(name__contains=search_item)
            item_rating = searched_item.annotate(
                avg_rating=Avg('inventory__rating_score'))
            items_name = ", ".join([item.name for item in searched_item])
            messages.success(request, f"Search result: {items_name}")


        for item in item_rating:
            if item.avg_rating == None:
                item.avg_rating = 0

            item.avg_rating = int(item.avg_rating)

        # set up paginator
        p = Paginator(item_rating, 4)
        page = request.GET.get('page')
        item_per_page = p.get_page(page)
        num_of_page = 'a'*item_per_page.paginator.num_pages

        return render(request,
                      template_name='main/market_page.html',
                      context={
                          'item_rating': item_rating,
                          'item_per_page': item_per_page,
                          'num_of_page': num_of_page,
                          'query_params': urlencode(request.GET)
                      }
                      )

    if request.method == 'POST':
        if "add_inventory" in request.POST:
            return add_inventory(request, request.POST.get('item_name'))
        elif "get_item_info" in request.POST:
            return info_page(request, request.POST.get("get_item_info"))


def register_page(request):
    if request.method == 'GET':
        return render(request, template_name='main/register_page.html')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
 
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Successfully register")
            return redirect('home-page')
        else:
            
           errors = form.errors.items()
           for k, v in errors:
               print(v[0])
           return render(request, template_name="main/register_page.html", context={"errors": errors})


def login_page(request):
    if request.method == 'GET':
        return render(request, template_name='main/login_page.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully login")
            return redirect("market-page")
        else:
            messages.error(request, "Failed. Check username and password")
            return render(request, template_name='main/login_page.html')


def logout_page(request):
    logout(request)
    messages.info(request, f"Logged out")
    return redirect("home-page")


def dashboard_page(request):
    if request.method == 'GET':
        
        item_in_inventory = Inventory.objects.filter(
            user_id=request.user.id, is_in_inventory=True)
        item_purchased = Inventory.objects.filter(
            user_id=request.user.id, is_in_inventory=False, is_buying=True)

        return render(request,
                      template_name='main/dashboard.html',
                      context={
                          "item_in_inventory": item_in_inventory,
                          "item_purchased": item_purchased
                      })

    if request.method == 'POST':

        if "get_item_info" in request.POST:
            get_item_info = request.POST.get("get_item_info")
            return info_page(request, get_item_info)

        elif "buy_item" in request.POST:
            buy_item_id = request.POST.get("buy_item")
            return buy_item(request, buy_item_id)

        elif "cancel_item_name" in request.POST:
            return cancel_item(request, request.POST.get("cancel_item_name"))
    print("hahaha")
    return redirect("dashboard-page")


def get_item_and_inventory(item_name):

    item_object = Item.objects.filter(name=item_name).first()
    inventory = Inventory.objects.filter(item_id=item_object.id)
    if inventory is not None:
        user_name = CustomUser.objects.filter(
            id__in=inventory.values_list('user_id', flat=True))
        user_data = []
        for user in user_name:
            inventories = inventory.filter(user_id=user.id).first()
            if inventories:
                user_data.append({
                    'user': user.username,
                    'rating_score': inventories.rating_score,
                    'comments': inventories.comments
                })

    return item_object, inventory, user_data


def info_page(request, item_name):

    if request.method == 'POST':

        item_object, _, user_data = get_item_and_inventory(item_name)

        return render(request,
                      template_name='main/item_info.html',
                      context={
                          'item_object': item_object,
                          'user_data': user_data,
                      })


def review(request, item_name):

    if request.method == 'POST':

        inventory_object = Inventory.objects.filter(
            user_id=request.user.id, item_id=Item.objects.filter(name=item_name).first().id).first()

        if inventory_object:
            inventory_object.comments = request.POST.get('comments')
            inventory_object.rating_score = request.POST.get('rating')
            inventory_object.save()
        else:
            inventory_object = Inventory.objects.create(
                user_id=request.user.id,
                item_id=Item.objects.filter(name=item_name).first().id,
                rating_score=int(request.POST.get('rating')),
                comments=request.POST.get('comments')
            )
            inventory_object.save()

        item_object, _, user_data = get_item_and_inventory(item_name)

        update_review_template = render_to_string(
            'main/reviews.html', {'user_data': user_data},  request=request)

        return JsonResponse({
            "success": True,
            "review_part": update_review_template,
            'comments': request.POST.get('comments')
        })

    return redirect("market-page")


def cancel_item(request, cancel_item_pk):

    if request.method == "POST":
        
        inventory_object = Inventory.objects.filter(
            item_id=cancel_item_pk, user_id=request.user.id).first()
        inventory_object.item.remain += inventory_object.quantity
        messages.success(request, "Cancel Successfully")
        inventory_object.item.save()
        inventory_object.delete()

        item_in_inventory = Inventory.objects.filter(
            user_id=request.user.id)
        update_template = render_to_string("main/cart.html",
                                           {"item_in_inventory": item_in_inventory},
                                           request=request)
        return JsonResponse({
            "success": True,
            "update_template": update_template

        })


def is_enough_in_store(item_object, purchased_quantity):
    return item_object.remain < purchased_quantity


def buy_item(request, buy_item_id):

    inventory_object = Inventory.objects.filter(
        user_id=request.user.id, item_id=buy_item_id).first()
    if can_buy_item(request, buy_item_id):
        request.user.budget -= inventory_object.get_total()
        inventory_object.is_buying = True
        inventory_object.is_in_inventory = False
        inventory_object.bought_quantity += inventory_object.quantity
        inventory_object.quantity = 0
        inventory_object.save()
        request.user.save()
        messages.success(request, f"Buy Successfully")
        return redirect("dashboard-page")
    else:
        messages.error(request, f"Not enough budget")
        return redirect("dashboard-page")


def can_buy_item(request, buy_item_id):
    inventory_object = Inventory.objects.filter(
        user_id=request.user.id, item_id=buy_item_id).first()
    return request.user.budget > inventory_object.get_total()


def add_inventory(request, item_name):

    if request.method == "POST":
        add_inventory_item = item_name
        purchased_quantity = int(request.POST.get('quantity'))


        item_object = Item.objects.filter(name=add_inventory_item).first()
        inventory_object = Inventory.objects.filter(
            item_id=item_object.id, user_id=request.user.id).first()
        if is_enough_in_store(item_object, purchased_quantity):
            return JsonResponse({
                "success": False,
                "remain" : item_object.remain
            })
        else:

            if inventory_object is None:  # not add to inventory, create new item in inventory
                inventory_object = Inventory.objects.create(
                    item_id=item_object.id,
                    user_id=request.user.id,
                    is_in_inventory=True,
                    rating_score=0,
                    comments="",
                    quantity=purchased_quantity
                )
                item_object.remain -= purchased_quantity

                item_object.save()
                inventory_object.save()

                messages.success(
                    request, f"Add { add_inventory_item } to inventory")
            else:  # already have, just add the quantity to that item
                inventory_object.quantity += purchased_quantity
                item_object.remain -= purchased_quantity
                inventory_object.is_in_inventory = True
                inventory_object.save()
                item_object.save()
                

            return JsonResponse({
                "success": True,
                "remain" : item_object.remain
            })

    return redirect("market-page")
