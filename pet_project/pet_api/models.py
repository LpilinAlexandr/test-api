from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet


class TimeMixin(models.Model):

    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Время последнего обновления', auto_now=True)

    class Meta:
        abstract = True


class Photo(TimeMixin):
    file = models.ImageField('Фотография', upload_to='photos/')

    def get_full_url(self):
        domain = 'http://localhost:8000' if settings.DEBUG else settings.BASE_URL
        return f'{domain}{self.file.url}'

    def delete(self, *args, **kwargs):
        """Удаление файла вместе с объектом модели."""
        storage, path = self.file.storage, self.file.path
        super().delete(*args, **kwargs)
        storage.delete(path)


class PetQuerySet(QuerySet):

    def get_pet_list(self, limit=20, offset=0, has_photos=None):
        """
        Получить список питомцев.

        :param limit: лимит по кол-ву возвращаемых питомцев в запросе
        :param offset: сдвиг по кверисету
        :param has_photos: переключатель фильтрации по наличию фотографий:
            Если параметр не передан - возвращается всё
            Если передан False - возвращаются только питомцы без фотографий
            Если передан True - возвращаются только питомцы с фотографиями

        :return: Кверисет питомцев
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
            (DOG, 'Собака'),
            (CAT, 'Кошка'),
        )

    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст')
    kind = models.CharField('Тип', max_length=25, choices=PetTypes.CHOICES)
    photos = models.ManyToManyField(Photo, verbose_name='Фото', related_name='pets', blank=True)

    objects = PetQuerySet.as_manager()

    def __str__(self):
        return f'Pet id: {self.pk}. Name is "{self.name}"'

    def get_info_about(self):
        return {
            'id': self.pk,
            'name': self.name,
            'age': self.age,
            'type': self.kind,
            'created_at': self.created_at,
            'photos': self.get_photos(),
        }

    def get_photos(self):
        return [{
            'id': photo.pk,
            'url': photo.get_full_url()
        } for photo in self.photos.all()]

    def get_next_photo_name(self):
        count = self.photos.count() + 1
        return f'pet_{self.pk}_img_{count}.jpg'

    def delete(self, *args, **kwargs):
        """Удаление питомца вместа с фотографиями."""
        for photo in self.photos.all():
            photo.delete()
        super().delete(*args, **kwargs)

    @classmethod
    def multi_delete(cls, ids_list):
        """Множественное удаление питомцев вместе с фотографиями."""
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
