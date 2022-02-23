from rest_framework import serializers
from .models import Participate, Project, Client, User

class ParticipateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Participate
        fields = ['idClient','idProject','enrollmentDate','role']

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title','description','level','initDate', 'finDate', 'report', 'is_finalized', 'idCategory']
        
class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['dni','name','surname','address', 'birthDate']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']