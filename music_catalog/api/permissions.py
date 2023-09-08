from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import View


class IsSafeMethod(BasePermission):
    """Все пользователи могут просматривать каталог."""
    def has_permission(self, request: Request, view: View) -> bool:
        """Если запрос безопасный, то доступ разрешен."""
        return request.method in SAFE_METHODS
