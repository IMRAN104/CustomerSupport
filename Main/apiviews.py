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

class ComplainList(APIView):
    def get(self, request, format=None):
        complains = Complain.objects.filter(parent=None)
        serializer = ComplainSerializer(complains, many=True)
        return Response(serializer.data)

class ComplainDetails(APIView):
    def get_object(self, id):
        try:
            # return Complain.objects.get(id=id)
            return Complain.objects.filter(parent_id=id).order_by('date')
            #ItemCategory.objects.__getattribute__()
        except Complain.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        complain = Complain.objects.get(id=id)
        serializer1 = ComplainSerializer(complain)

        complain = self.get_object(id)
        print("Complain: ", complain)
        serializer2 = ComplainSerializer(complain, many = True)
        
        serializer = {
            'parent': serializer1.data,
            'children': serializer2.data
        }
        return Response(serializer)


# @csrf_exempt
# def UserExists(request):
# 	if request.method == 'POST':
        
# 		json_data = json.loads(str(request.body, encoding='utf-8'))
# 		mobile = json_data['username']
# 		print(type(username))

# 		try:
# 			user = User.objects.get(username=(username))
# 			data = {
# 				'customer_exists': True,
# 				'token': gener
# 			}
# 			return JsonResponse(data, safe=False)
# 		except User.DoesNotExist:
# 			data = {
# 				'customer_exists': False,
# 				'token': randomStringGenerator
# 			}
# 			return JsonResponse(data, safe=True)
# 	else:
# 		HttpResponseForbidden('Allowed only via POST')

def randomStringGenerator():
    name = "I"
    name = name + str(random.randint(100, 999))
    letters = string.ascii_uppercase
    name = name + ''.join(random.choice(letters) for i in range(2))
    name = name + str(random.randint(10, 99))
    name = name + ''.join(random.choice(letters) for i in range(2))
    name = name + str(random.randint(100, 999))
    name = name + "."
    return name


@csrf_exempt
def ComplainCreate(request):
    if request.method == 'POST':
        json_data = json.loads(str(request.body, encoding='utf-8'))
        print(json_data)

        user_id = int(json_data['user'])
        description = str(json_data['description'])
        parent_id = int(json_data['parent'])
        # date = datetime(json_data['date'])
        # attachment = str(json_data['attachment'])

        try:
            print("in try")
            complain = Complain(user_id = user_id, description = description, parent_id = parent_id )
            print(complain)
            complain.save()
            print(complain)
            data = {
                'success': True
            }
        except:
            data = {
                'success': False,
                'message': 'Could not create complain'
            }
            print(data)
        return JsonResponse(data, safe=True)
    else:
        HttpResponseForbidden('Allowed only via POST')