""" House Serializers """
from rest_framework import serializers
from api.models import HouseModel, SupportedStates


class HouseListSerializer(serializers.ModelSerializer):
    """ Lighter version for list view """

    class Meta:
        model = HouseModel
        fields = [
            'uuid',
            'address',
            'city',
            'state',
            'price',
            'zillow_id',
            'year_built',
        ]


class HouseSerializer(serializers.ModelSerializer):
    """ General House Serializer to use for details, create, update and delete"""

    class Meta:
        model = HouseModel
        fields = '__all__'

    def to_representation(self, instance):
        """ Make additional data changes """
        rep = super().to_representation(instance)
        if instance.state == SupportedStates.CA:
            rep['state'] = 'Lovely California'
        return rep

    def validate_price(self, value):
        """ Ensure price is positive """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, attrs):
        """ Cross-field validation """
        price = attrs.get('price')
        rent_price = attrs.get('rent_price')

        if rent_price and price and rent_price > price:
            raise serializers.ValidationError("Rent price cannot exceed house price.")

        return attrs

    def update(self, instance, validated_data):
        """ Prevent updates if house is reserved """
        if instance.reserved:
            raise serializers.ValidationError("You cannot modify a reserved house.")
        return super().update(instance, validated_data)


class ReserveHouseSerializer(serializers.Serializer):
    """ Reservation Serializer """

    def validate(self, attrs):
        """ Validate if house available to be reserved """
        if attrs:
            raise serializers.ValidationError('Endpoint does not support any parameters.')

        if self.instance.reserved:
            raise serializers.ValidationError('House already reserved.')
        return attrs

    def reserve(self):
        """ Reserve house action """
        self.instance.reserved = True
        self.instance.save(update_fields=["reserved"])
        return self.instance
