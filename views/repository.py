import sqlite3
import json
from models import Animal, Customer, Employee, Location


def all(resource, query_params):
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""
        where_clause = ""

        
        # Write the SQL query to get the information you want
        if resource == 'animals':
            if len(query_params) != 0:
                param = query_params[0]
                [qs_key, qs_value] = param.split("=")

                sort_by = ""
                where_clause = ""

                if qs_key == "_sortBy":
                    if qs_value == "location":
                        # if qs_value == 'location':
                        sort_by = " ORDER BY location_id"

                    if qs_value == "status":
                        sort_by = " ORDER BY status ASC"

                elif qs_key == "location_id":
                    where_clause = f"WHERE a.location_id = {qs_value}"

                elif qs_key == "status":
                    where_clause = f"WHERE a.status = '{qs_value}'"

                sql_to_execute = f"""
                    SELECT
                        a.id,
                        a.name,
                        a.breed,
                        a.status,
                        a.location_id,
                        a.customer_id,
                        l.name location_name,
                        l.address location_address,
                        c.name customer_name,
                        c.address customer_address,
                        c.email customer_email
                    FROM Animal a
                    JOIN `Location` l
                        ON l.id = a.location_id
                    JOIN `Customer` c
                        ON c.id = a.location_id
                    {where_clause}
                    {sort_by}"""

                db_cursor.execute(sql_to_execute)

                animals = []

                # Convert rows of data into a Python list
                dataset = db_cursor.fetchall()

                # Iterate list of data returned from database
                for row in dataset:

                    # Create an animal instance from the current row.
                    # Note that the database fields are specified in
                    # exact order of the parameters defined in the
                    # Animal class above.
                    animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])

                    # Create a Location instance from the current row
                    location = Location(
                        row['location_id'], row['location_name'], row['location_address'])

                    # Add the dictionary representation of the location to the animal
                    animal.location = location.__dict__
                    # Create a Location instance from the current row
                    customer = Customer(
                            row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'])

                # Add the dictionary representation of the location to the animal
                    animal.customer = customer.__dict__

                    # Add the dictionary representation of the animal to the list
                    animals.append(animal.__dict__)

                return animals

            
                    # if qs_value == 'customer':
                    #     sort_by = " ORDER BY customer_id"
                    #     sql_to_execute = f"""
                    #         SELECT
                    #             a.id,
                    #             a.name,
                    #             a.breed,
                    #             a.status,
                    #             a.location_id,
                    #             a.customer_id,
                    #             c.name customer_name,
                    #             c.address customer_address,
                    #             c.email customer_email
                    #         FROM Animal a
                    #         JOIN `Customer` c
                    #             ON c.id = a.location_id
                    #         {sort_by}"""

                    #     db_cursor.execute(sql_to_execute)

                    #     animals = []

                    #     # Convert rows of data into a Python list
                    #     dataset = db_cursor.fetchall()

                    #     # Iterate list of data returned from database
                    #     for row in dataset:

                    #         # Create an animal instance from the current row.
                    #         # Note that the database fields are specified in
                    #         # exact order of the parameters defined in the
                    #         # Animal class above.
                    #         animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])

                    #         # Create a Location instance from the current row
                    #         customer = Customer(
                    #             row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'])

                    # # Add the dictionary representation of the location to the animal
                    #         animal.customer = customer.__dict__
                    #         # Add the dictionary representation of the animal to the list
                    #         animals.append(animal.__dict__)

                    #     return animals
                
            else:
                db_cursor.execute("""
                SELECT
                    a.id,
                    a.name,
                    a.breed,
                    a.status,
                    a.location_id,
                    a.customer_id,
                    l.name location_name,
                    l.address location_address,
                    c.name customer_name,
                    c.address customer_address,
                    c.email customer_email
                FROM Animal a
                JOIN Location l 
                    ON l.id = a.location_id
                JOIN Customer c
                    ON c.id = a.customer_id
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
                    animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])

                    # Create a Location instance from the current row
                    location = Location(
                        row['location_id'], row['location_name'], row['location_address'])

                    # Add the dictionary representation of the location to the animal
                    animal.location = location.__dict__

                    # Create a Customer instance from the current row
                    customer = Customer(
                        row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'])

                    # Add the dictionary representation of the location to the animal
                    animal.customer = customer.__dict__
                    # Add the dictionary representation of the animal to the list
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
                a.location_id,
                l.name location_name,
                l.address location_address
            FROM employee a
            JOIN location l
                ON a.location_id = l.id
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

                location = Location(
                    row['id'], row['location_name'], row['location_address'])

                # Add the dictionary representation of the location to the animal
                employee.location = location.__dict__

            return employees

        if resource == 'locations':
            db_cursor.execute("""
            SELECT
            COUNT(a.location_id) AS animals,
                l.id,
                l.name,
                l.address
            FROM location l
            JOIN animal a
                ON a.location_id = l.id
            GROUP BY l.id
            """)

            # Initialize an empty list to hold all animal representations
            locations = []

            # Convert rows of data into a Python list
            dataset = db_cursor.fetchall()

            # Iterate list of data returned from database
            for row in dataset:

                location = Location(row['id'], row['name'], row['address'])
                location.animals = (row['animals'])

                locations.append(location.__dict__)

            return locations

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
                    a.customer_id,
                    l.name location_name,
                    l.address location_address,
                    c.name customer_name,
                    c.address customer_address,
                    c.email customer_email
                FROM Animal a
                JOIN Location l 
                    ON l.id = a.location_id
                JOIN Customer c
                    ON c.id = a.customer_id
                WHERE a.id =?
                """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

            location = Location(
                        data['location_id'], data['location_name'], data['location_address'])

                    # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__

                    # Create a Customer instance from the current row
            customer = Customer(
                data['customer_id'], data['customer_name'], data['customer_address'], data['customer_email'])

            # Add the dictionary representation of the location to the animal
            animal.customer = customer.__dict__

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

def create(resource, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        if resource == 'animals':
            db_cursor.execute("""
            INSERT INTO Animal
                ( name, breed, status, location_id, customer_id )
            VALUES
                ( ?, ?, ?, ?, ?);
            """, (new_animal['name'], new_animal['breed'],
                new_animal['status'], new_animal['location_id'],
                new_animal['customer_id'], ))

            # The `lastrowid` property on the cursor will return
            # the primary key of the last thing that got added to
            # the database.
            id = db_cursor.lastrowid

            # Add the `id` property to the animal dictionary that
            # was sent by the client so that the client sees the
            # primary key in the response.
            new_animal['id'] = id


            return new_animal
# def create(resource, post_body):
#     """For POST requests to a collection"""

#     # Get the id value of the last animal in the list
#     max_id = DATABASE[resource][-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the animal dictionary
#     post_body["id"] = new_id

#     # Add the animal dictionary to the list
#     DATABASE[resource].append(post_body)

#     # Return the dictionary with `id` property added
#     return post_body


def update(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'], new_animal['status'], new_animal['location_id'], new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
# def update(resource, id, post_body):
#     # Iterate the ANIMALS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, item in enumerate(DATABASE[resource]):
#         if item["id"] == id:
#             # Found the animal. Update the value.
#             DATABASE[resource][index] = post_body
#             break


# def delete(resource, id):
#     """For DELETE requests to a single resource"""
#     resource_index = -1

#     # Iterate the ANIMALS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, item in enumerate(DATABASE[resource]):
#         if item["id"] == id:
#             # Found the animal. Store the current index.
#             resource_index = index

#     # If the animal was found, use pop(int) to remove it from list
#     if resource_index >= 0:
#         DATABASE[resource].pop(resource_index)

def delete(resource, id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        if resource == 'animals':
            db_cursor.execute("""
            DELETE FROM animal
            WHERE id = ?
            """, (id, ))
