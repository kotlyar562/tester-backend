from rest_framework import permissions

class IsOwnerOrIsPublic(permissions.BasePermission):
    """Доступ к базе вопросов """
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return obj.publik and obj.good and not obj.copied
        return False
