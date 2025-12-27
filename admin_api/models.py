# admin_api/models.py
from django.contrib.auth.models import User
from django.db import models
from httpcore import Response
from rest_framework.permissions import IsAuthenticated
from admin_api.permissions import IsAdminUserOnly
from rest_framework.views import APIView

class AdminDevice(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20, default="android")
    created_at = models.DateTimeField(auto_now_add=True)
class AdminRegisterDeviceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def post(self, request):
        token = request.data.get("device_token")
        platform = request.data.get("platform", "android")

        if not token:
            return Response({"error": "device_token required"}, status=400)

        AdminDevice.objects.get_or_create(
            admin=request.user,
            device_token=token,
            defaults={"platform": platform}
        )

        return Response({"status": "registered"})
class AdminUnregisterDeviceAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def post(self, request):
        token = request.data.get("device_token")

        AdminDevice.objects.filter(
            admin=request.user,
            device_token=token
        ).delete()

        return Response({"status": "removed"})
