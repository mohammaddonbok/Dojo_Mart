from django.shortcuts import render , HttpResponse ,redirect
from .models import *

def root(request):

    return render(request,"homePage.html")

def showSignInForm(request):

    return render(request,"signinForm.html")
def showCreateAccountForm(request):
    return render(request,"registerForm.html")

def showCartForm(request):

    return render(request,"cartForm.html")
# Create your views here.
def addCategory(request):
    """
    Not complete.............................................
    only the admin can add to category
    this method to add title and image to a category
    """ 
    if request.method=="POST":
        title=request.POST['title']
        image=request.FILES['img']
        add_Category(title=title,image=image)
    return redirect('/')
    def addProduct(request):
        pass
