# Mountain Peak

## Description
This project tests the backend skills.
It uses Django, a postgresql database and is deployed with Docker (and docker-compose).
It is a REST API accessible by 2 endpoints.

## How to deploy
Before all, you have to install Docker and docker-compose (cf. https://docs.docker.com/get-docker/).
Then 4 commands are required to deploy this project (with Windows, remove the prefix 'sudo'):
- ``sudo docker-compose run django_peak_api sh -c "python manage.py makemigrations"``
- ``sudo docker-compose run django_peak_api sh -c "python manage.py migrate"``
- ``sudo docker-compose build``
- ``sudo docker-compose up``

## How to use
There are 5 JSON object formats:
  - POST format: ``{'name': name, 'lat': latitude, 'lon': longitude, 'altitude': altitude}``
    <br>Where:
    - name is a string as 'Everest' with a length lower than 100 characters 
    (we consider that there is no peak with such a long name).
    - latitude is a float in the interval [-90.0, 90.0] 
    and represents the latitude of a peak in DD (decimal degree format)
    - longitude is a float and represents the latitude of a peak in DD (decimal degree format)
    - altitude is a float in the interval [-16383.0, 16383.0]. 
    Indeed, the highest peak is the Everest mount at 8849m and the deepest place is the Mariana Trench at -10.920m.
  - GET format: ``{'name': name}``
  <br>Where name is a string (and there is a peak in the database which has this name)
  - Successful deletion format: ``{'action': name + 'has been deleted'}``
  <br>Where name is the string of the deleted peak
  - Error format: ``{'error': exception}``
  <br>Where exception is a message explaining why the error occurred.
  - Zone format: ``{'lat_ne': latitude1, 'lat_sw': latitude2, 'lon_ne': longitude1, 'lon_sw': longitude2}``
  <br>Where longitude1 and longitude2 are floats and latitude1 and latitude2 are floats between -90.0 and 90.0.

<br>

There are 2 endpoints:
- ``http://localhost:8000/zone`` which can be accessed with a GET request.
<br>It returns a list of the peaks in a given geographical bounding box (the peaks are in the POST format). 
This box is a rectangle on the map which can be described by its 4 vertices.
<br>It requires 4 parameters in the zone format:
  - lat_ne: latitude of the vertex at the northeast of all the peaks in the box,
  - lat_sw: latitude of the vertex at the southwest of all the peaks in the box,
  - lon_ne: longitude of the vertex at the northeast of all the peaks in the box,
  - lat_sw: longitude of the vertex at the southwest of all the peaks in the box.
- ``http://localhost:8000/peak`` which can be accessed with 4 methods:
  - get: 
    - Required: GET request in GET format
    - Returned:
      - An error 500 (in the error format) if there is no peak with the asked name registered in the database
      - Otherwise, it returns the peak's data in the POST format.
  - post: 
    - Required: POST request in POST format
    - Action: If there is no error 500, insertion in the database of the peak given in the request.
    - Returned: 
      - An error 500 (in the error format) if a peak with the name given in the request is already in the database, 
      if the altitude is not in the interval [-16383, 16383] 
      or if the latitude is not in the interval [-90, 90].
      - Otherwise, it returns the peak's data in the POST format.
  - put:
    - Required: PUT request in POST format
    - Action: If there is no error 500, modify the peak's data in the database 
    with the peak's data given in the request.
    - Returned:
      - An error 500 (in the error format) if a peak with the name given in the request is already in the database, 
      if the altitude is not in the interval [-16383, 16383] 
      or if the latitude is not in the interval [-90, 90]
      or if there is no peak with the name given in the request in the database.
      - Otherwise, it returns the peak's data in the POST format.
  - delete:
    - Required: DELETE request in GET format
    - Action: If there is no error 500, remove the peak with the name given in the request from the database
    - Returned:
      - An error 500 (in the error format) if there is no peak with the name given in the request in the database.
      - Otherwise, it returns a successful message in the successful deletion format.

<br>
You can send requests with the client I implemented in client/main.py (in another terminal) by running the command 
``python client/main.py localhost_ipaddress`` where localhost_ipaddress is your localhost ip address 
(127.0.0.1 for Windows and 0.0.0.0 otherwise)
<br><b>Warning</b>: you must install python and the requests module if you use this solution.
<br>Of course, any other method to send a request (like the linux command line curl) should work.