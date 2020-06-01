from django.shortcuts import render,redirect
from django.core.exceptions import SuspiciousOperation
from .models import *  
from django.http import HttpResponseRedirect
from .scrape import get_image_from_tag
# Create your views here.
# all the views related to main screen where there are lists of
# hashtags. 
# all the hits. 
# option to sort on the basis of books.
# option to sort eveything on the basis of hash tags. 


def main_view(request):  # main page , shows posts and books
	if request.session['user_id_hit'] is None:
		raise HttpResponseNotFound
	posts = hit_post.objects.filter(user_id=request.session['user_id_hit']).reverse()
	books = hit_book.objects.filter(user_id=request.session['user_id_hit']).exclude(title='general', description='general')
	# defaults
	context = {
        'hits': posts,
        'books': books,
    }
	return render(request, 'home.html', context)


def create_new_book(request):  # create a new book , on saving redirect to new hit_post 
	if request.POST:	
		hit_book.objects.create(title=request.POST['nb_title'], 
								description=request.POST['nb_description'],
								user_id=request.session['user_id_hit']
								)
		book_id = str(hit_book.objects.latest('id').id) # getting the latest id of the cerated book		
		return redirect(f'/create/new_hit/{book_id}')
	return render(request,'create/new_book.html')


def create_hit_post(request, book_id=None): #random hit of book_id is None else hit in book 
	if book_id is None:  # general hit
		book_id = str(hit_book.objects.get(title='general',user_id=request.session['user_id_hit']).id)
		context = {'title': 'Create hit'}
	else :  # hit under new book
		book_id = book_id # getting the latest id of the cerated book
		context= {'title':'Create hit for book '}	
	if request.POST:
		context['hit'] = None  # so that i can use this template in the update process of the hit_post 
		# if 'rh_private' in request.POST: val = True  # for checkbutton  
		# else: val = False
		request.session['hit_post_data'] = {'title':request.POST['rh_title'],
								's_description':request.POST['rh_s_description'], 
								'content':request.POST['rh_content'], 
								# 'hash_tags':request.POST['rh_hash_tags'],
								# 'private':val,
								'book_id': book_id, 
								'user_id': request.session['user_id_hit']
								}
								# redirecting the user to seelt the images
		return redirect(f'/img_link/food/1')							
	return render(request, 'create/random_hit.html', context)


def show_all_books_post_view(request, book_id):
	# show all the posts of the book id entered and the user obviously
	hit = hit_post.objects.filter(book_id=book_id, user_id=request.session['user_id_hit'])
	book = hit_book.objects.get(id=book_id,user_id=request.session['user_id_hit'])
	context = {
	'hit': hit,
	'book': book 
	}
	return render(request,'book_posts.html', context)

def show_all_books(request):
	books = hit_book.objects.filter(user_id=request.session['user_id_hit']).exclude(title='general')
	context = {'books':books}
	return render(request,'all_books.html', context)

def hit_selected_view(request, hit_id): # shows the hit selected in a sexy way  
	hit = hit_post.objects.get(id=hit_id, user_id=request.session['user_id_hit'])  # also taking user id so that one user cant see the things of the other user 
	context = {
	'hit':hit
	}
	return render(request,'view_hit.html',context)

def update_hit_view(request, hit_id): # modify aldready saved hit 
	hit = hit_post.objects.get(id=hit_id, user_id=request.session['user_id_hit'])
	context = {
	'title': 'Modify your hit', 
	'hit':hit, 
	}
	if request.POST:
		# if 'rh_private' in request.POST: val = True  # for checkbutton  
		# else: val = False
		hit.title=request.POST['rh_title']
		hit.s_description=request.POST['rh_s_description'] 
		hit.content=request.POST['rh_content']
		# hit.hash_tags=request.POST['rh_hash_tags']
		# hit.private=val
		hit.save()
		return redirect(f'/view/hit/{hit_id}/')
	return render(request,'update_hit_post.html',context)


def images_select(request,to_search=None, page_no=1): # user can select a image for his posts and books
	# if 'img_tag' in request.GET: tag = request.GET['img_tag']  # taking in the search text
	# else:tag='nature'
	img = get_image_from_tag(to_search, page=page_no)
	if img is None: # no img so promt that no image found 
		context = {'img_found': False}
		return render(request, 'create/select_image.html', context)
	elif img['total_pages'] < 7 : # pages more than 7 so limit to 7 pages 
		total_pages = list(range(1,img['total_pages']))
	else :  # pages less than 7 so limit to original no of pages. 
		total_pages = list(range(1,7))

	img_urls = img['urls']
	request.session['img_urls'] = img_urls
	temp = 0 
	c0 = []
	c1 = []
	c2 = []
	c3 = []
	for i in range(len(img_urls)):  # all this shit for just creating the grid to add the images 
		if temp == 0: 
			c0.append([img_urls[i],i])
			temp = temp + 1 
		elif temp == 1:
			c1.append([img_urls[i],i])
			temp = temp + 1 
		elif temp == 2: 
			c2.append([img_urls[i],i])
			temp = temp + 1 
		else:
			c3.append([img_urls[i],i])
			temp = 0 

	context = {
		'c0':c0,
		'c1':c1,
		'c2':c2, 
		'c3':c3, 
		'total_pages':total_pages, 
		'img_found': True
		}

	return render(request, 'create/select_image.html', context)


def save_complete_post_with_img(request, img_link):  # save the hit_post in the db by getting the image link and saving it in the db .  
    post_data = request.session['hit_post_data']
    hit_post.objects.create(title=post_data['title'],
    						s_description=post_data['s_description'], 
    						content=post_data['content'],
    						# hash_tags=post_data['hash_tags'],
    						# private=post_data['private'],
    						book_id=post_data['book_id'], 
    						user_id=post_data['user_id'], 
    						img_link=request.session['img_urls'][int(img_link)][1],
    						)
    return redirect('/home/')


def about(request):# show all hash tags in a sexy way. 
		return render(request, 'about.html')


def delete_post(request, id, delete=None  ):  # show all hits which have the specific hash tag or tags. 
	if delete is not None  : 
		hit_post.objects.filter(id=id, user_id=request.session['user_id_hit']).delete()
		return redirect('/home/')
	# if delete is 'book' : 
	# 	hit_book.objects.filter(id=id, user_id=request.session['user_id_hit']).delete()
	return render(request, 'delete.html')

def schedule_posts(request, hit_post_id):
	# check if the user is logged in and accesing the suitable things 
	hit_post_data = hit_post.objects.filter(user_id=request.session['user_id_hit'],id=hit_post_id )
	if len(hit_post_data) == 0 :
		return render(request, 'error/user_login_error.html')
	hit_post_data = hit_post_data[0]
	if request.POST:
		# take from the user inputs
		hit_post_data.period = request.POST['period']
		hit_post_data.times = request.POST['times']
		hit_post_data.time_for_next_email = 1
		hit_post_data.save()
		return redirect(f'/view/hit/{hit_post_data.id}/')
		# the post page and also set the icon the post for the the user... 


	return render(request, 'scheduling_emails.html')

def logout(request):
	request.session['user_id_hit'] = None 
	request.session['hit_post_data'] = None 
	return redirect('/')


def handler404(request, *args, **kwargs):
    return render(request, 'error404.html', status=404)

def handler500(request, *args, **kwargs):
    return render(request, 'error500.html', status=500)