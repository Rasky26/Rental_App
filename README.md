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
      <td></td>
      <td>Change Password</td>
      <td></td>
      <td></td>
      <td>Done</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Forgot Password</td>
      <td></td>
      <td></td>
      <td>Done</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
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
      <td>buildings/{company-pk-value}/new-building</td>
      <td>POST</td>
      <td>Done</td>
      <td>In development</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Edit a building</td>
      <td>buildings/{building-pk-value}/new-building</td>
      <td>PATCH</td>
      <td>Done</td>
      <td>In development</td>
      <td></td>
      <td>In development</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Retrieve a building</td>
      <td></td>
      <td>GET</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Delete a building</td>
      <td></td>
      <td>DELETE</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><b>Change Log</b></td>
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
      <td>Get list of changes</td>
      <td></td>
      <td>GET</td>
      <td>Done</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><b>Companies</b></td>
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
      <td>Create company</td>
      <td>companies/create</td>
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
      <td>Retrieve company</td>
      <td></td>
      <td>GET</td>
      <td>Done</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Update company</td>
      <td></td>
      <td>PATCH</td>
      <td>Done</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Delete company</td>
      <td></td>
      <td>DELETE</td>
      <td>Done</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Invite Users to company</td>
      <td>companies/invite/{company-pk-value}</td>
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
      <td>Upload documents to company</td>
      <td>companies/{company-pk-value}/upload-document</td>
      <td>POST</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td></td>
    </tr>
    <tr>
      <td><b>Contacts</b></td>
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
      <td>Edit address</td>
      <td></td>
      <td>PATCH</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Edit contact</td>
      <td></td>
      <td>PATCH</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><b>Documents</b></td>
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
      <td>Edit document</td>
      <td></td>
      <td>PATCH</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Edit image</td>
      <td></td>
      <td>PATCH</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><b>General Ledger</b></td>
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
      <td>Create general ledger account</td>
      <td></td>
      <td>POST</td>
      <td>In development</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Only make GL's when new entities are made?</td>
    </tr>
    <tr>
      <td></td>
      <td>Update general ledger account</td>
      <td></td>
      <td>PATCH</td>
      <td>In development</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Retrieve general ledger account</td>
      <td></td>
      <td>GET</td>
      <td>In development</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Add functions to get cash with time / timeframes</td>
    </tr>
    <tr>
      <td></td>
      <td>Delete general ledger account</td>
      <td></td>
      <td>DELETE</td>
      <td>In development</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Do not allow deletion, only closure</td>
    </tr>
    <tr>
      <td><b>Notes</b></td>
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
      <td>Get & Update note</td>
      <td>notes/{note-pk-value}/update</td>
      <td>GET / PATCH</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td>Done</td>
      <td></td>
    </tr>
  </tbody>
</table>
