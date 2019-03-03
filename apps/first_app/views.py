from django.shortcuts import render, HttpResponse, redirect
from .models import User, Wish
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,"wishing_app/index.html")
def process(request):
    print(request.POST)
    errors = User.objects.validate(request.POST)
    if errors:
        for error in errors:
            messages.error(request,error)
        return redirect("wishing_app:index")
    user_id = User.objects.create_user(request.POST)
    print(user_id)
    return redirect("wishing_app:index")
def login(request):
    print(request.POST)
    valid,result = User.objects.login(request.POST)
    if not valid:
        messages.error(request,result)
        return redirect("wishing_app:index")
    request.session['user_id']= result
    return redirect("wishing_app:dashboard")
def dashboard(request):
    context={
        
        "user" :  User.objects.get(id=request.session['user_id']),
        "wishes" : Wish.objects.filter(user_id=request.session['user_id']),
        "granted_wish" : Wish.objects.filter(grant_status="granted")
    }
    return render(request,"wishing_app/dashboard.html",context)
def create(request):
    context={
        
        "user" :  User.objects.get(id=request.session['user_id'])
         }
    return render(request,"wishing_app/create.html",context)
def create_wish(request):
    print(request.POST)
    errors = Wish.objects.validate(request.POST)
    if errors:
        for error in errors:
            messages.error(request,error)
        return redirect("wishing_app:create")
    wish_id = Wish.objects.create_wish(request.POST,user_id = request.session['user_id'])
    
    print(wish_id)
    return redirect("wishing_app:dashboard")
def edit(request,id):
    context={
        "wish":Wish.objects.get(id=id),
        "user":  User.objects.get(id=request.session['user_id'])
    }
    return render(request,"wishing_app/edit.html",context)
def update(request,id):
    errors = Wish.objects.validate(request.POST)
    if errors:
        for error in errors:
            messages.error(request,error)
            return redirect("/{}/edit".format(id))   
    else:
        wish = Wish.objects.get(id = id)
        wish.wish = request.POST['wish']
        wish.desc = request.POST['description']
        wish.save()
    return redirect("wishing_app:dashboard")
def grant(request,id):
    wish = Wish.objects.get(id = id)
    wish.grant_status = "granted"
    wish.save()
    print(wish)
    return redirect("wishing_app:dashboard")
def destroy(request,id):
    wish=Wish.objects.get(id=id)
    wish.delete()
    return redirect("wishing_app:dashboard")
def like(request,id):
    likes = Wish.objects.add_like(user_id=request.session['user_id'],wish_id=id)
    return redirect("wishing_app:dashboard")
def stats(request):
    context={
        "user" :  User.objects.get(id=request.session['user_id']),
        
        "grants":Wish.objects.filter(grant_status="granted").count(),
        "wishes" : Wish.objects.filter(user_id=request.session['user_id']).exclude(grant_status="granted").count(),
        "no_wishes" : Wish.objects.filter(user_id=request.session['user_id']).exclude(grant_status="not_granted").count()
    }
    return render(request,"wishing_app/stats.html",context)
def logout(request):
    request.session.clear()
    return redirect("wishing_app:index")
