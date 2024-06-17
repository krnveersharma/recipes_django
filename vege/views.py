from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

#login is used for session

# Create your views here.

@login_required(login_url="/login") #can't access recipes without login
def recipes(request):
    queryset=Recipe.objects.all()
    context={'recipes':queryset}
    if request.method == "POST":
        data=request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES['recipe_image']
        Recipe.objects.create(
            user=request.user,
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description
        )
        return redirect('/recipes/')
    return render(request,'recipes.html',context)

def update_recipe(request,id):
    if(request.method=="POST"):
        data=request.POST
        queryset=Recipe.objects.get(id=id)
        queryset.recipe_name=data.get('recipe_name')
        queryset.recipe_description=data.get('recipe_description')
        queryset.recipe_image=request.FILES['recipe_image']
        queryset.save()
        return redirect('/recipes/')
    queryset=Recipe.objects.get(id=id)
    context={'recipe':queryset}
    return render(request,'update_recipe.html',context)

def delete_recipe(request,id): #it is managinf dynamic urls as we are passing id too
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

def login_page(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password) #authenticate user
        if user is not None:
            login(request,user) #creating session
            return redirect("/recipes")
        else:
            print("Not valid user")
    return render(request,"login_page.html")

def logout_page(request):
    logout(request)
    return redirect('/login')
 
def register(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password) #TO encrypt password
        user.save()
        return redirect("/login")
    return render(request,"register.html")