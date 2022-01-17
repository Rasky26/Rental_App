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

<table>
  <thead>
    <tr>
      <th>Main Function</th>
      <th>Sub Function</th>
      <th>Route</th>
      <th>Method</th>
      <th>Model</th>
      <th>View</th>
      <th>Serializer</th>
      <th>URL</th>
      <th>Tests</th>
      <th>Improvements</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>User Account</b></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Register</td>
      <td>accounts/registration</td>
      <td>POST</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Add email confirmation before approval</td>
    </tr>
    <tr>
      <td></td>
      <td>Login</td>
      <td>accounts/login</td>
      <td>POST</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Logout (current browser)</td>
      <td>accounts/logout</td>
      <td>POST</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Logoutall (all browsers)</td>
      <td>accounts/logoutall</td>
      <td>POST</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td></td>
    </tr>
    <tr>
      <td><b>Buildings</b></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Add building with <b>NO</b> exising company</td>
      <td>buildings/no-company/new-building</td>
      <td>POST</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Add building with exising company</td>
      <td>buildings/__company-pk-value__/new-building</td>
      <td>POST</td>
      <td>Done</td>
      <td>In development</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
