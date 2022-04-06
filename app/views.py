from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


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
                               , [request.POST['username'], request.POST['phoneno'], request.POST['password1']])
                newuser = form.save()
                login(request, newuser)
                messages.success(request, ("Registration successful. Welcome, {username}!"))
                return redirect('login')
            else:
                messages.success(request, ("Username or Phone Number already taken. Please Try Again."))
                return redirect('register')

    form = NewUserForm()
    return render(request, "app/register.html", {})


def sell(request):
    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO products(sellerid, name, description, price, category, allergen, minorder) VALUES (%s, %s, %s, %s, %s, %s, %s)", [request.POST['username'], request.POST['foodname'], request.POST['description'], request.POST['price'], request.POST['category'], request.POST['allergen'], request.POST['minorder'] ])
            return redirect('home')
    return render(request, "app/sell.html")


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
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM allusers WHERE userid = %s", [username])
                account = cursor.fetchone()
                if account[2] == password and account is not None:
                    created = User.objects.create_user(username, str(account[1]), password)
                    #created = NewUserForm(username, str(account[1]), password, password)
                    #created = UserCreationForm(account)
                    #user = NewUserForm(created)
                    #login_user = created.save()
                    login(request, created)
                    messages.success(request, f'Welcome, You logged in to {username}')
                    return redirect('home')
                else:
                    messages.success(request, f'Invalid. Please Try Again :(')
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
        cursor.execute("SELECT * FROM allusers WHERE userid =  %s",[id])
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM transactions WHERE b_id =%s", [id])
        trans = cursor.fetchall()
        cursor.execute("SELECT * FROM products WHERE sellerid =%s", [id])
        list = cursor.fetchall()

    result_dict = {'user': user}

    return render(request, 'app/profile.html', {'user': user, 'list':list, 'trans':trans})


def view(request, id):
    """Shows the main page"""
    ##Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid = %s", [id])
        customer = cursor.fetchone()
        cursor.execute("SELECT SUM(qty) FROM transactions WHERE p_id = %s", [id])
        order = cursor.fetchone()
        if order is None:
            order = 0
    result_dict = {'cust': customer}

    ##use raw query to get the current orders
    # with connection.cursor() as cursor:
    # cursor.execute("SELECT SUM(qty) FROM transactions WHERE p_id = %s", [id])
    # status = cursor.fetchall
    # result_dict = {'status': status}

    return render(request, 'app/view.html', {'cust':customer, 'order':order})


def search_products(request):
    qns = request.POST['searched']
    qns = "%" + qns + "%"
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE lower(name) LIKE lower(%s)", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_products.html', result_dict)


def search_users(request):
    qns = request.POST['searched']
    qns = "%" + qns + "%"
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE lower(name) LIKE lower(%s)", [qns])
        searched = cursor.fetchall()
    result_dict = {'searched': searched}

    return render(request, 'app/search_users.html', result_dict)


def user_purchase(request, id):
    # context = {}
    # status = ''
    # phoneno = request.phoneno
    # if request.POST['action'] == "purchase":
    # with connection.cursor() as cursor:
    # cursor.execute("INSERT INTO transactions(productid, sellerid, name, description, price, category, allergen, minorder) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # , [request.POST["productid"], request.POST["sellerid"], request.POST["name"], request.POST["description"],
    #  request.POST["price"], request.POST["category"], request.POST["allergens"], request.POST["minorder"] ])
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM(qty) FROM transactions WHERE p_id = %s", [id])
        transactions = cursor.fetchall()
        if transactions is None:
            transactions = 0
    result_dict = {'transactions': transactions}
    return render(request, 'app/purchase.html', result_dict)


def purchase_more(request):
    if request.POST['action'] == "backhome":
        return redirect('home')


def admin_users(request):
    """Show list of allusers with buttons to edit/delete"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM allusers WHERE phoneno = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers ORDER BY phoneno")
        user = cursor.fetchall()

    result_dict = {'user': user}

    return render(request, 'app/admin_users.html', result_dict)


def admin_users_edit(request, id):
    """Shows the admin_users_edit page"""

    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE phoneno = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE allusers SET userid = %s, password = %s, phoneno = %s WHERE phoneno = %s"
                , [request.POST['user_id'], request.POST['password'], request.POST['phoneno'], id])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM allusers WHERE phoneno = %s", [id])
            obj = cursor.fetchone()

    context["obj"] = obj
    context["status"] = status

    return render(request, "app/admin_users_edit.html", context)
