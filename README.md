# ServerLogging

Server logging for :-
  1. The server maintains a log of its uptime (In Seconds) 
  2. The server maintains a log of all the requests coming to it. With
     following elements:
       a. Timestamp of request
       b. API name
       c. Response Code

Follow below steps run the project (ubuntu OS) :

1. Make the directory on system with any name ex: Server_Dir
2. Command to enter into Server_Dir ->  cd Server_Dir 
3. Now run the command to create virtual env -> virtualenv env (virtual environement name)
4. Type ls to see env is created.
5. Now activate env with command -> source env/bin/activate
6. You are now in virtualenv (env).
7. Command to enter into ServerLogging -> cd ServerLogging
8. Now ls command to see files inside the directory, Here you see requirements.txt.
9. Install the requirement in env with -> pip istall -r requirements.txt
10. Now goto juntrax_server with cd juntrax_server. ls to see files here you will see the manage.py file.
11. Now run the Django Local Server with python manage.py runserver
12. If server run fine then. Run command to migrate the database - python manage.py makemigrations and 
    python manage.py migrate
13. Now again run the django server with 11 point.
14. Open the link http://127.0.0.1:8000/ in browser. If no error then you will see the 
    ^admin/
    ^api/
    api's are there.
15. Now change the url with http://127.0.0.1:8000/api/
16. Now there are API's you will see : 

{
    "serveruptime": "http://127.0.0.1:8000/api/serveruptime/",
    "requestlogging": "http://127.0.0.1:8000/api/requestlogging/",
    "googlereversegeocoding": "http://127.0.0.1:8000/api/googlereversegeocoding/",
    "limitchange": "http://127.0.0.1:8000/api/limitchange/"
}

17. Now click on each API. You will get the result.
