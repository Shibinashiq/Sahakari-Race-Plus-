



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


@api_view(["POST"])  
def register(request):
    name = request.data.get("name")
    district_number = request.data.get("district")
    email = request.data.get("email")
    phone = request.data.get("phone")

    print(name, "--", district_number, "--", email)

    if not name:
        return Response({"status": "error", "message": "Please provide name"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not district_number:
        return Response({"status": "error", "message": "Please provide a valid district"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not email:
        return Response({"status": "error", "message": "Please provide a valid email"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if CustomUser.objects.filter(email=email,name=name,phone_number=phone, is_deleted=False).exists():
            return Response({"status": "error", "message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        valid_districts = [choice[0] for choice in DISTRICT_CHOICES]
        if district_number not in valid_districts:
            return Response({"status": "error", "message": "Invalid district number"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            name=name,
            email=email,
            district=district_number,
            phone_number=phone,
        )
        user.save()
        district_name = dict(DISTRICT_CHOICES).get(district_number, "Unknown District")

        user_details = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone_number,
            "district": district_name,
        }

        return Response({
            "status": "success",
            "message": "Registration Successful",
            "user": user_details,
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






def sendsms(otp, phone):
    cynbus_url = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey=347d4ad8-60cd-11ec-b710-0200cd936042&to=91{phone}&from=OTPQIK&msg=Your%20OTP%20to%20login%20Sahakari%20Race%20Plus%20is%20{otp}%20Please%20do%20not%20share%20this%20OTP.%20Powered%20by%20Cynbus"
    requests.get(url=cynbus_url)

@api_view(["POST"])
def otp_auth(request):
    phone = request.data.get("phone")
    request_id = request.data.get("request_id")
    print(phone, request_id)

    if phone and request_id:

        try:
            user = CustomUser.objects.get(phone_number=phone,  is_deleted=False)
            otp_exists = Otp.objects.filter(request_id=request_id, requested_by=user, verified=False).exists()
            
            if otp_exists:
                otp = Otp.objects.filter(request_id=request_id, requested_by=user, verified=False).first()
                code = otp.code
                if phone != "919876543210":
                    sendsms(str(code), phone)
                response = {
                    "status": "Success",
                    "message": "Login OTP Sent!",
                    "route": "login",
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                code = randint(1000, 9999)
                if phone == "919876543210":
                    code = 5555
                otp = Otp(requested_by=user, code=code, request_id=request_id)
                otp.save()
                code = otp.code
                if phone != "919876543210":
                    sendsms(str(code), phone)
                response = {
                    "status": "success",
                    "message": "Login OTP Sent!",
                    "route": "login",
                }
                return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            otp_exists = Otp.objects.filter(temp_user__phone=phone, request_id=request_id, verified=False).exists()
            if otp_exists:
                otp = Otp.objects.filter(temp_user__phone=phone, request_id=request_id, verified=False).first()
                code = otp.code
                if phone != "919876543210":
                    sendsms(str(code), phone)
                response = {
                    "status": "Success",
                    "message": "Signup OTP Sent!",
                    "route": "signup",
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                code = randint(1000, 9999)
                if phone == "919876543210":
                    code = 5555
                tempuser = TempUser.objects.create(name="",phone=phone, email="")
                otp = Otp(temp_user=tempuser, request_id=request_id, code=code)
                otp.save()
                code = otp.code
                if phone != "919876543210":
                    sendsms(str(code), phone)
                response = {
                    "status": "success",
                    "message": "Signup OTP Sent!",
                    "route": "signup",
                }
                return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            "status": "error",
            "message": "Incomplete request",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    





@api_view(["POST"])
def otp_login_verify(request):
    phone = request.data.get("phone")
    code = request.data.get("code")
    request_id = request.data.get("request_id")
    if phone and code and request_id:

        if CustomUser.objects.filter(
            phone_number=phone, is_deleted=False
        ).exists():
            user = CustomUser.objects.get(
                phone_number=phone, is_deleted=False
            )

            if Otp.objects.filter(
                requested_by=user, code=code, request_id=request_id, verified=False
            ).exists():
                otp = Otp.objects.get(
                    requested_by=user, code=code, request_id=request_id, verified=False
                )
                otp.verified = True
                date_from = datetime.now() - timedelta(days=1)
                otp.created__gte = date_from
                otp.save()

                user_details = {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone_number,
                    "email": user.email,
                }

                refresh = RefreshToken.for_user(user)
                response = {
                    "status": "success",
                    "message": "Login successful",
                    "user": user_details,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": "error",
                    "message": "OTP verification failed",
                }
                return Response(response, status=status.HTTP_410_GONE)
        else:
            response = {
                "status": "error",
                "message": "User not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    else:
        response = {
            "status": "error",
            "message": "Incomplete request",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    















@api_view(["POST"])
def resend_otp(request):
    request_id = request.data.get("request_id")
    phone = request.data.get("phone")

    is_temp_otp = Otp.objects.filter(
        request_id=request_id, verified=False, temp_user__phone=phone
    )
    is_user_otp = Otp.objects.filter(
        request_id=request_id, verified=False, requested_by__phone_number=phone
    )

    if is_temp_otp:
        otp = is_temp_otp[0]
        code = otp.code
        if phone != "919876543210":
            sendsms(str(code), phone)
        response = {
            "status": "success",
            "message": "OTP resend!",
            "route": "signup",
        }
        return Response(response, status=status.HTTP_200_OK)
    elif is_user_otp:
        otp = is_user_otp[0]
        code = otp.code
        if phone != "919876543210":
            sendsms(str(code), phone)
        response = {
            "status": "success",
            "message": "OTP resend!",
            "route": "login",
        }
        return Response(response, status.HTTP_200_OK)
    else:
        response = {
            "status": "error",
            "message": "OTP does not exist",
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
