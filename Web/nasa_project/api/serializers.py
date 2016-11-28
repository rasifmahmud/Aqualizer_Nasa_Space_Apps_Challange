from rest_framework import serializers

from api.models import Task
from api.models import WaterParticle


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'description', 'completed')

class WaterParticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = WaterParticle
		fields = ('user', 'deviceID', 'ph', 'temperature', 'orp', 'dateTime', 'geoLocation','token','salinity','access')
