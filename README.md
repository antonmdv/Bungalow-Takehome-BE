# Notes

### 1. Setup & Admin Access
./manage.py createsuperuser --username=admin --email=admin@bungalow.com
password: admin

### 2. Migrate the Database
./manage.py migrate
Sets up local DB schema

### 3. Import Sample Data
./manage.py import_house_data --not_dry_run
Imports 448 records from CSV
Enforces zillow_id uniqueness (by design)
Use --not_reset_db to retain existing data if zillow_id's are unique
Use --file_name to specify a different file to import

### 4. Shell Sanity Check
./manage.py shell
>>> from api.models import HouseModel
>>> HouseModel.objects.count() == 448

### 5. Testing
./manage.py test
Runs all unit tests (list, detail, reserve, auth, validation)

### 6. API Overview
API Root -> GET http://127.0.0.1:8000/api/
Use the browsable DRF interface (session login supported).


### 7. CRUD Support
Action         Endpoint Method
List Houses    /api/houses/                        GET
Get House      /api/houses/<uuid>/                 GET
Create House   /api/houses/                        POST
Update House   /api/houses/<uuid>/                 PATCH
Delete House   /api/houses/<uuid>/                 DELETE
Reserve House  /api/houses/<uuid>/reserve_house/   POST

### 8. Authentication
Certain endpoints (like reserve_house) require login.
Login: /admin/login/
Logout: /admin/logout/
Use session login in browser, authorization token was not setup.

### 9. Payloads
Sample json payload data for POST action to create new listing: 
{
  "area_unit": "SqFt",
  "bathrooms": 2.5,
  "bedrooms": 3,
  "home_size": 1400,
  "home_type": "SingleFamily",
  "last_sold_date": "2020-07-15",
  "last_sold_price": 450000,
  "link": "https://www.zillow.com/homedetails/6051-Spring-Valley-Rd-Hidden-Hills-CA-91302/19882694_zpid/",
  "price": 500000,
  "property_size": 6000,
  "rent_price": 2500,
  "rent_zestimate_amount": 2550,
  "rent_zestimate_last_updated": "2023-10-01",
  "tax_value": 100000,
  "tax_year": 2023,
  "year_built": 1995,
  "zestimate_amount": 505000,
  "zestimate_last_updated": "2023-10-01",
  "zillow_id": 12345678,
  "address": "123 Example St",
  "city": "Los Angeles",
  "state": "CA",
  "zipcode": "90001"
}

Sample json payload data for PATCH action to update existing listing: 
{
  "city": "San Francisco",
  "price": 1000
}

### 10. Re-sync requirements:
Added ipython & ipdb to make life easier =)

## Time Spent
3 hours

## Assumptions
Not splitting row in the CSV into different models and linking them

## Next Steps
Splitting view futher, splitting serializers and having higherarchical inheritance structure. Adding more form validations on serializer level. Splitting models into objects pulled from zillow and our own models. Possibly addding nested data models like adresses, etc, depending on the business needs.

