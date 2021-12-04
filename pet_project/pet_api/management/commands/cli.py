import pprint

from django.core.management.base import BaseCommand
from ... import models


class Command(BaseCommand):
    """Show all pets into stdout."""

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--has_photos', action='store_true', help='Use it if you going to get photos')
        parser.set_defaults(has_photos=False)

    def handle(self, *labels, **options):
        pet_list = []
        result = {
            'pets': pet_list
        }
        has_photos = options.get('has_photos')
        limit = models.Pet.objects.count()

        for pet in models.Pet.objects.get_pet_list(limit=limit, has_photos=has_photos or None):
            pet_list.append(self.make_pet_data(pet, has_photos))

        pprint.pprint(result)

    @staticmethod
    def make_pet_data(pet, has_photos):
        pet_data = {
            'id': pet.id,
            'name': pet.name,
            'age': pet.age,
            'type': pet.get_kind_display(),
            'created_at': pet.created_at,
        }

        if has_photos:
            pet_data['photos'] = [photo_data['url'] for photo_data in pet.get_photos()]

        return pet_data
