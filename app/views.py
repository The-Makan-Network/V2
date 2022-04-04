from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm

# Create your views here.
def home(request):
    """Shows the product listing page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products ORDER BY productid")
        products = cursor.fetchall()

    result_dict = {'products': products}

    return render(request, 'app/home.html', result_dict)



# Create your views here.
def register(request):

    if request.POST:
        form = NewUserForm(request.POST)
        ## Check if userid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [request.POST['username']])
            user = cursor.fetchone()
            ## No customer with same id
            if not form.is_valid():
                messages.success(request, ("Password does not pass requirements. Please try again."))
                return redirect('register')
            elif user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO allusers(userid, phoneno, password) VALUES (%s, %s, %s)"
                        , [request.POST['username'], request.POST['phoneno'], request.POST['password1'] ])
                newuser = form.save()
                login(request, newuser)
                messages.success(request, ("Registration successful. Welcome, {username}!"))
                return redirect('login')
            else:
                messages.success(request, ("Username or Phone Number already taken. Please Try Again."))
                return redirect('register')
		
    form = NewUserForm()
    return render(request, "app/register.html", {})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, You logged in to {user.username}')
            return redirect('home')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again."))	
            return redirect('login')	


    else:
        return render(request, 'app/login.html', {})

def signout(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('home')
			
		
def profile(request, id):
    """Shows the main page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE sellerid =  %s",[id])
        user = cursor.fetchone()

    result_dict = {'product': user}

    return render(request, 'app/profile.html', result_dict)


def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)
