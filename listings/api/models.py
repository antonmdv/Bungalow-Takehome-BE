""" Models, Choices, Validators: should be split to modules """
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_bathroom_size(value):
    """ Bathroom Field Validations """
    if value:
        if round(value, 1) != value:
            raise ValidationError('Value must have at most 1 decimal place.')


class HomeType(models.TextChoices):
    """ Allowed Home Types """
    SINGLE_FAMILY = 'SingleFamily', 'Single Family'
    VACANT_RESIDENTIAL_LAND = 'VacantResidentialLand', 'Vacant Residential Land'
    MISCELLANEOUS = 'Miscellaneous', 'Miscellaneous'
    MULTI_FAMILY_2_TO_4 = 'MultiFamily2To4', 'Multi Family (2-4)'
    Condominium = 'Condominium', 'Condominium'
    APARTMENT = 'Apartment', 'Apartment'
    DUPLEX = 'Duplex', 'Duplex'


class MeasureUnits(models.TextChoices):
    """ Allowed Measure Units """
    SQFT = 'SqFt', 'SqFt'


class SupportedStates(models.TextChoices):
    """ Allowed Measure Units """
    CA = 'CA'


class HouseModel(models.Model):
    """ House Model """

    class Meta:
        verbose_name = 'System House Listing'
        db_table = 'bungalow_house_data'

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    area_unit = models.CharField(
        max_length=10,
        choices=MeasureUnits.choices,
        default=MeasureUnits.SQFT
    )
    bathrooms = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=1,
        validators=[validate_bathroom_size, MinValueValidator(0)]
    )
    bedrooms = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    home_size = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    home_type = models.CharField(
        max_length=50,
        choices=HomeType.choices
    )
    last_sold_date = models.DateField(
        null=True,
        blank=True
    )
    last_sold_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    link = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    property_size = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    rent_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    rent_zestimate_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    rent_zestimate_last_updated = models.DateField(
        null=True,
        blank=True
    )
    tax_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    tax_year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2300)]
    )
    year_built = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1800), MaxValueValidator(2300)]
    )
    zestimate_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    zestimate_last_updated = models.DateField(
        null=True,
        blank=True
    )
    zillow_id = models.BigIntegerField(
        unique=True
    )
    address = models.CharField(
        max_length=255
    )
    city = models.CharField(
        max_length=100
    )
    state = models.CharField(
        max_length=2,
        choices=SupportedStates.choices
    )
    zipcode = models.CharField(
        max_length=10
    )
    reserved = models.BooleanField(
        default=False
    )

    @property
    def formatted_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}"

    def __str__(self):
        return str(self.uuid)
