from rest_framework import permissions

class MatchmakerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_matchmaker:
            return True
        return False