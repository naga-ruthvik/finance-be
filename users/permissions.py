from rest_framework.permissions import BasePermission

from .models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.ADMIN


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.VIEWER


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.ANALYST


class CanViewRecords(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [
            User.Role.VIEWER,
            User.Role.ADMIN,
            User.Role.ANALYST,
        ]
