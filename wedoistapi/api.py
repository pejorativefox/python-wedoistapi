"""
Copyright (C) 2012 <Wedoist>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from wedoistapi.auth import WedoistHTTPAuth
from wedoistapi.handler import WedoistRequest


class WedoistCall (object):
    """
        The callable class is meant to be subclassed by the main API class. 
        It allows the API URIs to be resolved recursively using the getattr
        and call methods provided by object.

        Arguments:
            callable_cls: the class to instanciate for the recursive step. 

            auth: An instance of WedoistAuth or a subclass that provides the
                required methods.

            domain: The base uri for the web api.

            request_handler: A request handler class either WedoistRequest or
                a subclass that provides the required methods

            uriparts: A list that holds the decoded parts of the uri as strings 
            through the recursion.

        When a call is made to the toplevel class instance it is recursively 
        handed down until a __call__ is reached. The properties to the left of
        the call are converted to strings using __getattr__ and appended to 
        self.uriparts. Upon reaching the __call__ we make a request using 
        self.request_handler with the built URI and any keyword args supplied
        to the __call__.
        
    """
    def __init__(self, callable_cls, auth, domain, request_handler, uriparts=[]):
        self.uriparts = uriparts
        self.callable_cls = callable_cls
        self.domain = domain
        self.auth = auth
        self.request_handler = request_handler
        
    def __getattr__(self, k):
        ## Try to get the attrubute from the instance
        try:
            return object.__getattr__(self, k)
        ## If the attribute does not exist, assume its an part of an
        ## API URI and pass it down until a __call__ is hit.
        except AttributeError:
            return self.callable_cls(
                    domain=self.domain,
                    callable_cls=self.callable_cls, 
                    uriparts=self.uriparts + [k],
                    request_handler=self.request_handler,
                    auth = self.auth)
            
    def __call__(self, **kwargs):
        ## Build the URI from self.domain and self.uriparts
        uri = self.domain
        for part in self.uriparts:
            uri += part + '/'
        ## Build a request handler for the assembled URI
        request = self.request_handler(uri)
        ## Do the request with the kwargs and the auth cookies
        response = request.do_request(kwargs, self.auth.get_cookies())
        ## return the data from the responce instance.
        return response.get_data()


class Wedoist (WedoistCall):
    """
    Using our Python API
    ====================

    Introduction
    ------------

    Wedoistapi is a minimal and full pythonic API for wedoist.com's project 
    management application. It allows Python developers access to the entire 
    set of diverse features that Wedoist offers. 


    Install
    -------

    You can install the Wedoist API using pip:
        pip install wedoistapi
        
    Or you can download the package from the Python Package Index:
        http://pypi.python.org/pypi/wedoistapi


    Examples:
    ---------

    .. code-block:: python

        # Import the wedoist api
        from wedoistapi import Wedoist, WedoistHTTPAuth
        
        # Authenticate with the HTTP auth class.
        auth = WedoistHTTPAuth(email="foo@bar.com", password="bar")
        
        # Create an instance of the wedoist api using the user we authed to.
        wedoist = Wedoist(auth)
        
        # You can access the user's imformation in the auth objects 
        # user_data property
        default_project = auth.get_user_data()["default_project"]
        
        # To make an api call we use the names from the official api docs.
        # To access all of the active items on our users default project at
        # wedoist.com/API/Items/getAllActive we make the following call with 
        # the required POST data as keyword arguments:
        wedoist.Items.getAllActive(project_id=default_project)

    Will return all active items as a list of python dictionaries, one for each 
    item we fetched.

    .. code-block:: json

        { "date_format": 0, 
          "default_project": 42, 
          "has_to_setup": 0, 
          "partition": 1, 
          "number_of_projects": 1, 
          "email": "foo@bar.com", 
          "time_format": 0, 
          "join_date": "Sun, 13 May 2012 20:20:53", 
          "avatar": "254bd140e8520bb8e25b5d2da98244b2", 
          "full_name": "John Cardholder", 
          "timezone": "America\/Chicago", 
          "id": 23
        }

    Any API function call be called as presented in the official API
    documentation with the required POST data passed as keyword 
    arguments.

    .. code-block:: python

        # API call: wedoist.com/API/Projects/getAll
        wedoist.Projects.getAll()
        
        # API call: wedoist.com/API/Projects/get
        wedoist.Projects.get(project_id=42)

    Error Handling:
    ---------------

    More sophisticated error handling is in the works. For now the API uses 
    straight urllib2 calls to interact with Wedoist's servers. As such it throws 
    generic HTTPError when a request can not be completed. 
        See: http://docs.python.org/library/urllib2.html#urllib2.HTTPError

    """
    def __init__(self, auth, domain="https://wedoist.com/API/", 
        request_handler=WedoistRequest):
        ## Do the auth request before we init the subclass
        auth.do_auth()
        ## Initialize the base class
        WedoistCall.__init__(self, WedoistCall, auth, domain, request_handler)


