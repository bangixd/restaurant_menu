from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from .models import OTP, PhoneNumber, User
import random
from .serializers import UserProfileSerializer, VerifyOTPSerializer, PhoneNumberSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


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


# class VerifyOTPView(APIView):
#     def post(self, request):
#         phone = request.data.get('phone')
#         code = request.data.get('code')
#
#         try:
#             otp = OTP.objects.filter(phone=phone, code=code, verified=False).latest('created_at')
#         except OTP.DoesNotExist:
#             return Response({'error': 'کد تایید نا معتبر است'}, status=400)
#
#         if not otp.is_invalid():
#             return Response({'error': 'کد منقضی شده'}, status=400)
#
#         otp.verified = True
#         otp.save()
#
#         user, created = User.objects.get_or_create(phone=phone)
#
#         refresh = RefreshToken.for_user(user)
#
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': {
#                 'id': user.id,
#                 'phone': user.phone,
#                 'role': user.role,
#             }
#         })

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=200)


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


class PhoneNumberCreateView(generics.CreateAPIView):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [permissions.AllowAny]  # بدون نیاز به احراز هویت