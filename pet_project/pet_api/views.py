import io
import json

from django.core.files.images import ImageFile
from django.db.transaction import atomic
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from . import forms as api_forms
from . import models as api_models


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(atomic, name='dispatch')
class PetView(View):

    create_form = api_forms.PetForm
    list_form = api_forms.PetListForm

    def get(self, request):
        """Получить список питомцев."""
        form = self.list_form(request.GET)
        if form.is_valid():
            pet_query = api_models.Pet.objects.get_pet_list(**form.cleaned_data)
            response = {
                'count': pet_query.count(),
                'items': [pet.get_info_about() for pet in pet_query]
            }
            return JsonResponse(response)

        return JsonResponse({'errors': 'Invalid params.'}, status=400)

    def post(self, request):
        """Создать питомца."""
        data = self.get_data(request)
        form = self.create_form(data)

        if form.is_valid():
            obj = form.save()
            return JsonResponse({
                    'id': obj.id,
                    'name': obj.name,
                    'age': obj.age,
                    'type': obj.kind,
                    'photos': [],
                    'created_at': obj.created_at,
                })

        error_text = f'Parameters are missing or passed incorrectly in the following fields: {[f for f in form.errors]}'
        return JsonResponse({'errors': error_text}, status=400)

    def delete(self, request):
        """Удалить питомцев вместе с фотографиями."""
        data = self.get_data(request)

        if 'ids' in data and isinstance(data['ids'], list):
            ids = [id for id in data['ids'] if isinstance(id, int)]
            delete_result = api_models.Pet.multi_delete(ids)
            return JsonResponse(delete_result)

        return JsonResponse({'errors': 'Invalid params.'}, status=400)

    @staticmethod
    def get_data(request):
        data = request.POST.copy()
        if request.body:
            data.update(json.loads(request.body.decode()))
        return data


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(atomic, name='dispatch')
class PhotoUploadView(View):
    """Загрузка фотографии питомца."""

    def post(self, request, pet_id):
        """Загрузить фото питомца."""
        pet = api_models.Pet.objects.filter(id=pet_id).first()
        if pet and request.body:
            image = ImageFile(io.BytesIO(request.body), name=pet.get_next_photo_name())
            new_photo = api_models.Photo.objects.create(file=image)
            pet.photos.add(new_photo)
            return JsonResponse({
                'id': new_photo.id,
                'url': new_photo.get_full_url()
            })

        return JsonResponse({'errors': 'Invalid params.'}, status=400)
