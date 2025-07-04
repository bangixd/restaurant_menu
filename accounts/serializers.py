from rest_framework import serializers
from .models import User, OTP
from django.utils import timezone


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'full_name', 'birth_date', 'gender', 'role']
        read_only_fields = ['phone', 'role']


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    full_name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='customer')

    def validate(self, data):
        try:
            otp = OTP.objects.get(phone=data['phone'], code=data['code'], verified=False)
        except OTP.DoesNotExist:
            raise serializers.ValidationError("کد تأیید نامعتبر است.")

        if otp.created_at + timezone.timedelta(minutes=2) < timezone.now():
            raise serializers.ValidationError("کد منقضی شده است.")

        otp.verified = True
        otp.save()
        return data

    def create(self, validated_data):
        validated_data.pop("code")

        user, created = User.objects.get_or_create(
            phone=validated_data["phone"],
            defaults={
                "full_name": validated_data.get("full_name", ""),
                "birth_date": validated_data.get("birth_date"),
                "gender": validated_data.get("gender"),
                "role": validated_data.get("role", "customer")
            }
        )

        return user
