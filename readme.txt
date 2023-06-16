# Flight ticket booking system
This is part task round for on campus round DEVREV

`console.java` is the application where users/admins can assess the system to book tickets or manage tickets.
It is not connected to sql database, rather, it makes api calls to fetch the results from the server.
`server.py` contains server side code which receives api calls ans populate them in sqlite3 database in python.
I have developed a server side code which can be usefull in the case when a frontend can make api calls in different languages and fetch data from the database.

## RUN
To run this project, first run `server.py` to start the server and then console.java in separate cmd prompt. Java application makes api calls to local server to stimulate the environment of different users using the java application and a centralized server to store the data.

visit https://github.com/ultralegendary/devrev

not able to upload code files in this form.