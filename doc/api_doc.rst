Pet API version 0.0.1
===================

Welcome pet-api documentation. Here is description all methods.

API is using only http protocol. You need the secret key to work. His header is called "X-API-KEY". Value can be seen in the settings.py file :)

Temporary server address: http://134.122.59.240

API has 4 available methods
----------------

POST/pets
~~~~~~~~~~
Create pet.

Request body::

   {
        "name": "Name",
        "age": 5,
        "kind": "dog"
    }

Response body::

   {
        "id": "82d760b9-c86f-47e8-acdb-08a73b8b3906",
        "name": "Name",
        "age": 5,
        "type": "dog",
        "photos": [],
        "created_at": "2021-12-04T09:34:03.967Z"
    }


GET/pets
~~~~
Get pets list.

Optional parameters:

* **limit** - Amount pets in the final query.
* **offset** - Offset from start of query.
* **has_photos** - Filter-checkbox between objects with and without photos.

    without - return all.
    False - objects without photos.
    True - objects with photos.

Response body::

   {
    "count": 1,
    "items": [
        {
            "id": "82d760b9-c86f-47e8-acdb-08a73b8b3906",
            "name": "Name",
            "age": 5,
            "type": "dog",
            "created_at": "2021-12-04T09:34:03.967Z",
            "photos": [
                {
                    "id": "4827a227-6d87-47b3-929b-7192935411dc",
                    "url": "http://domain/media/photos/pet_82d760b9-c86f-47e8-acdb-08a73b8b3906_img_1.jpg"
                },
            ]
        }
    ]
    }

DELETE/pets
~~~~~~~~
Delete pets with photos.

Request body::

   {
        "ids": [
            "82d760b9-c86f-47e8-acdb-08a73b8b3906",
            "4827a227-6d87-47b3-929b-7192935411dc",
        ]
    }

Response body::

   {
    "deleted": 1,
    "errors": [
        {
            "id": "82d760b9-c86f-47e8-acdb-08a73b8b3906",
            "error": "Pet with the matching ID was not found."
        }
    ]
    }

POST/pets/id/photo
~~~~~~~~
Upload pets photo.

* **file: binary**

Response body::

   {
        "id": "a6ee0515-184c-4882-bb3a-98b08297319c",
        "url": "http://domain/media/photos/pet_82d760b9-c86f-47e8-acdb-08a73b8b3906_img_4.jpg"
    }

