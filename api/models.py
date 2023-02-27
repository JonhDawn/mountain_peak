from django.db.models import CharField, FloatField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


LATITUDE_VALIDATORS = [MaxValueValidator(90), MinValueValidator(-90)]
ALTITUDE_VALIDATORS = [MaxValueValidator(16383), MinValueValidator(-16383)]  # Everest: 8849m, Mariana Trench: -10.920m


class Peak(Model):
    lat = FloatField(validators=LATITUDE_VALIDATORS)  # latitude
    lon = FloatField()  # longitude
    altitude = FloatField(validators=ALTITUDE_VALIDATORS)
    name = CharField(unique=True, max_length=100)

    @classmethod
    def get_fields(cls):
        return [field.name for field in cls._meta.get_fields()]
