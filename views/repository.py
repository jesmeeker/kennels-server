import sqlite3
import json
from models import Animal, Customer, Employee, Location

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
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if resource == 'animals':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM animal a
            """)

            # Initialize an empty list to hold all animal representations
            animals = []

            # Convert rows of data into a Python list
            dataset = db_cursor.fetchall()

            # Iterate list of data returned from database
            for row in dataset:

                # Create an animal instance from the current row.
                # Note that the database fields are specified in
                # exact order of the parameters defined in the
                # Animal class above.
                animal = Animal(row['id'], row['name'], row['breed'],
                                row['status'], row['location_id'],
                                row['customer_id'])

                animals.append(animal.__dict__)

            return animals

        if resource == 'customers':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.email,
                a.password
            FROM customer a
            """)

            # Initialize an empty list to hold all animal representations
            customers = []

            # Convert rows of data into a Python list
            dataset = db_cursor.fetchall()

            # Iterate list of data returned from database
            for row in dataset:

                # Create an animal instance from the current row.
                # Note that the database fields are specified in
                # exact order of the parameters defined in the
                # Animal class above.
                customer = Customer(
                    row['id'], row['name'], row['address'], row['email'], row['password'])

                customers.append(customer.__dict__)

            return customers

        if resource == 'employees':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.location_id
            FROM employee a
            """)

            # Initialize an empty list to hold all animal representations
            employees = []

            # Convert rows of data into a Python list
            dataset = db_cursor.fetchall()

            # Iterate list of data returned from database
            for row in dataset:

                # Create an animal instance from the current row.
                # Note that the database fields are specified in
                # exact order of the parameters defined in the
                # Animal class above.
                employee = Employee(
                    row['id'], row['name'], row['address'], row['location_id'])

                employees.append(employee.__dict__)

            return employees

        if resource == 'locations':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address
            FROM location a
            """)

            # Initialize an empty list to hold all animal representations
            locations = []

            # Convert rows of data into a Python list
            dataset = db_cursor.fetchall()

            # Iterate list of data returned from database
            for row in dataset:

                # Create an animal instance from the current row.
                # Note that the database fields are specified in
                # exact order of the parameters defined in the
                # Animal class above.
                location = Location(row['id'], row['name'], row['address'])

                locations.append(location.__dict__)

            return locations

# def all(resource):
#     """For GET requests to collection"""
#     return DATABASE[resource]


def retrieve(resource, id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        if resource == 'animals':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM animal a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

            return animal.__dict__

        if resource == 'customers':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.email,
                a.password
            FROM customer a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            customer = Customer(
                data['id'], data['name'], data['address'], data['email'], data['password'])

            return customer.__dict__

        if resource == 'employees':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.location_id
            FROM employee a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            employee = Employee(
                data['id'], data['name'], data['address'], data['location_id'])

            return employee.__dict__

        if resource == 'locations':
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address
            FROM location a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            location = Location(
                data['id'], data['name'], data['address'])

            return location.__dict__
# def retrieve(resource, id):
#     """For GET requests to a single resource"""
#     requested_resource = None

#     # Iterate the ANIMALS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for e in DATABASE[resource]:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if e["id"] == id:
#             requested_resource = e

#             if resource == 'animals':
#                 for i in DATABASE['locations']:
#                     matching_location = None
#                     if i["id"] == requested_resource["locationId"]:
#                         matching_location = i
#                         requested_resource["location"] = matching_location

#                 for j in DATABASE['customers']:
#                     matching_customer = None
#                     if j["id"] == requested_resource["customerId"]:
#                         matching_customer = j
#                         requested_resource["customer"] = matching_customer

#             del requested_resource["locationId"]
#             del requested_resource["customerId"]

#     return requested_resource


def get_customer_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, (email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(
                row['id'], row['name'], row['address'], row['email'], row['password'])
            customers.append(customer.__dict__)

    return customers

def get_animal_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)

    return animals

def get_animal_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.status = ?
        """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)

    return animals

def get_employee_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id
        FROM employee a
        WHERE a.location_id = ?
        """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return employees


def create(resource, post_body):
    """For POST requests to a collection"""

    # Get the id value of the last animal in the list
    max_id = DATABASE[resource][-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    post_body["id"] = new_id

    # Add the animal dictionary to the list
    DATABASE[resource].append(post_body)

    # Return the dictionary with `id` property added
    return post_body


def update(resource, id, post_body):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            # Found the animal. Update the value.
            DATABASE[resource][index] = post_body
            break


def delete(resource, id):
    """For DELETE requests to a single resource"""
    resource_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            # Found the animal. Store the current index.
            resource_index = index

    # If the animal was found, use pop(int) to remove it from list
    if resource_index >= 0:
        DATABASE[resource].pop(resource_index)
