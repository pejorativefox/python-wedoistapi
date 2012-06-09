Using our Python API
====================

Introduction
------------

Wedoistapi is a minimal and full pythonic API for wedoist.com's project management application. It allows Python developers access to the entire set of diverse features that Wedoist offers. 


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

Will return all active items as a list of python dictionaries, one for each item we fetched.

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

More sophisticated error handling is in the works. For now the API uses straight urllib2 calls to interact with Wedoist's servers. As such it throws generic HTTPError when a request can not be completed. See: http://docs.python.org/library/urllib2.html#urllib2.HTTPError


