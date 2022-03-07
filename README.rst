==================
Computer Dashboard
==================


Computer Dashboard is a reasonable test in order to better understand websockets.


* Free software: MIT license

Prerequisites:
--------------

- ``npm``
- ``python``
- any kind of virtual environment for Python (optional)

How to Configure it:
--------------------

First install dependencies on Python:

- create a virtual environment for Python packages (this is optional)
- then install Python dependencies:

``$ pip3 install -r api/requirements.txt``

Then install dependencies for frontend:

``$ cd dashboard``

``$ npm install``


How to Use it
-------------

First, run backend part:

``$ python3 api/api.py``

Then, go to frontend folder and run it:

``$ cd dashboard``

``$ npm run serve``

How to Test it
--------------

Just run ``pytest``

``$ pytest``

Features
--------

* TODO:

- Finish killing process

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
