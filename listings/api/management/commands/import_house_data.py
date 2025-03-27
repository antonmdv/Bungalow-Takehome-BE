""" Management command to populate db """
from django.core.management.base import BaseCommand
from api.models import HouseModel
from pathlib import Path
import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime


FILE_PATH = '../sample-data/'
FILE_NAME = 'data.csv'
DATE_FORMAT = '%m/%d/%Y'


def parse_price(value):
    if not value:
        return None
    value = value.strip().replace('$', '').upper()
    try:
        if value.endswith('K'):
            return Decimal(value[:-1]) * 1_000
        elif value.endswith('M'):
            return Decimal(value[:-1]) * 1_000_000
        else:
            return Decimal(value.replace(',', ''))
    except (InvalidOperation, ValueError):
        return None

def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT).date()
    except ValueError:
        return None

def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = 'Imports data about houses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file_name',
            dest='file_name',
            type=str,
            default=FILE_NAME,
            help='Overrides file name'
        )
        parser.add_argument(
            '--not_reset_db',
            dest='reset_db',
            action='store_false',
            help='Blocks DB reset before import.'
        )
        parser.set_defaults(reset_db=True)

        parser.add_argument(
            '--not_dry_run',
            dest='dry_run',
            action='store_false',
            help='Creates objects in DB'
        )
        parser.set_defaults(dry_run=True)


    def handle(self, *args, **options):
        """" Handle command """
        file_name, reset_db, dry_run = options['file_name'], options['reset_db'], options['dry_run']
        self.stdout.write(f"Launching {self.__module__}\n"
                          f"File Name: {file_name} | Reset DB: {reset_db} | Dry Run: {dry_run}")
        if reset_db:
            res = HouseModel.objects.all().delete()
            self.stdout.write(f"Deleted Rows: {res[0]}")

        file_path = Path(f'{FILE_PATH}{file_name}')
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File is not found. File Path {file_path}"))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            houses = []

            for row in reader:
                house = HouseModel(
                    area_unit=row.get(' area_unit').strip(' '),
                    bathrooms=parse_float(row.get('bathrooms')),
                    bedrooms=parse_int(row.get('bedrooms')),
                    home_size=parse_int(row.get('home_size')),
                    home_type=row.get('home_type'),
                    last_sold_date=parse_date(row.get('last_sold_date')),
                    last_sold_price=parse_price(row.get('last_sold_price')),
                    link=row.get('link'),
                    price=parse_price(row.get('price')),
                    property_size=parse_int(row.get('property_size')),
                    rent_price=parse_price(row.get('rent_price')),
                    rent_zestimate_amount=parse_price(row.get('rentzestimate_amount')),
                    rent_zestimate_last_updated=parse_date(row.get('rentzestimate_last_updated')),
                    tax_value=parse_price(row.get('tax_value')),
                    tax_year=parse_int(row.get('tax_year')),
                    year_built=parse_int(row.get('year_built')),
                    zestimate_amount=parse_price(row.get('zestimate_amount')),
                    zestimate_last_updated=parse_date(row.get('zestimate_last_updated')),
                    zillow_id=parse_int(row.get('zillow_id')),
                    address=row.get('address'),
                    city=row.get('city'),
                    state=row.get('state'),
                    zipcode=row.get('zipcode'),
                )
                houses.append(house)

        if not dry_run:
            self.stdout.write(f"Creating new objects in DB")
            HouseModel.objects.bulk_create(houses)

        self.stdout.write(f"Finished {self.__module__}\n"
                          f"Created in db: {HouseModel.objects.count()}\n"
                          f"Rows in file: 448")
