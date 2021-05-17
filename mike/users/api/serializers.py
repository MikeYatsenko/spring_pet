from rest_framework import serializers
from ..models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username','password']

    def validate(self, attrs):
        email =attrs.get('email', '')
        username =attrs.get('username', '')

        if  not username.isalnum():
            raise  serializers.ValidationError('The username should only contain alphanumeric')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields =['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    username = serializers.CharField(max_length=225, read_only=True)
    tokens = serializers.CharField(max_length=555, read_only=True)

    class Meta:
        model = User
        fields = ['email','password','username','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user =auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, please specify correct credentials')
        if not user.is_active:
            raise AuthenticationFailed('Your account is inactive')
        if not user.is_verified:
            raise AuthenticationFailed('Please verify your email')


        return {
            'email':user.email,
            'username':user.username,
            'tokens': user.tokens
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
     email = serializers.EmailField(min_length=3)

     class Meta:
         fields = ['email']

     def validate(self,attrs):
         try:
             email=attrs['data'].get('email','')
             if User.objects.filter(email=email).exist():
                 user = User.objects.get(email=email)
                 uidb64 = urlsafe_base64_encode(user.id)
                 token = PasswordResetTokenGenerator.make_token(user)
                 request =attrs['data'].get('request')
                 current_site= get_current_site(request).domain
                 relativeLink = reverse('email-verify')
                 absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
                 email_body = 'Hi ' + user.username + '. Use link bellow to verify your email \n' + absurl
                 data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
                 Utils.send_email(data)




