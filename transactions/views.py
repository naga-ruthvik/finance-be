from django.shortcuts import render

from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import CanViewTransactions, IsAdmin, IsAnalyst, IsViewer

from .filters import TransactionFilter
from .models import Transaction
from .pagination import StandardResultsSetPagination
from .serializers import DashboardSummarySerializer, TransactionSerializer
from .services.dashboard import get_dashboard_summary

# Create your views here.


class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = TransactionFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ["amount", "date"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, CanViewTransactions]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DashboardSummaryView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        responses={200: DashboardSummarySerializer},
        operation_id="get_dashboard_summary",
    )
    def get(self, request):
        data = get_dashboard_summary()
        serializer = DashboardSummarySerializer(data)
        return Response(serializer.data)
