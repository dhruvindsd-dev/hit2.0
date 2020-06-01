import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hit.settings")
django.setup()

from user.email_service import *
from user.models import *
from hit_book.models import hit_post
# initialise the server

email = Email()
email.login()

post_reminders = hit_post.objects.filter(period__gt=0, times__gt=0 ) # for any post that has a period greater that 0
# validations to be implemented in js
# the user entered no of times should not be 0
for hit in post_reminders:
	# reduce all time_for_next_email by one
	hit.time_for_next_email = int(hit.time_for_next_email) - 1
	hit.save()
	if hit.time_for_next_email == 0 :  # if time is zero than send the mail and redset the time_for_next_email to period and also increment the counter
		user = User_db.objects.get(id=hit.user_id)
		text = f'Hey {user.user_name} this is a reminder from HIT 2.0, to remind you to read your post on {hit.title} \n here is a link to take you directly to your post: highlyinformativetext.pythonanywhere.com/login/{hit.id}/  \n {hit.counter}/{hit.times} \n {hit.custom_message}'
		subject = 'REMINDER FROM HIT_2.0'
		email.send_mail(text=text, subject=subject, to_emails=[user.email])
		print(f'email sent to {user.email}')
		hit.time_for_next_email = hit.period
		hit.counter = int(hit.counter) + 1
		hit.save()
		if int(hit.counter) >= int(hit.times):  # if the counter reaches the max length the user hash entered then reset the hit_post until the user schedules it again
			# set everthing to zero
			hit.time_for_next_email = 0
			hit.period = 0
			hit.custom_message = 0
			hit.times = 0
			hit.counter = 0
			hit.save()

email.quit_server()