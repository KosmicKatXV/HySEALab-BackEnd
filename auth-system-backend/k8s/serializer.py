from rest_framework import serializers
from .models import Lab

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ('user')

    def create(self,validated_data):
        lab = Lab.objects.create(user = validated_data['user'])
        lab.save()
        return lab
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        return instance