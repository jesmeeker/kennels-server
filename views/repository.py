DATABASE = {
    'animals':
    [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 1,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 1,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }],
    'customers': [
        {
            "id": 1,
            "full_name": "Ryan Tanay",
            "email": "ryan.tanay@gmail.com"
        }
    ],
    'employees': [
        {
            "id": 1,
            "name": "Jenna Solis",
            "address": "20 Page Terrace",
            "locationId": 3
        }
    ],
    'locations': [
        {
            "id": 1,
            "name": "Nashville North",
            "address": "8422 Johnson Pike"
        },
        {
            "id": 2,
            "name": "Nashville South",
            "address": "209 Emory Drive"
        }
    ]
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, id):
    """For GET requests to a single resource"""
    requested_resource = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for e in DATABASE[resource]:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if e["id"] == id:
            requested_resource = e

            if resource == 'animals':
                for i in DATABASE['locations']:
                    matching_location = None
                    if i["id"] == requested_resource["locationId"]:
                        matching_location = i
                        requested_resource["location"] = matching_location

                for j in DATABASE['customers']:
                    matching_customer = None
                    if j["id"] == requested_resource["customerId"]:
                        matching_customer = j
                        requested_resource["customer"] = matching_customer

            del requested_resource["locationId"]
            del requested_resource["customerId"]

    return requested_resource


def create():
    """For POST requests to a collection"""
    pass


def update():
    """For PUT requests to a single resource"""
    pass


def delete():
    """For DELETE requests to a single resource"""
    pass
