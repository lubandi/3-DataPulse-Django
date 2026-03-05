from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Dataset, ValidationRule, CheckResult, QualityScore

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "full_name"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            "id", "name", "file_type", "row_count", "column_count",
            "column_names", "status", "uploaded_at",
        ]

class ValidationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRule
        fields = [
            "id", "name", "dataset_type", "field_name", "rule_type",
            "parameters", "severity", "is_active", "created_at",
        ]

class ValidationRuleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRule
        fields = [
            "name", "dataset_type", "field_name", "rule_type",
            "parameters", "severity", "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class CheckResultSerializer(serializers.ModelSerializer):
    dataset_id = serializers.IntegerField(source="dataset.id", read_only=True)
    rule_id = serializers.IntegerField(source="rule.id", read_only=True)

    class Meta:
        model = CheckResult
        fields = [
            "id", "dataset_id", "rule_id", "passed", "failed_rows",
            "total_rows", "details", "checked_at",
        ]

class QualityScoreSerializer(serializers.ModelSerializer):
    dataset_id = serializers.IntegerField(source="dataset.id", read_only=True)

    class Meta:
        model = QualityScore
        fields = [
            "id", "dataset_id", "score", "total_rules", "passed_rules",
            "failed_rules", "checked_at",
        ]

class QualityReportSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()
    dataset_name = serializers.CharField()
    score = serializers.FloatField()
    total_rules = serializers.IntegerField()
    results = CheckResultSerializer(many=True)
    checked_at = serializers.DateTimeField()
