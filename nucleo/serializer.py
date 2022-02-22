from dataclasses import fields
from rest_framework import serializers
from .models import Participate

class ParticipateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Participate
        fields = ['idClient','idProject','enrollmentDate','role']