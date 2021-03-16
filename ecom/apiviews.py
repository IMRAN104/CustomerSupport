from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from .models import *
from .serializers import *

# Create your views here.


class CategoryList(APIView):
	def get(self, request, format=None):
		categories = eComCategory.objects.all()
		#categories = (categories)
		serializer = CategoryHierarchySerializer(categories, many=True)
		return Response(serializer.data)

	# def post(self, request, format=None):
	#     serializer = ItemCategorySerializer(data=request.data)
	#     if serializer.is_valid():
	#         serializer.save()
	#         return Response(serializer.data, status=status.HTTP_201_CREATED)
	#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class CategoryItems(APIView):
	def get_object(self, catname):
		try:
			return eComCategory.objects.get(category_name=catname)
		except eComCategory.DoesNotExist:
			raise Http404

	def get(self, request, catname, format=None):
		
		category = self.get_object(catname)
		serializer = CategoryItemsSerializer(category)
		
		return Response(serializer.data)

	def delete(self, request, id, format=None):
		category = self.get_object(id)
		category.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ItemSingle(APIView):
	def get_object(self, id):
		try:
			return eComItem.objects.get(id=id)
			#ItemCategory.objects.__getattribute__()
		except eComItem.DoesNotExist:
			raise Http404

	def get(self, request, id, format=None):
		
		item = self.get_object(id)
		serializer = ItemSerializer(item)
		return Response(serializer.data)

class ItemCard(APIView):
	def get_object(self, id):
		try:
			return eComItem.objects.get(id=id)
		except eComItem.DoesNotExist:
			raise Http404

	def get(self, request, id, format=None):
		
		item = self.get_object(id)
		serializer = ItemCardSerializer(item)
		print(type(serializer.data))
		return Response(serializer.data)


class SearchedItems(APIView):
	def get(self, request, text, format=None):
		ecomitem = eComItem.objects.filter(display_name__icontains=text)
		serializer = ItemCardSerializer(ecomitem, many=True)
		
		return Response(serializer.data)

class HomeGroups(APIView):
	def get(self, request, format=None):
		homegroups = HomeGroup.objects.all().order_by('group_order')
		serializer = HomeGroupSerializer(homegroups, many=True)
		
		return Response(serializer.data)

# class HomeItems(APIView):
#     def get(self, request, format=None):
#         homeitems = HomeItem.objects.all()
#         serializer = HomeItemSerializer(homeitems, many=True)
		
#         return Response(serializer.data)

class OfferList(APIView):
	def get(self, request, format=None):
		offers = Offer.objects.all()
		#categories = (categories)
		serializer = OfferSerializer(offers, many=True)
		return Response(serializer.data)


class OfferItems(APIView):
	def get_object(self, offer_id):
		try:
			return Offer.objects.get(id=offer_id)
		except Offer.DoesNotExist:
			raise Http404

	def get(self, request, offer_id, format=None):
		
		offer = self.get_object(offer_id)
		serializer = CategoryItemsSerializer(offer)
		
		return Response(serializer.data)


class CustomerProfile(APIView):
	def get_object(self, token):
		try:
			return Customer.objects.get(cardno=token)
		except Customer.DoesNotExist:
			raise Http404

	def get(self, request, token, format=None):
		
		customer = self.get_object(token)
		serializer = CustomerSerializer(customer)
		
		return Response(serializer.data)


def generate_login_token():
	name = "L"
	name = name + str(random.randint(10000, 99999))
	letters = string.ascii_uppercase
	name = name + ''.join(random.choice(letters) for i in range(4))
	name = name + str(random.randint(100, 999))
	name = name + ''.join(random.choice(letters) for i in range(4))
	name = name + str(random.randint(10000, 99999))
	return name


@csrf_exempt
def UserExists(request):
	if request.method == 'POST':
		
		json_data = json.loads(str(request.body, encoding='utf-8'))
		mobile = json_data['phone']
		print(type(mobile))

		try:
			customer = Customer.objects.get(mobile=(mobile))

			# token = generate_login_token() 
			# customer.cardno = token # store
			# customer.save()
			data = {
				'customer_exists': True,
				'token': customer.cardno
			}
			return JsonResponse(data, safe=False)
		except Customer.DoesNotExist:
			data = {
				'customer_exists': False,
				'token': None
			}
			return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def EmailValidation(request):
	if request.method == 'POST':
		
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		token = json_data['token']
		email = json_data['email']
		
		if Customer.objects.filter(cardno=(token),email=email).exists():
			# right pass
			
			return EmailOTPSend(request)
		else:
			message = 'Incorrect email. Please enter correct email.'
			data = {
				'success': False,
				'message': message
			}
		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def UserVerification(request):
	if request.method == 'POST':

		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)
		token = json_data['token']
		password = json_data['password']
		
		if Customer.objects.filter(cardno=(token),password=password).exists():
			# right pass
			# redirect to homepage
			data = {
				'success': True,
				'token': token
			}
		else:
			data = {
				'success': False,
				'token': None,
			}
		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')
	


@csrf_exempt
def Register(request):
	print("register------------------------")

	if request.method == 'POST':
		
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		name = json_data['name']
		mobile = json_data['phone']
		email = json_data['email']
		password = json_data['password']
		street_address = json_data['address']
		city = json_data['city']
		country = 'Bangladesh'#json_data['country']
		gender = json_data['gender']

		district = json_data['district']
		postcode = json_data['postcode']

		#checking

		# if email != '':
		#     if Customer.objects.filter(email_address__iexact=email).exists():
		#         messages.warning(request, f'Email {email} already exists.')
				#return redirect to reister
		try:
			print("in try")
			customer = Customer(name=name,
			mobile=mobile,  email=email, password=password,
			address=street_address, city=city, country=country, gender=gender, type=1, postcode=postcode,
			district=district, cardno=generate_login_token())
			print(customer)
			customer.save()
			print(customer)

			data = {
				'success': True
			}
		except:
			data = {
				'success': False,
				'message': 'Could not create customer'
			}
			print(data)
		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

def TimeExpired(time, limit): # not implemented
	# limit should be in seconds?
	# now - time > limit
	return False # always allow

def send_sms(contact_number, sms_body):
	contact_number = ('88'+contact_number)
	print(contact_number)
	response = requests.get(
		'http://brandsms.mimsms.com/smsapi',
		params={
			'api_key': 'C20057475e39353dd774c6.89872256',
			'type' : 'text',
			'contacts' : contact_number,
			'senderid' : '8809601000500',
			'msg' : sms_body
		},
	)
	print(response)

@csrf_exempt
def MobileVerification(request):
	print("mobileverification------------------")

	if request.method == 'POST':
		
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		mobile = json_data['mobile']
		code = json_data['mobile_OTP']

		try:
			otp = OTP.objects.get(contact=mobile, is_mobile=True)
		except:
			message = 'NO OTP for you!'
			print(message)
			data = {
				'success': False,
				'message': message
			}
			return JsonResponse(data, safe=True)

		if int(code) != int(otp.code):
			message = "Invalid OTP. Try Again."
			print(message)
			data = {
				'success': False,
				'message': message
			}
		elif TimeExpired(otp.timestamp, 300):
			message = "OTP Expired. Try to resend."
			print(message)
			data = {
				'success': False,
				'message': message
			}
		else:
			# correct
			otp.delete()
			message = 'Mobile Verified'
			data = {
				'success': True,
				'message': message
			}

		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def EmailVerification(request):
	print("emailverification------------------")

	if request.method == 'POST':
		
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		token = json_data['token']
		code = json_data['email_OTP']

		try:
			customer = Customer.objects.get(cardno=token)
			#customer = Customer.objects.filter(cardno=token).first().values('email')
			email = customer.email
		except:
			message = "No customer found. This MUST not happen."
			print(message)
			data = {
				'success': False,
				'message': message
			}
			return JsonResponse(data, safe=True)

		try:
			otp = OTP.objects.get(contact=email, is_mobile=False)
		except:
			message = 'NO OTP for you! Should not happen.'
			print(message)
			data = {
				'success': False,
				'message': message
			}
			return JsonResponse(data, safe=True)

		if int(code) != otp.code:
			message = "Invalid OTP. Try Again."
			print(message)
			data = {
				'success': False,
				'message': message
			}
		elif TimeExpired(otp.timestamp, 300):
			message = "OTP Expired. Try to resend."
			print(message)
			data = {
				'success': False,
				'message': message
			}
		else:
			# correct
			otp.delete()
			message = 'Email Verified'
			data = {
				'success': True,
				'message': message
			}

		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')


def generate_new_OTP():
	return str(random.randint(10000, 99999))

def send_email(subject, recipient_list, email_body):
	email_from = settings.EMAIL_HOST_USER
	#subject = subject
	#recipient_list = recipient_list
	send_mail(subject=subject, message=email_body, from_email=email_from, recipient_list=recipient_list, fail_silently=False)

@csrf_exempt
def MobileOTPSend(request):
	print("mobile_otp_send------------------")

	if request.method == 'POST':
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		mobile = json_data['mobile']
		print(type(mobile))
		try:
			# actual otp sending
			success = None
			tried = 0
			#otpcode = "87612"
			otpcode = generate_new_OTP()

			otp, created = OTP.objects.get_or_create(contact=mobile, is_mobile=True, defaults={'resend_count': 0, 'code': int(otpcode)})
			#print('Created' + str(created))
			if not created:
				print("Re writing")
				otp.resend_count = 0
				otp.code = int(otpcode)
				otp.timestamp = datetime.now()
				# otp.save()
			else:
				print("Newly created")

			
			otp.save()
			success = True
			# 	#break
				
			data = {
				'success': success
			}
			msg_body =  str(otpcode)
			send_sms(mobile, msg_body)
			print(data)
		except:
			message = "Could not send OTP"
			print(message)
			data = {
				'success': False,
				'message': message
			}
			print(data)
		return JsonResponse(data, safe=True)
	else:
		#send_sms(mobile, msg_body)
		HttpResponseForbidden('Allowed only via POST')
		

@csrf_exempt
def MobileOTPResend(request):
	print("mobile_otp_resend------------------")

	if request.method == 'POST':
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		mobile = json_data['mobile']
		
		try:
			otp = OTP.objects.get(contact=mobile, is_mobile=True)
			rs_count = otp.resend_count
			
			if rs_count == settings.MOBILE_OTP_VERIFICATION_RESEND_LIMIT:
				message = "Too many OTP resend request. Try again later."
				print(message)
				data = {
					'success': False,
					'message': message
				}
			else:
				print("in else")
				try:
					# send otp
					# otpcode = "87612"
					otpcode = generate_new_OTP()
					otp.code = int(otpcode)
					rs_count += 1
					otp.resend_count = rs_count
					msg_body = str(otpcode)
					print(msg_body)
					send_sms(mobile, msg_body)
					otp.save()
				except:
					pass
				data = {
					'success': True,
					'message': 'OTP resent. '+str(settings.MOBILE_OTP_VERIFICATION_RESEND_LIMIT-rs_count)+' resends remaining.'
				}
		except:
			print("OTP not found")
			data = {
				'success': False,
				'message': 'This message should NEVER be visible. \
				Attempt to resend OTP without sending in the first place.'
			}
		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def EmailOTPSend(request):
	print("email_otp_send------------------")

	if request.method == 'POST':
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		email = json_data['email']
		token = json_data['token']
		# cust = Customer.objects.get(email=email, cardno=token)
		# print(cust.cardno == token)
		# print(cust.email == email)
		try:
			if Customer.objects.filter(email=email, cardno=token).exists():
				
				success = None
				tried = 0
				message = None
				try:
					otpcode = "87612"
					# otpcode = generate_new_OTP()

					otp, created = OTP.objects.get_or_create(contact=email, is_mobile=False, defaults={'resend_count': 0, 'code': int(otpcode)})
					if not created:
						print("Re writing")
						otp.resend_count = 0
						otp.code = int(otpcode)
						otp.timestamp = datetime.now()
						otp.save()
					else:
						print("Newly created")

					msg_body = "Your OTP for Email Verification is "+str(otpcode)+". It will expire in 5 minutes.\n\nIgnore this message if you didn't request for this."
					print(msg_body)
					send_email(subject="Email Verification for Password Reset", 
					recipient_list= [email], email_body=msg_body)
					
					otp.save()
					success = True
					message = 'OTP resent at your email.'
					#break
				except MultipleObjectsReturned:
					print("This MUST not happen. Multiple OTP under same email found.")
					success = False
					message = "This MUST not happen. Multiple OTP under same email found."
					pass
				data = {
					'success': success,
					'message': message
				}
			else:
				message = "No user found!"
				data = {
					'success': False,
					'message': message
				}
		except:
			
			message = 'Internal system error occured. Try again.'
			print(message)
			data = {
				'success': False,
				'message': message
			}
		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')
		

@csrf_exempt
def EmailOTPResend(request):
	print("email_otp_resend------------------")

	if request.method == 'POST':
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		email = json_data['email']
		token = json_data['token']
		if Customer.objects.filter(email=email, cardno=token).exists():
			try:
				otp = OTP.objects.get(contact=email, is_mobile=False)
				rs_count = otp.resend_count
				if rs_count == settings.EMAIL_OTP_PASSWORD_RESET_RESEND_LIMIT:
					# eto otp chas ken
					message = "Too many OTP resend request for password reset. Try again later."
					print(message)
					data = {
						'success': False,
						'message': message
					}
				else:
					try:
						# send otp
						otpcode = "87612"
						# otpcode = generate_new_OTP()
						otp.code = int(otpcode)
						rs_count += 1
						otp.resend_count = rs_count
						msg_body = "Your OTP for Email Verification is "+str(otpcode)+". It will expire in 5 minutes.\n\nIgnore this message if you didn't request for this."
						print(msg_body)
						send_email(subject="Email Verification for Password Reset", 
						recipient_list= [email], email_body=msg_body)
						otp.save()
					except:
						pass
					data = {
						'success': True,
						'message': 'OTP resent. '+str(settings.EMAIL_OTP_PASSWORD_RESET_RESEND_LIMIT-rs_count)+' resends remaining.'
					}
			except:
				print("OTP not found")
				data = {
					'success': False,
					'message': 'This message should NEVER be visible. \
					Attempt to resend OTP without sending in the first place.'
				}
		else:
			print("No user found")
			data = {
				'success': False,
				'message': 'This message should NEVER be visible. \
				The (email, token) pair is not compatible.'
			}
		return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def ResetPassword(request):
	if request.method == 'POST':
		
		json_data = json.loads(str(request.body, encoding='utf-8'))
		token = json_data['token']
		password = json_data['password']
		

		try:
			customer = Customer.objects.get(cardno=token)
			token = generate_login_token() 
			customer.cardno = token # store
			customer.password = password
			customer.save()
			data = {
				'success': True,
				'new_token': token
			}
			return JsonResponse(data, safe=False)
		except Customer.DoesNotExist:
			data = {
				'success': False,
				'new_token': None
			}
			return JsonResponse(data, safe=True)
	else:
		HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def OrderReceive(request): #incomplete
	print("order_receive------------------")

	if request.method == 'POST':
		json_data = json.loads(str(request.body, encoding='utf-8'))
		print(json_data)

		email = json_data['email']