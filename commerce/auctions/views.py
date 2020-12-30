from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Listings, WatchList, Comments, Bid
from .forms import AddItemsForm, WatchListForm


def index(request):
    return render(request, "auctions/index.html", {
        "all_items": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def add_item(request):
    if request.method == "POST":
        form = AddItemsForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Get the data but not save it just yet
            instance.user = request.user  # Add the user to the new variable
            instance.save()  # Save all info on the DB
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/add.html", {
            "form": AddItemsForm(),
        })


@login_required(login_url='login')
def listing_page(request, item_id):
    # Filter the WatchList DB table by logged user
    watch_item = WatchList.objects.filter(user_id=request.user, item_id=item_id).first()
    # Get the details for the item selected
    form = Listings.objects.get(pk=item_id)
    # Compare "item created by" with "logged user"
    is_owned = str(form.user) == str(request.user)
    # Obtain all current bids for the item
    all_bids = Bid.objects.filter(item_id=item_id).count()
    if not all_bids:
        winner1 = str(form.user)
        max_bid = form.start_price
    else:
        # Obtain max bid for the item
        x = Bid.objects.filter(item_id=item_id).aggregate(high_bid=Max('amount'))
        max_bid = x['high_bid']
        # Obtain winner (max Bid)
        y = Bid.objects.get(amount=max_bid)
        winner1 = y.user_id
    # Obtain all Comments for the item
    comments = Comments.objects.filter(item_id=item_id)

    return render(request, "auctions/item.html", {
        "item": form,
        "watch_item": watch_item,
        "is_owned": is_owned,
        "all_bids": all_bids,
        "max_bid": max_bid,
        "winner": winner1,
        "comments": comments
    })


@login_required(login_url='login')
def watchlist(request):
    # Display all items on the Watchlist DB table for logged user
    return render(request, "auctions/watchlist.html", {
        "items_list": WatchList.objects.filter(user_id=request.user)
    })


@login_required(login_url='login')
def add_watchlist(request):
    # Add an item to the Watchlist DB table for logged user
    user = User.objects.get(pk=int(request.user.id))
    item = Listings.objects.get(pk=int(request.POST["item_id"]))
    added_item = WatchList(user_id=user, item_id=item)
    added_item.save()
    return HttpResponseRedirect(reverse("item", kwargs={"item_id": request.POST["item_id"]}))


@login_required(login_url='login')
def remove_watchlist(request):
    # Delete an item from the Watchlist DB table for logged user
    user = User.objects.get(pk=int(request.user.id))
    item = Listings.objects.get(pk=int(request.POST["item_id"]))
    delete_item = WatchList.objects.filter(user_id=user, item_id=item).first()
    delete_item.delete()
    return HttpResponseRedirect(reverse("item", kwargs={"item_id": request.POST["item_id"]}))


@login_required(login_url='login')
def add_bid(request):
    if request.method == "POST":
        # Get all the info from the form
        amount = float(request.POST["item_bid"])
        user = User.objects.get(pk=int(request.user.id))
        item = Listings.objects.get(pk=int(request.POST["item_id"]))

        # Get initial price for item
        all_data = Listings.objects.get(id=request.POST["item_id"])
        price = all_data.start_price

        # Obtain max bid for the item
        x = Bid.objects.filter(item_id=item).aggregate(Max('amount'))
        max_bid = x['amount__max']
        if max_bid is None:
            max_bid = 0

        # If price is bigger than Start Price and Max Bid, save it on the DB
        if amount > price:
            if amount > max_bid:
                new_bid = Bid(amount=amount, user_id=user, item_id=item)
                new_bid.save()
                return HttpResponseRedirect(reverse("item", kwargs={"item_id": request.POST["item_id"]}))
            else:
                return render(request, "auctions/error.html", {
                    "message": 'Bid must be greater than Highest bid',
                    "item": all_data,
                    "comments": Comments.objects.filter(item_id=item),
                    "all_bids": Bid.objects.filter(item_id=item).count(),
                    "watch_item": WatchList.objects.filter(user_id=request.user, item_id=item).first(),
                    "max_bid": max_bid
                })
        else:
            return render(request, "auctions/error.html", {
                "message": 'Bid must be greater than Highest bid',
                "item": all_data,
                "comments": Comments.objects.filter(item_id=item),
                "all_bids": Bid.objects.filter(item_id=item).count(),
                "watch_item": WatchList.objects.filter(user_id=request.user, item_id=item).first(),
                "max_bid": max_bid
            })
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def add_comment(request):
    if request.method == "POST":
        text = request.POST["comment"]
        item_id = Listings.objects.get(pk=int(request.POST["item_id"]))
        user_id = User.objects.get(pk=int(request.user.id))
        add_a_comment = Comments(text=text, item_id=item_id, user_id=user_id)
        add_a_comment.save()
        return HttpResponseRedirect(reverse("item", kwargs={"item_id": request.POST["item_id"]}))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def close_listing(request):
    if request.method == "POST":
        user_id = int(request.POST["item_id"])
        # Get the details for the item selected
        close_item = Listings.objects.get(pk=int(request.POST["item_id"]))

        # Obtain all current bids for the item
        all_bids = Bid.objects.filter(item_id=int(request.POST["item_id"])).count()
        if not all_bids:
            winner = str(close_item.user)
            max_bid = close_item.start_price
            close_item.winner = winner
        else:
            # Obtain max bid for the item
            x = Bid.objects.filter(item_id=user_id).aggregate(high_bid=Max('amount'))
            max_bid = x['high_bid']
            # Obtain winner (max Bid)
            y = Bid.objects.get(amount=max_bid)
            winner = str(y.user_id)
            close_item.winner = winner
        close_item.closed = True
        close_item.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def all_closed_listings(request):
    # Calculate if there is a closed item or not on the DB
    x = Listings.objects.all()
    count = 0
    for item in x:
        if item.closed:
            count += 1

    return render(request, "auctions/close.html", {
        "all_items": Listings.objects.all(),
        "items_closed": count
    })


@login_required(login_url='login')
def categories(request):
    selected_categories = Listings.objects.values('category').distinct()
    return render(request, "auctions/all_categories.html", {
        "all_categories": selected_categories
    })


@login_required(login_url='login')
def category_page(request, name):
    items_category = Listings.objects.filter(category=name)
    return render(request, "auctions/each_category.html", {
        'items_category': items_category
    })
