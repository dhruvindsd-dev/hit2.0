"""hit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:     path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import login_view, create_user_view, otp_check
from hit_book.views import *
handler404 = 'hit_book.views.handler404'
handler500 = 'hit_book.views.handler500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/<int:post_id>', login_view),  # for obvious login purposes. 
    path('login/', login_view),  # for obvious login purposes. 
    path('signup', create_user_view), # for creatig a new user 
    path('signup/<str:validation>', otp_check), # for creatig a new user 
    path('home/', main_view), # loged in biitch.
    path('book/<int:book_id>',show_all_books_post_view),  # show all posts of the book id given except the general posts 
    path('all_books/',show_all_books),  # show all posts of the book id given except the general post      
    path('create/new_book/', create_new_book),
    path('create/new_hit/<int:book_id>/', create_hit_post),# new hit in a book. 
    path('create/new_hit/', create_hit_post),  # random hit.
    path('view/hit/<int:hit_id>/', hit_selected_view),# view a hit  
    path('update/<int:hit_id>/', update_hit_view),# update the selected hit   
    path('img_link/<str:to_search>/<int:page_no>', images_select),
    path('save/<str:img_link>', save_complete_post_with_img),
    path('delete/<int:id>/<str:delete>', delete_post),
    path('delete/<int:id>/', delete_post),
    path('schedule/<int:hit_post_id>/', schedule_posts),
    path('', about),
    path('logout/', logout),

]
