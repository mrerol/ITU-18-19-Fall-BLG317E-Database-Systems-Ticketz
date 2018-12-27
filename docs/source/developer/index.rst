Developer Guide
===============

Database Design
---------------

There are 14 tables in our database. Tables and corresponding members are listed in Table Distribution below.

Table Distribution
^^^^^^^^^^^^^^^^^^^

:Ufuk DEMİR:

   * users
   * city
   * terminal
   * sale
   * user_has_sale

:Muhammed Raşit EROL:

   * firms
   * drivers
   * vehicles
   * images_for_firms

:Abdullah AKGÜL:

   * expeditions
   * tickets
   * seats
   * hotels
   * images



**include the E/R diagram(s)**

Code
----

There are two types of database class definitions that are listed below.


.. code-block:: python

    class hotel_database:
        def __init__(self):
            self.hotel = self.Hotel()





.. code-block:: python

      class CityDao(BaseDao):
        def __init__(self):
            super(CityDao,self).__init__()





.. toctree::

   member1
   member2
   member3
