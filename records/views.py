from django.shortcuts import render

from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import CanViewRecords, IsAdmin, IsAnalyst, IsViewer

from .filters import RecordFilter
from .models import Record
from .pagination import StandardResultsSetPagination
from .serializers import DashboardSummarySerializer, RecordSerializer
from .services.dashboard import get_dashboard_summary

# Create your views here.


class RecordView(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = RecordFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ["amount", "date"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, CanViewRecords]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsAnalyst | IsAdmin]

    @extend_schema(
        responses={200: DashboardSummarySerializer},
        operation_id="get_dashboard_summary",
    )
    def get(self, request):
        data = get_dashboard_summary()
        serializer = DashboardSummarySerializer(data)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_dashboard_summary_api(request):
    """Note: This function is deprecated in favor of DashboardSummaryView."""
    view = DashboardSummaryView.as_view()
    return view(request._request)
