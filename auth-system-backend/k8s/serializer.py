from rest_framework import serializers
from .models import Lab, Volume

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

class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        fields = ('user')

    def create(self,validated_data):
        vol = Volume.objects.create(user = validated_data['user'])
        vol.save()
        return vol
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        return instance