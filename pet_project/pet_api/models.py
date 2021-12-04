import uuid

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet


class TimeMixin(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Time of creation', auto_now_add=True)
    updated_at = models.DateTimeField('Last update time', auto_now=True)

    class Meta:
        abstract = True


class Photo(TimeMixin):

    file = models.ImageField('Фотография', upload_to='photos/')

    def delete(self, *args, **kwargs):
        """Delete obj with all files."""
        storage, path = self.file.storage, self.file.path
        super().delete(*args, **kwargs)
        storage.delete(path)

    def get_full_url(self):
        """Return full url to photo."""
        domain = 'http://localhost:8000' if settings.DEBUG else settings.BASE_URL
        return f'{domain}{self.file.url}'


class PetQuerySet(QuerySet):

    def get_pet_list(self, limit=20, offset=0, has_photos=None):
        """
        Return pets list.

        :param limit: Amount pets in the final query.
        :param offset: Offset from start of query.
        :param has_photos: Filter-checkbox between objects with and without photos.
            None - return all.
            False - objects without photos.
            True - objects with photos.
        """
        pet_photos = Pet.photos.through.objects.distinct('pet_id').values_list('pet_id', flat=True)

        if has_photos is False:
            pet_query = self.exclude(id__in=pet_photos)
        elif has_photos is True:
            pet_query = self.filter(id__in=pet_photos).prefetch_related('photos')
        else:
            pet_query = self.all().prefetch_related('photos')

        return pet_query.order_by('id')[offset:limit]


class Pet(TimeMixin):

    class PetTypes:
        DOG = 'dog'
        CAT = 'cat'
        CHOICES = (
            (DOG, 'Dog'),
            (CAT, 'Cat'),
        )

    name = models.CharField('Name', max_length=100)
    age = models.PositiveSmallIntegerField('Age')
    kind = models.CharField('Type', max_length=25, choices=PetTypes.CHOICES)
    photos = models.ManyToManyField(Photo, verbose_name='Photos', related_name='pets', blank=True)

    objects = PetQuerySet.as_manager()

    def __str__(self):
        return f'Pet id: {self.pk}. Name is "{self.name}"'

    def delete(self, *args, **kwargs):
        """Delete the pet with their photos."""
        for photo in self.photos.all():
            photo.delete()
        super().delete(*args, **kwargs)

    def get_info_about(self):
        """Return prepared data about the pet."""
        return {
            'id': self.pk,
            'name': self.name,
            'age': self.age,
            'type': self.kind,
            'created_at': self.created_at,
            'photos': self.get_photos(),
        }

    def get_photos(self):
        """Return list of all photos with id and url."""
        return [{
            'id': photo.pk,
            'url': photo.get_full_url()
        } for photo in self.photos.all()]

    def get_next_photo_name(self):
        """Return next name for new pet photo."""
        count = self.photos.count() + 1
        return f'pet_{self.pk}_img_{count}.jpg'

    @classmethod
    def multi_delete(cls, ids_list):
        """Multiple deleting pets with their photos."""
        deleted_count = cls.objects.filter(id__in=ids_list).count()
        result = {
            'deleted': deleted_count,
            'errors': []
        }
        for pk in ids_list:
            try:
                pet = cls.objects.get(pk=pk)
            except cls.DoesNotExist:
                result['errors'].append({
                    'id': pk,
                    'error': 'Pet with the matching ID was not found.'
                })
            else:
                pet.delete()

        return result
