# Rental_App

Rental App Info

<hr>
Django server that works to automate as much of the apartment management process as necessary.

...

Active APIs:

<hr>

User registration:
URL = /'accounts/registration'

    Method: POST -> data={username, password}
    Responses:
        Success -> {token, expiry}
        Error -> {registration-errors: errors: [username, password]}
