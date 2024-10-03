



from rest_framework.response import Response
from dashboard.views.imports import *
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

DISTRICT_CHOICES = [
    ('0', 'Thiruvananthapuram'),
    ('1', 'Kollam'),
    ('2', 'Pathanamthitta'),
    ('3', 'Alapuzha'),
    ('4', 'Kottayam'),
    ('5', 'Idukki'),
    ('6', 'Eranakulam'),
    ('7', 'Thrissur'),
    ('8', 'Palakkad'),
    ('9', 'Malappuram'),
    ('10', 'Kozhikode'),
    ('11', 'Wayanad'),
    ('12', 'Kannur'),
    ('13', 'Kasargode'),
]
@csrf_exempt 
@api_view(["POST"])  
def register(request):
    name = request.data.get("name")
    district_number = request.data.get("district")
    email = request.data.get("email")

    print(name, "--", district_number, "--", email)

    if not name:
        return Response({"status": "error", "message": "Please provide name"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not district_number:
        return Response({"status": "error", "message": "Please provide a valid district"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not email:
        return Response({"status": "error", "message": "Please provide a valid email"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if CustomUser.objects.filter(email=email,name=name, is_deleted=False).exists():
            return Response({"status": "error", "message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        valid_districts = [choice[0] for choice in DISTRICT_CHOICES]
        if district_number not in valid_districts:
            return Response({"status": "error", "message": "Invalid district number"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            name=name,
            email=email,
            district=district_number
        )
        user.save()
        district_name = dict(DISTRICT_CHOICES).get(district_number, "Unknown District")

        user_details = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "district": district_name,
        }

        return Response({
            "status": "success",
            "message": "Registration Successful",
            "user": user_details,
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
