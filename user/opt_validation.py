from .email_service import *
import random 

#     print(hotp(key=secret_key,counter=counter,digits=6))
class OTP:
	def __init__(self):
		self.otp = None
		self.mail = Email()
		self.mail.login()
	

	def generate_otp(self):
		self.otp = str(random.randint(1, 9999)).zfill(4) # generates a random 4 digit no 


	def send_email(self,user_email):
		self.mail.send_mail(text=f'hey your otp for verification of your email is {self.otp} ',
								subject=f'Your hit verification otp is {self.otp}',
							    to_emails=[user_email])
		self.mail.quit_server()

	def validate_otp(self, user_otp):
		if user_otp == self.otp:
			return True 
		return False 


