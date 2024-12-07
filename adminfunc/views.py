from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from profiles.models import FightRecord
from profiles.serializers import FightRecordSerializer
from .models import ProbableFight
from .serializers import ProbableFightSerializer
from rest_framework.response import Response
from rest_framework import generics, status

# Create your views here.
class ProbableFightView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = ProbableFightSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def get_queryset(self):
        return ProbableFight.objects.all().order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApproveFightRecordView(generics.UpdateAPIView):
    queryset = FightRecord.objects.all()
    serializer_class = FightRecordSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        fight_record = self.get_object()
        fight_record.is_approved = True
        fight_record.save()
        serializer = self.get_serializer(fight_record)
        return Response(serializer.data)

    def get_object(self):
        obj = super().get_object()
        if obj.user_profile.user.is_verified:
            return obj
        raise PermissionDenied("User is not verified.")