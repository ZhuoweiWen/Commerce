from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import TextInput
from .models import *
from .choices import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max




#Default view
def index(request):
    #Listings.objects.all().delete()
    return render(request, "auctions/index.html", {
        "items" : Listings.objects.all().order_by('id').reverse(),
        "categories": CATEGORY_CHOICE
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
        return render(request, "auctions/login.html", {
            "categories": CATEGORY_CHOICE
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return render(request, "auctions/register.html", {
            "categories": CATEGORY_CHOICE
        })

# View for listing page
def listing(request, index):

    item = Listings.objects.get(pk=index)   
    bids = Bids.objects.filter(bid_listing=Listings.objects.get(pk=index))
    # Get the max bid of this item
    max_bid = bids.order_by('user_bid').reverse().first()
    comments = Comments.objects.filter(comment_listing=Listings.objects.get(pk=index))
    # Boolean for handling whether it is in watchlist
    inWatchlist = False
    # Boolean for if log in to determine whether can bid and post comment
    logIn = False
    # Boolean for if owner to allow close auction
    owner = False
    # Boolean for if user is the winner after listing closed
    winner = False
    # Boolean for if there is bids
    no_bid = False
    # Boolean for if the user has the current winning bid
    cur_winner = False
    bid_count = len(bids)

    if bid_count > 0:
        # Check if user is the winner after closing
        if item.closed and request.user == max_bid.user:
            winner = True
        # Check if user is the current winner before closing
        elif request.user == max_bid.user:
            cur_winner = True
    else:
        no_bid = True


    if request.user == item.user:
            owner = True

    if request.user.is_authenticated:
        logIn = True
        # Check if item is in watchlist    
        if WatchList.objects.filter(
            user=request.user, watchlist_item=item).exists():
            inWatchlist = True
    # Check if listing is closed and return all contexts
    if Listings.objects.get(pk=index).closed == True:
        return render(request, "auctions/listing.html",{
            "item" : item,           
            "inWatchlist": inWatchlist,
            "logIn" : logIn,
            "bids" : bids,
            "max_bid" : max_bid,
            "owner": owner,
            "winner": winner,
            "no_bid": no_bid,
            "comment_form": comment_Form(),
            "comments": comments,
            "categories": CATEGORY_CHOICE
        })

    else:
        if item != None:
            return render(request, "auctions/listing.html",{
                "item" : item,           
                "inWatchlist": inWatchlist,
                "logIn" : logIn,
                "bid_form" : bid_Form(),
                "bids" : bids,
                "max_bid" : max_bid,
                "owner": owner,
                "no_bid": no_bid,
                "comment_form": comment_Form(),
                "comments": comments,
                "cur_winner": cur_winner,
                "bid_count": bid_count,
                "categories": CATEGORY_CHOICE
            })

# View function for create listing page
@login_required(login_url='/login')
def create(request):

    if request.method == "POST":
        form = create_Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            imageURL = form.cleaned_data["url"]
            # Create and save listing
            item = Listings.objects.create(
                name = name,
                price = price,
                description = description,
                category = category,
                url = imageURL,
                user = request.user                
            )           
            item.save()
            return HttpResponseRedirect(reverse("index"))
        # Invalid submission return to page with user form
        else:
            return render(request, "auctions/create.html", {
                form: "form",
                "categories": CATEGORY_CHOICE
            })

    return render(request, "auctions/create.html", {
        "form":create_Form(),
        "categories": CATEGORY_CHOICE
    })


# View function for watchlist                
@login_required(login_url='/login')        
def watchlist(request):
    user_watchlist = request.user.my_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlists": user_watchlist,
        "categories": CATEGORY_CHOICE
    })

# View function for adding to watchlist
def watchlist_add(request, index):

    item_to_add = Listings.objects.get(pk=index)
    if WatchList.objects.filter(
        user=request.user, watchlist_item=item_to_add).exists():
        return HttpResponseRedirect(reverse('listing', args=(index,)))
    
    user_watchlist = WatchList.objects.create(user=request.user,
                            watchlist_item = item_to_add)
    user_watchlist.save()
    
    return HttpResponseRedirect(reverse('listing', args=(index,)))

# View function for watchlist remove in listing page
def listing_watchlist_remove(request, index):
    watchlist_remove(request = request, index= index)       
    return HttpResponseRedirect(reverse('listing', args=(index,)))

# View function for watchlist remove in watchlist page
def watchlistpage_watchlist_remove(request, index):
    watchlist_remove(request= request, index= index)
    return HttpResponseRedirect(reverse('watchlist'))


# View function for bidding
@login_required(login_url='/login')   
def bid(request, index):
    if request.method == 'POST':
        form = bid_Form(request.POST)
        if form.is_valid():
            cur_bid = form.cleaned_data["bid"]
            item_to_bid = Listings.objects.get(pk=index)
            bids = Bids.objects.filter(bid_listing=Listings.objects.get(pk=index))
            # Boolean for whether bid is successful
            success_bid = True

            # Handle all the cases when bidding is not successful
            if len(bids) > 0:
                max_bid = bids.order_by('user_bid').first()
                if cur_bid <= max_bid.user_bid:
                    messages.error(request, 'Error: Your bid must be higher than the current highest bid')
                    success_bid= False
            else:
                if cur_bid < item_to_bid.price: 
                    messages.error(request, 'Error: Your bid must be higher than the starting bid')
                    success_bid = False

            
            if success_bid:
                # Update bid is user already bided on this item
                check_bid = Bids.objects.filter(
                user=request.user, bid_listing=item_to_bid)
                if check_bid.exists():

                    check_bid.update(user_bid=cur_bid)

                # Create new valid bid
                else:
                    user_bid = Bids.objects.create(
                    starting_bid=item_to_bid.price,
                    user_bid=cur_bid,
                    user=request.user,
                    bid_listing=item_to_bid

                )

                    user_bid.save()
                    messages.success(request, 'Successfully placed bid')

    return HttpResponseRedirect(reverse('listing', args=(index,)))

# View function for closing auction
def close(request, index):
    if request.method == 'POST':
        item_to_close = Listings.objects.get(pk=index)
        item_to_close.closed = True
        item_to_close.save()
        return HttpResponseRedirect(reverse('listing', args=(index,)))

# View function for comment
def comment(request, index):

    if request.method == 'POST':
        form = comment_Form(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            new_comment = Comments.objects.create(
                comment_listing= Listings.objects.get(pk=index),
                comment_section= comment,
                user=request.user
            )

            new_comment.save()

            

            return HttpResponseRedirect(reverse('listing', args=(index,)))
        else:
            return render(request, "auctions/listing.html", {
                form: "form"
            })

# View function for category page 
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORY_CHOICE
    })

# View function for category query result
def categories_search(request, index):
    item_in_category = Listings.objects.filter(category=index)
    title = CATEGORY_CHOICE[index][1]

    return render(request, "auctions/categories_search.html",{
        "item_in_category": item_in_category,
        "title": title,
        "categories": CATEGORY_CHOICE
    })

# Helper method for removal from watchlist
def watchlist_remove(request, index):
    item_to_remove = Listings.objects.get(pk=index)
    if WatchList.objects.filter(
        user=request.user, watchlist_item=item_to_remove).exists():
        request.user.my_watchlist.get(watchlist_item=item_to_remove).delete()
        


        
    
    
