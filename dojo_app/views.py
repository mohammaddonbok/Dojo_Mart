from django.shortcuts import render , HttpResponse ,redirect
from django.http import JsonResponse
from .models import *
import re ,bcrypt

def root(request):
    # if 'category_id'  not in request.session:
    #     specific_category=get_Category(id=1)
    #     category=Category.objects.all()
    #     all_products=specific_category.products.all
    # else:
    specific_category=get_Category(id=request.session['category_id'])
    category=Category.objects.all()
    all_products=specific_category.products.all
    if 'user_id' not in request.session:
        context={
            "signin":True,
            "logout":False,
            "admin":False,
            "All_category":category,
            "all_products":all_products
        }
        
        return render(request,"homePage.html", context)
    else:
        user=get_user(request.session['user_id'])
        role=user.role.role
        context={
            "signin":False,
            "logout":True,
            "admin":role
        }
        return render(request,"homePage.html",context)

def showSignInForm(request):

    return render(request,"signinForm.html")
def showCreateAccountForm(request):
    return render(request,"registerForm.html")

def showCartForm(request):

    return render(request,"cartForm.html")
# Create your views here.
def addCategory(request):
    """
    only the admin can add to category
    this method to add title and image to a category
    """ 
    if request.method=="POST":
        title=request.POST['title']
        image=request.FILES['img']
        add_Category(title=title,image=image)
    return redirect('/admin')

def addUser(request):
    """
    this method to register and  check if the data is validate
    if validate add the user to a database
    this method use ajax to check email is validate or not
    the attribute email: the email from form registerForm.html
    
    """
    print("iam here*******************************************************************")
    if request.method=="POST":
        errors={}
        email = request.POST['email']
        firstName=request.POST['fname']
        lastName=request.POST['lname']
        password=request.POST['password']
        if not validate_email(email):
            errors['email']="Email not valid"
        if is_duplicate_email(email):
            errors['email']="sorry email in use ,choose another email"
        
        if not validate_text(firstName):
            errors['firstName']="the name should be a text and greater the length grather than two "
        if not validate_text(lastName):
            errors['firstName']="the name should be a text and greater the length grather than two "
        if not validate_text(password, min_length=8):
            errors['password']="the length of password shoud be at least 8 charecter"
            return  JsonResponse(errors)
        if validate_name(firstName) and validate_text(firstName)and validate_name(lastName)and validate_text(lastName)and validate_email(email)and not is_duplicate_email(email):
            if 'user_id' not in request.session:
                print("not in create")
                passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                role=role_user()
                user=add_user(firstName,lastName,email,passwd,role)
                request.session['user_id']=user.id

                request.session['first_name']=user.first_name
                request.session['last_name']=user.last_name
                return redirect('/')
    return redirect('/')
def validateEmailByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the email is valid or not and return a json.
    the returnd json  carry a message if email is invalid
    the length of the message will be zero if the email valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        msg['email']=''
        email=request.POST['email']
        if not validate_email(email):
            msg['email']="Email not valid"
            return JsonResponse(msg)
        if is_duplicate_email(email):
            msg['email']="sorry email in use ,choose another email"
        return JsonResponse(msg)
    return redirect('/')

def validateFirstNameByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the first name is valid or not and return a json.
    the returnd json  carry a message if first name is invalid
    the length of the message will be zero if the first name valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        msg['fname']=''
        firstName=request.POST['fname']
        if not validate_text(firstName):
            msg['fname']="the name should be a text and greater the length grather than two "
            return JsonResponse(msg)
        if not validate_name(firstName):
            msg['fname']="The first name should be a text"
        return JsonResponse(msg)
    return redirect('/')

def validateLastNameByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the last name is valid or not and return a json.
    the returnd json  carry a message if last name is invalid
    the length of the message will be zero if the last name valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        msg['lname']=''
        lastName=request.POST['lname']
        if not validate_text(lastName):
            msg['lname']=" the length should be  grather than two "
            return JsonResponse(msg)
            if not validate_name(lastName):
                msg['lname']="The first name should be a text"
        return JsonResponse(msg)
    return redirect('/')

def validatePasswordByAjax(request):
    """
    this method recieve the request that will be sent by ajax
    to check if the password is valid or not and return a json.
    the returnd json  carry a message if password is invalid
    the length of the message will be zero if the password valid
    if the request.method does not equal post then redirect to homepage
    """
    if request.method=="POST":
        msg={}
        password=request.POST['password']
        msg['password']=''
        if not validate_text(password, min_length=8):
            msg['password']="the length of password shoud be at least 8 charecter"
        return JsonResponse(msg)
    return redirect('/')


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
            return True
    return False
    

def validate_text(text, min_length=2):
    verified = True
    if not text:
        verified = False
    elif len(text) < min_length:
        verified = False
    return verified
def validate_name(name):
    NAME_REGEX=re.compile(r'^[a-zA-Z]+$')
    if not NAME_REGEX.match(name):
        return False
    return True

def logout(request):
    print('not in ***********logout')
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['first_name']
        del request.session['last_name']
    print('not in ***********logout')
    return redirect('/')
def signin(request):
    print("**************************************************************************")
    email=request.POST['email']
    password=request.POST['password']
    user=get_userByEmail(email)
    if(user):
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session["user_id"]=user.id
            request.session["first_name"]=user.first_name
            request.session["last_name"]=user.last_name
            return redirect('/')
    return redirect('/show_sign_in_form')

def edit_product_form(request,id):
    context={
        "product":Product.objects.get(id=id),
        "categories":Category.objects.all()
    }
    return render(request, "edit_product.html",context)



def edit_product(request,id):
        if request.method=="POST":
            n=request.POST['name']
            desc=request.POST['description']
            p=request.POST['price']
            q=request.POST['quantity']
            image=request.FILES['img']
            cat=request.POST['category']
            product_id=id
            product_to_edit(n,desc,p,q,image,cat,product_id)
        return redirect('/admin')


def showadminpage(request):
    """
    in the sign in method (after the query to get the user) if the user.role.role==1 request.session['admin_id'] =user.id redirect to a url with a method that render the admin page
    """
    # if 'admin_id' in request.session :
    context={
            "categories":Category.objects.all(),        
        }
    return render(request, "admin_interface.html", context)

def suggestion(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.name)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render (request, "homePage.html")


def add_product_form(request):
    context={
        "categories":Category.objects.all()
    }
    return render(request,"add_product.html", context)


def add_product(request):
    if request.method=="POST":
        n=request.POST['name']
        desc=request.POST['description']
        p=request.POST['price']
        q=request.POST['quantity']
        image=request.FILES['img']
        cat=request.POST['category']
        product_to_add(n,desc,p,q,image,cat)
        return redirect('/admin')


def showCatgeoryProducts(request,category_id):
    if 'category_id'  not in request.session:
        request.session['category_id']=category_id
        
    else:
        del request.session['category_id']
        request.session['category_id']=category_id
    return redirect('/')

