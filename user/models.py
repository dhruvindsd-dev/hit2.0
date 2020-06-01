from django.db import models

# Create your models here.
class User_db(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=20)

    @staticmethod
    def login_check(username, password):
        user = User_db.objects.filter(user_name=username, password=password)
        if len(user) == 0:
            return False, False
        return True, user[0].id

    def create_user(self):  # create_userate a user
        User_db.objects.create(user_name=self.user_name, email=self.email, password=self.password)

     
        
