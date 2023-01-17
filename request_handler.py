import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import all, retrieve, create, update, delete

method_mapper = {
    'single': retrieve, 'all': all
    # 'customers': {'single': get_single_customer, 'all': get_all_customers},
    # 'employees': {'single': get_single_employee, 'all': get_all_employees},
    # 'locations': {'single': get_single_location, 'all': get_all_locations}
}

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def get_all_or_single(self, resource, id):
        """Determines whether the client is needing all items or a single item and then calls the correct function.
        """
        if id is not None:
            response = method_mapper["single"](resource, id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper["all"](resource)

        return response

    def parse_url(self, path):
        """Splits the URL into two variables"""
        # This is a Docstring it should be at the beginning of all classes and functions
        # It gives a description of the class or function

        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server """

        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_data = None

        if resource == "animals":
            if "name" in post_body and "species" in post_body and "locationId" in post_body and "customerId" in post_body and "status" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"species is required" if "species" not in post_body else ""} {"locationId is required" if "locationId" not in post_body else ""} {"customerId is required" if "customerId" not in post_body else ""} {"status is required" if "status" not in post_body else ""}'
                }

        if resource == "customers":
            if "full_name" in post_body and "email" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"full_name is required" if "full_name" not in post_body else ""} {"email is required" if "email" not in post_body else ""}'
                }

        if resource == "employees":
            if "name" in post_body and "address" in post_body and "locationId" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""} {"locationId is required" if "locationId" not in post_body else ""}'
                }

        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
                }

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_data).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        update(resource, id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Set a 204 response code
        self._set_headers(204)
        # Delete a single item from the list
        delete(resource, id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
