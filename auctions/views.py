from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User,category,listing,comments,Bid


def index(request):
    auclist = listing.objects.filter(status = True)
    allcategory = category.objects.all()
    return render(request, "auctions/index.html", {"listing":auclist, "categories":allcategory})


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
        return render(request, "auctions/register.html")

@login_required(login_url="login")   
def create(request):
    if request.method == "GET":
        categories = category.objects.all()
        return render(request, "auctions/create.html", { "category":categories})
    
    elif request.method == "POST":
        tit = request.POST["title"]
        cat = request.POST["category"]
        URL = request.POST["img_url"]
        des = request.POST["description"]
        bid = request.POST["starting_bid"]
        user = request.user
        categorydata = category.objects.get(categoryName = cat)
        cd = Bid(bid_amt = bid, bidder = user, bid_count = 0, initial_bid = bid)
        cd.save()
        new_listing = listing(
            title=tit,
            category=categorydata,
            img_url=URL,
            description=des,
            price = cd,
            publisher = user
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    

def disp_category(request):
    if request.method == "POST":
        cat = request.POST["category"]
        catmain = category.objects.get(categoryName= cat)
        item_to_disp = listing.objects.filter(category=catmain, status=True)
        allcategory = category.objects.all()
        return render(request, "auctions/index.html", {"listing": item_to_disp, "categories": allcategory})


def list(request, listing_id):
    if request.method == "GET":
        item = listing.objects.get(id=listing_id)
        currentuser = request.user
        determine_watchlist = currentuser in item.watchlist.all()
        cat = category.objects.get(categoryName = item.category)
        allcomment = comments.objects.filter (comment_listing = item)
        if request.user == item.publisher:
            button = True
        else:
            button = False
        return render(request, "auctions/listing.html", {"lists":item, "category":cat, "determine":determine_watchlist, "allcomment":allcomment, "bt":button})
    elif request.method == "POST":
            item = listing.objects.get(id=listing_id)
            if request.user == item.publisher:
                item.status = False
                item.save()
                message = "Closed the auction successfully"
                messages.add_message(request, messages.SUCCESS, message)
                return HttpResponseRedirect(reverse('index'))
            else :
                amount = request.POST["bidding-amount"]
                if item.status == True:
                    if int(amount) > item.price.bid_amt:
                        item.price.bid_amt = amount
                        item.price.bidder = request.user
                        item.price.save()
                        message = "Your bid has been placed"
                        messages.add_message(request, messages.SUCCESS, message) 
                    else:
                        message = "Bid should be more than the current bid"
                        messages.add_message(request, messages.ERROR, message)  
                    return HttpResponseRedirect(reverse('list', args=[listing_id]))
                
                elif item.status == False:
                    if item.price.bidder == request.user:
                        message = "You won the auction !!!"
                        messages.add_message(request, messages.SUCCESS, message)
                        return HttpResponseRedirect(reverse('index'))
                    else :
                        message = "Sorry the auction has been closed"
                        messages.add_message(request, messages.ERROR, message)
                        return HttpResponseRedirect(reverse('index'))

    
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listingdata = listing.objects.get(id = listing_id)
        usertoadd = request.user
        listingdata.watchlist.add(usertoadd)
        listingdata.save()
        return HttpResponseRedirect(reverse('list', args=[listing_id]))
    
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        listingdata = listing.objects.get(id = listing_id)
        usertoadd = request.user
        listingdata.watchlist.remove(usertoadd)
        listingdata.save()
        return HttpResponseRedirect(reverse('list', args=[listing_id]))

def disp_watchlist(request):
    currentuser = request.user
    watlist = listing.objects.filter(watchlist = currentuser)
    allcategory = category.objects.all()
    return render(request, "auctions/index.html", {"listing":watlist, "categories":allcategory})


def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        commentofuser = request.POST["comment"]
        item = listing.objects.get(id = listing_id)
        newcomment = comments(comment = commentofuser, comment_user=user, comment_listing=item)
        newcomment.save()
    return HttpResponseRedirect(reverse('list', args=[listing_id]))