from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import AdFilter
from .models import Ad, Review
from .paginations import CustomPagination
from .permissions import IsOwnerOrAdmin
from .serializers import AdDetailSerializer, AdSerializer, ReviewSerializer


@extend_schema(tags=["Advertisements"])
@extend_schema_view(
    list=extend_schema(
        summary="Getting a list of all advertisements",
    ),
    create=extend_schema(
        summary="Creating a new ad",
    ),
    update=extend_schema(
        summary="Modifying an existing ad",
    ),
    partial_update=extend_schema(
        summary="Brief description of the partial change"
    ),
    retrieve=extend_schema(
        summary="Detailed information about the advertisement",
    ),
    destroy=extend_schema(
        summary="Deleting an advertisement",
    ),
)
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


@extend_schema(tags=["Reviews"])
@extend_schema_view(
    list=extend_schema(
        summary="Getting a list of all reviews",
    ),
    create=extend_schema(
        summary="Creating a new review",
    ),
    update=extend_schema(
        summary="Modifying an existing review",
    ),
    partial_update=extend_schema(
        summary="Brief description of the partial change"
    ),
    retrieve=extend_schema(
        summary="Detailed information about the review",
    ),
    destroy=extend_schema(
        summary="Deleting a review",
    ),
)
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
