from django.contrib.auth.models import User
from rest_framework import serializers
from expence.models import Expences,Employee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email","password"]
        read_only_fields = ["id"]
    
class ExpenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expences
        fields = "__all__"
        read_only_fields = ["id","created_at","owner"]
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"