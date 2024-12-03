from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import ProbableFight
from .serializers import ProbableFightSerializer


# Create your views here.
class ProbableFightView(generics.ListCreateAPIView):
    serializer_class = ProbableFightSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProbableFight.objects.all().order_by('-created_at')