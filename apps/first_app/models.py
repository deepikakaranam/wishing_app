from django.db import models
import re 
import bcrypt

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate(self, form_data):
        errors = []
        if len(form_data['first_name'])<2:
            errors.append("first name should be more than 2 characters")
        if len(form_data['last_name'])<2:
            errors.append("Last name should be more than 2 characters")
        if len(form_data['password'])<8:
            errors.append("Password should be more than 8 characters")
        if len(form_data['password'])!= len(form_data['confirm_password']):
            errors.append("Passwords donot match")

        if not EMAIL_REGEX.match(form_data['email']):
            errors.append("Email must be valid")
        user_list = User.objects.filter(email=form_data['email'])
        if user_list:
            errors.append("Email already exits")
        return errors
    def create_user(self, form_data):
        hashed_pw=bcrypt.hashpw(form_data['password'].encode(),bcrypt.gensalt())
        print(hashed_pw)
        hashed_confirm=bcrypt.hashpw(form_data['confirm_password'].encode(),bcrypt.gensalt())
        
        user= User.objects.create(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            password=hashed_pw,
            confirm_password=hashed_confirm
                 
        )
        print("working", user)
        return user.id
    def login(self, form_data):
        errors=[]
        existing_user = User.objects.filter(email=form_data['email'])
        if not existing_user:
            return (False,"Email or password invalid")
        user = existing_user[0]
        print(user)
        if bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
            return(True ,user.id)
class WishManager(models.Manager):
    def validate(self, form_data):
        errors = []
        if len(form_data['wish'])<3:
            errors.append("A wish must consist atleast 3 characters")
        if len(form_data['description'])<1:
            errors.append("A description must be provided")
               
        return errors
    def create_wish(self, form_data,user_id):
        user = User.objects.get(id=user_id)
        wish= Wish.objects.create(
            wish = form_data['wish'],
            desc = form_data['description'],
            user= user
            
                 
        )
        print("working", wish)
        return wish.id   
    def add_like(self, wish_id, user_id):
        user= User.objects.get(id=user_id)
        wish = Wish.objects.get(id=wish_id)
        likes = user.likes.add(wish)
        return likes
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length= 255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Wish(models.Model):
    wish = models.CharField(max_length = 255)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name="user_wish")
    grant_status = models.CharField(max_length = 255, default="not_granted")
    user_liked = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
   

