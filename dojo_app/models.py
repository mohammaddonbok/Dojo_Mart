from django.db import models
class Role(models.Model):
    role=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    role=models.ForeignKey(Role,related_name="user_admin",on_delete=models.CASCADE)

class Category(models.Model):
    title=models.CharField(max_length=255)
    image=models.ImageField(null=True,blank=True, upload_to="categories/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Product(models.Model):
    name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    quantity=models.IntegerField()
    image=models.ImageField(null=True,blank=True,upload_to="products/")
    description=models.TextField()
    category=models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Order(models.Model):
    totalCharge=models.DecimalField(max_digits=5,decimal_places=2)
    address=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=25)
    products=models.ManyToManyField(Product,related_name="order",through="Cart")
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,related_name="who_purchased",on_delete=models.CASCADE)

class Cart(models.Model):
    quantity=models.IntegerField()
    order=models.ForeignKey(Order,related_name="cart",on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,related_name="cart",on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name="cart",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

def add_Category(title,image):
    """
    Create a record in Category tabel
    """
    newCategory=Category.objects.create(title=title, image=image)
    return newCategory
def add_role(role):
    """
    Create  a record  in Role tabel
    """
    roleOfUser=Role.objects.create(type=role)
    return roleOfUser

def add_user(first_name,last_name,email,password,typeOfUser):
    """
    Create a record in User table
    """
    user=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password,role=typeOfUser)
    return user

def get_Category(id):
    """
    bring specicfic category and return it 
    """
    category= Category.objects.get(id=id)
    return category

def is_duplicate_email(email):
    """
    this method to cheack if email is duplicated or not that take email and filter it
    in database and if len email grater true then return true
    """
    users = User.objects.filter(email=email).values()
    if len(users):
        return True
    return False

def role_admin():
    admin=Role.objects.get(id=1)
    return admin

def role_user():
    user=Role.objects.get(id=2)
    return user
def get_user(id):
    user = User.objects.get(id=id)
    return user
def get_userByEmail(email):
    user=User.objects.filter(email=email)
    if(len(user)>0):
        return user[0]
    return None

def product_to_add(name,description,price,quantity,image,category):
    category=Category.objects.get(title=category)
    product=Product.objects.create(name=name, description=description,quantity=quantity, price=price,image=image,category=category)
    return product

def product_to_edit(n,desc,p,q,image,cat,product_id):
    category=Category.objects.get(title=cat)
    product=Product.objects.get(id=product_id)
    product.name=n
    product.description=desc
    product.price=p
    product.quantity=q
    product.image=image
    product.category=category
    product.save()
