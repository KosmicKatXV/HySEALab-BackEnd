from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email' ,'password' ,'first_name' , 'last_name' )

    def create(self,validated_data):
        user = CustomUser.objects.create(email = validated_data['email'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        print("update!")
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        return instance

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password")