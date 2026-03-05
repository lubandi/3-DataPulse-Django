from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Dataset, ValidationRule, CheckResult, QualityScore

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file_type', 'row_count', 'column_count', 'column_names', 'status', 'uploaded_at']

class ValidationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRule
        fields = ['id', 'name', 'dataset_type', 'field_name', 'rule_type', 'parameters', 'severity', 'is_active', 'created_at']


