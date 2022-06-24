from django.db import models

# Create your models here.
class Index(models.Model):
    image = models.ImageField( 
                        upload_to='media/',
                        null=True,
                        blank=False,
                        )
    def __str__(self):
        return self.image
        
class Register(models.Model):
    # id = models.IntegerField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    date = models.DateField(default=" ")
    plan = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Profile(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default=" ")
    email = models.CharField(max_length=100,default=" ")
    phone = models.CharField(max_length=10,default=" ")
    address = models.TextField()
    country = models.CharField(max_length=200,default=" ")
    #dp = models/models.ImageField(_(), upload_to=None, height_field=None, width_field=None, max_length=None)
    #website = models.CharField(max_length=100,default=" ")
    
    def __str__(self):
        return self.name

class Item(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    total_item = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    hobby = models.CharField(max_length=50)
    income = models.CharField(max_length=100)
    except_amount = models.IntegerField(blank=False, null=True)
    age = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField( 
                        upload_to='media/',
                        null=True,
                        blank=False,
                        )


    def __str__(self):
        return self.name

class Store(models.Model):
    # id = models.AutoField(primary_key=True, editable=True)
    product_name = models.CharField(max_length=100)
    in_stock = models.IntegerField(editable=True)
    price = models.IntegerField(editable=True)
    image1 = models.ImageField( 
                            upload_to='store/',
                            null=True,
                            blank=False,
                            )
    image2 = models.ImageField( 
                            upload_to='store/',
                            null=True,
                            blank=False,
                            )
    image3 = models.ImageField( 
                            upload_to='store/',
                            null=True,
                            blank=False,
                            )
    condition = models.CharField(max_length=100, default='')

    def __str__(self):
            return self.product_name
