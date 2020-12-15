from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):    #check format of email
            errors['email'] = 'Invalid Email Address'
        
        existing_user = User.objects.filter(email=postData['email'])
                # email_check = self.filter(email=postData['email'])
                # if email_check:
                #     errors['email'] = "Email already in use"
        if len(existing_user) !=0:
            errors['email'] = "Email already in use"
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'        
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = 'Password and Confirm Password must match'  #don't tell them which one is wrong!
        
        return errors
      
    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(postData['email']):    #check format of email
            errors['email'] = 'Invalid Email Address'
    
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) !=1:      #now checking that at least one is found
            errors['user'] = "User not found"
    
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'        
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:  #authenticate
            errors['email'] = 'Email and Password do not match'  #don't tell them which one is wrong!
        
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()
    
#-------------------end of USER ---------------------------------------------------------
    
  
#ADD Manager classes here ----------------------------
#START application here---------------------------------------
