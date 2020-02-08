.. _installation:

============
Installation
============

**django-dag-cte** is available on `pypi <https://pypi.org/>`_, so installation into your python virtual environment is dead
simple:

.. code-block:: py

    pip install django-dag-cte

Don't have a virtual environment with pip? You probably should! ``pyenv`` is your friend. Google it.

You'll need to install it as an app in your django settings:

.. code-block:: py

    INSTALLED_APPS = [
        ...
        'django_dag_cte'
        ...

Then run migrations:

.. code-block:: bash

    python manage.py makemigrations


.. _compilation:

Compilation
============

There is presently no need to compile **django-dag-cte**, as it's written entirely in python. Yay.
