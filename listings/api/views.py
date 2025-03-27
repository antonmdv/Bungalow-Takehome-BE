from rest_framework import filters, viewsets, pagination, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.models import HouseModel, SupportedStates
from api.serializers import (
    HouseSerializer,
    HouseListSerializer,
    ReserveHouseSerializer,
)


class HousePagination(pagination.PageNumberPagination):
    """ Pagination class with custom page size """
    page_size = 10


class HouseViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ HouseViewSet """

    queryset = HouseModel.objects.all()
    http_method_names = ['head', 'options', 'get', 'patch', 'post', 'delete']
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price', 'year_built']
    ordering = ['-price', '-year_built']
    search_fields = ['zillow_id', 'city']
    lookup_field = 'uuid'
    pagination_class = HousePagination

    def get_permissions(self):
        """ Override permission for reserve house if needed """
        if self.action in ['reserve_house']:
            # Duplication but more for showcase
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """ Limit queryset only to CA market """
        housing_market = HouseModel.objects.filter(state=SupportedStates.CA)
        return housing_market

    def get_serializer_class(self):
        if self.action == 'list':
            return HouseListSerializer
        elif self.action == 'reserve_house':
            return ReserveHouseSerializer
        return HouseSerializer  # default (for retrieve, create, update, delete)

    @action(detail=True,
            methods=['post'],
            serializer_class=ReserveHouseSerializer,
            permission_classes=[IsAuthenticated])
    def reserve_house(self, request, uuid=None):
        house = self.get_object()
        serializer = self.get_serializer(instance=house, data=request.data)
        serializer.is_valid(raise_exception=True)
        reserved_house = serializer.reserve()
        response = Response(data={'message': f'House at {reserved_house.formatted_address} '
                                             f'was reserved by {request.user.username.capitalize()}'},
                            status=status.HTTP_200_OK)
        return response
