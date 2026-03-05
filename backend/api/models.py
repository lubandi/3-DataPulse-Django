from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    row_count = models.IntegerField(default=0)
    column_count = models.IntegerField(default=0)
    column_names = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="datasets")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.name} ({self.status})"

class DatasetFile(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="files")
    file_path = models.CharField(max_length=500)
    original_filename = models.CharField(max_length=255)

    def __str__(self):
        return self.original_filename

class ValidationRule(models.Model):
    name = models.CharField(max_length=255)
    dataset_type = models.CharField(max_length=100)
    field_name = models.CharField(max_length=255)
    rule_type = models.CharField(max_length=20)
    parameters = models.TextField(null=True, blank=True)
    severity = models.CharField(max_length=10, default="MEDIUM")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rule_type})"

class CheckResult(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="check_results")
    rule = models.ForeignKey(ValidationRule, on_delete=models.CASCADE, related_name="check_results")
    passed = models.BooleanField()
    failed_rows = models.IntegerField(default=0)
    total_rows = models.IntegerField(default=0)
    details = models.TextField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Pass" if self.passed else "Fail"
        return f"Check for {self.dataset.name} - Rule {self.rule.name}: {status}"

class QualityScore(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="quality_scores")
    score = models.FloatField()
    total_rules = models.IntegerField(default=0)
    passed_rules = models.IntegerField(default=0)
    failed_rules = models.IntegerField(default=0)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quality Score for {self.dataset.name}: {self.score}"
