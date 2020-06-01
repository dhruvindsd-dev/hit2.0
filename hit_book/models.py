from django.db import models
import datetime


# Create your models here.
# if the user wishes to create a entire new class of books he can do so by enabling the following option .
class hit_book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user_id = models.CharField(max_length=10)
    
class hit_post(models.Model):
    title = models.CharField(max_length=150)
    s_description = models.CharField(max_length=150)
    content = models.TextField()
    # hash_tags = models.CharField(max_length=500)
    # private = models.BooleanField(default=False)
    book_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    img_link = models.CharField(max_length=356, default=None)
    # for the email scheduling
    time_for_next_email = models.CharField(max_length=100, default=None, null=True)  # if 0 then sent the email the the user on the reminded post with the link 
    period = models.CharField(max_length=30, default=0, null=True)  # the period in which the user wants to be reminded about the post 
    custom_message = models.CharField(max_length=150, default=0, null=True)  # a custom message the user want to be reminded of while sending the email.
    times = models.CharField(max_length=150, default=0, null=True)  # the max limit the user wants to be reminded...
    counter = models.CharField(max_length=150, default=0, null=True)  # the user selectis how many no of times does he want to review the post 