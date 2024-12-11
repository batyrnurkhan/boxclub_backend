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


class ProbableFightUpdateView(generics.UpdateAPIView):
    serializer_class = ProbableFightSerializer
    permission_classes = [IsAdminUser]
    queryset = ProbableFight.objects.all()
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Handle the case where usernames are not provided in update
        if 'fighter1_username' not in request.data:
            request.data['fighter1_username'] = instance.fighter1.username
        if 'fighter2_username' not in request.data:
            request.data['fighter2_username'] = instance.fighter2.username

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

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