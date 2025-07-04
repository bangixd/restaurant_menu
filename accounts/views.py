from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework import status
from .models import OTP
import random


class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'شماره موبایل الزامی است.'}, status=400)
        code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=code)

        # TODO فقط برای محیط دولوپ
        print(f'کد تایید برای {phone} = {code}')

        return Response({'message': 'کد تایید ارسال شد'})


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')

        try:
            otp = OTP.objects.filter(phone=phone, code=code, verified=False).latest('created_at')
        except OTP.DoesNotExist:
            return Response({'error': 'کد تایید نا معتبر است'}, status=400)

        if not otp.is_invalid():
            return Response({'error': 'کد منقضی شده'}, status=400)

        otp.verified = True
        otp.save()

        user, created = User.objects.get_or_create(phone=phone)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'phone': user.phone,
                'role': user.role,
            }
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)