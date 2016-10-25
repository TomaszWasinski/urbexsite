import factory as f
import factory.fuzzy as fuzzy
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory

from .models import Category, Location


faker = FakerFactory.create()

# TODO
# def get_random_coordinates():
#     coord_generator = fuzzy.FuzzyFloat(-180.0, 180.0)
#     return [coord_generator.fuzz(), coord_generator.fuzz()]


class CategoryFactory(DjangoModelFactory):
    name = f.Sequence(lambda n: 'category %s' % n)
    description = f.LazyAttribute(lambda x: faker.text())

    class Meta:
        model = Category


class LocationFactory(DjangoModelFactory):
    name = f.Sequence(lambda n: 'location %s' % n)
    description = f.LazyAttribute(lambda x: faker.text())
    # TODO coordinates = f.LazyAttribute(lambda x: get_random_coordinates())

    class Meta:
        model = Location
