import os
import json
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    DatasetSerializer,
    ValidationRuleSerializer,
)
from .models import Dataset, DatasetFile, ValidationRule
from .services.file_parser import parse_csv, parse_json

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.payload["sub"] = user.email
    return str(refresh.access_token)

class RegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=serializer.validated_data["email"]).exists():
                return Response(
                    {"detail": "Email already registered"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
            access_token = get_tokens_for_user(user)
            return Response(
                {"access_token": access_token, "token_type": "bearer"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                access_token = get_tokens_for_user(user)
                return Response(
                    {"access_token": access_token, "token_type": "bearer"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatasetUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        filename = file.name or ""
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in ("csv", "json"):
            return Response({"detail": f"Unsupported file type: {ext}"}, status=status.HTTP_400_BAD_REQUEST)

        upload_dir = getattr(settings, "UPLOAD_DIR", os.path.join(settings.BASE_DIR, "uploads"))
        os.makedirs(upload_dir, exist_ok=True)

        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(upload_dir, unique_name)

        content = file.read()
        if len(content) == 0:
            return Response({"detail": "Uploaded file is empty."}, status=status.HTTP_400_BAD_REQUEST)

        with open(file_path, "wb") as fh:
            fh.write(content)

        try:
            metadata = parse_csv(file_path) if ext == "csv" else parse_json(file_path)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response({"detail": f"Failed to parse: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.create(
            name=filename.rsplit(".", 1)[0],
            file_type=ext,
            row_count=metadata["row_count"],
            column_count=metadata["column_count"],
            column_names=json.dumps(metadata["column_names"]),
            status="PENDING",
            uploaded_by=request.user if request.user.is_authenticated else None,
        )

        DatasetFile.objects.create(
            dataset=dataset,
            file_path=file_path,
            original_filename=filename,
        )

        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DatasetListView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        skip = int(request.query_params.get("skip", 0))
        limit = int(request.query_params.get("limit", 20))

        total = Dataset.objects.count()
        datasets = Dataset.objects.all()[skip:skip + limit]

        serializer = DatasetSerializer(datasets, many=True)
        return Response({"datasets": serializer.data, "total": total}, status=status.HTTP_200_OK)

VALID_TYPES = {"NOT_NULL", "DATA_TYPE", "RANGE", "UNIQUE", "REGEX"}
VALID_SEVERITIES = {"HIGH", "MEDIUM", "LOW"}

class RuleListCreateView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        dataset_type = request.query_params.get("dataset_type")
        qs = ValidationRule.objects.filter(is_active=True)
        if dataset_type:
            qs = qs.filter(dataset_type=dataset_type)
        serializer = ValidationRuleSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        rule_type = data.get("rule_type")
        severity = data.get("severity", "MEDIUM")

        if rule_type not in VALID_TYPES:
            return Response({"detail": f"Invalid rule_type: {VALID_TYPES}"}, status=status.HTTP_400_BAD_REQUEST)
        if severity not in VALID_SEVERITIES:
            return Response({"detail": f"Invalid severity: {VALID_SEVERITIES}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ValidationRuleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RuleDetailView(APIView):
    def put(self, request, pk, *args, **kwargs):
        return Response({"detail": f"PUT /api/rules/{pk} not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def delete(self, request, pk, *args, **kwargs):
        return Response({"detail": f"DELETE /api/rules/{pk} not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class CheckRunView(APIView):
    def post(self, request, pk, *args, **kwargs):
        return Response({"detail": f"POST /api/checks/run/{pk} not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class CheckResultView(APIView):
    def get(self, request, pk, *args, **kwargs):
        return Response({"detail": f"GET /api/checks/results/{pk} not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ReportDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        return Response({"detail": f"GET /api/reports/{pk} not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ReportTrendView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "GET /api/reports/trends not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)
