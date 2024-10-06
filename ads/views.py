from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import AdFilter
from .models import Ad, Review
from .paginations import CustomPagination
from .permissions import IsOwnerOrAdmin
from .serializers import AdDetailSerializer, AdSerializer, ReviewSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        elif self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return AdDetailSerializer
        return AdSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
