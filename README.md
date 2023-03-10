# taxi-service

Django project for managing taxi service


## Check it out!
[Taxi service deployed to Render](https://taxi-service-7a0v.onrender.com)



For not admin:

login: user

password: pass12345

For admin:

login: test_admin

password: adminpass123


## Demo
![Website Interface](demo-img/demo.png)

# Installation

Python3 must be already installed


```shell
git clone https://github.com/Pavilion4ik/taxi-service.git
cd taxi_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
set DJANGO_DEBUG=<False to run in DEBUG=False or True for DEBUG=True>
set SECRET_KEY=<your SECRET_KEY>
set DATABASE_URL=<your DATABASE_URL>
python manage.py runserver
```

# Features

* Authentication functionality for Driver/User
* Managing cars, drivers and manufacturers directly from website
* Powerful admin panel for advanced  managing
* Possibility of commenting and rating of car
* Functionality of adding avatars for drivers and images for cars
