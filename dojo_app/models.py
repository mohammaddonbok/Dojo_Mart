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
    image=models.ImageField(null=True,blank=True, upload_to="images/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Product(models.Model):
    name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    quantity=models.IntegerField()
    image=models.ImageField(null=True,blank=True,upload_to="images/")
    description=models.TextField()
    category=models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Order(models.Model):
    totalCharge=models.DecimalField(max_digits=5,decimal_places=2)
    address=models.CharField(max_length=255)
    numberOfItem=models.IntegerField()
    phone_number=models.CharField(max_length=25)
    products=models.ManyToManyField(Product,related_name="order",through="Cart")
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,related_name="who_purchased",on_delete=models.CASCADE)

class Cart(models.Model):
    quantity=models.IntegerField()
    order=models.ForeignKey(Order,related_name="cart",on_delete=models.CASCADE)
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

def add_user(first_name,last_name,email,password):
    """
    Create a record in User table
    """
    pass


