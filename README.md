# django-ecommerce-demo
The Django-Ecommerce is an open-source project initiative and tutorial series built with Python and the Django Framework.

[sumber](https://github.com/veryacademy/django-ecommerce-project)

## Getting Started

### Instalasi

1.  `$ git clone https://github.com/maulana20/django-ecommerce-demo`
2.  `$ python -m venv env`
3.  `$ source env/bin/active` untuk `linux` `$ env\Scripts\activate` untuk `windows`
4.  `$ pip install --upgrade pip setuptools`
5.  `$ pip install -r requirements.txt`
6.  `$ python manage.py migrate`
7.  `$ python manage.py loaddata seed/001_account.json`
8.  `$ python manage.py loaddata seed/002_store.json`
9.  `$ python manage.py loaddata seed/003_chat.json`
10.  `$ python manage.py runserver`

#### admin :
`http://localhost:8000/admin`
- email : admin@example.com
- password : 12345

#### shop :
`http://localhost:8000/account/login`
- email : maulana@example.com
- password : 12345

#### user :
`http://localhost:8000/account/login`
- email : saputra@example.com
- password : 12345

#### note :
- setup config : `core/settings.py`
- run `redis-server`

##### home
![home](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/home.png)

##### category
![category](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/category.png)

##### detail
![detail](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/detail.png)

##### register
![register](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/register.png)

##### login
![login](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/login.png)

##### dashboard
![dashboard](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/dashboard.png)

##### cart
![cart](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/cart.png)

##### discussion
![discussion](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/discussion.png)

##### chat shop
![chat](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/chat.png)

##### chat user
![chat-user](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/chat-user.png)

##### chat rest api
![chat-rest-api](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/chat-rest-api.png)

##### chat product
![chat-product](https://github.com/maulana20/django-ecommerce-demo/blob/main/screens/chat-product.png)

##### reference :
- [breadcrumbs](https://django-bootstrap-breadcrumbs.readthedocs.io/en/latest/)
- [formatnumber](https://stackoverflow.com/questions/346467/format-numbers-in-django-templates)
- [mathfilters](https://pypi.org/project/django-mathfilters/)
- [seeder](https://medium.com/@ardho/migration-and-seeding-in-django-3ae322952111)
- [customauth](https://kimmosaaskilahti.fi/blog/2021-04-18-django-custom-authentication/)
- [comments](https://djangocentral.com/creating-comments-system-with-django/)
- [chat](https://github.com/narrowfail/django-channels-chat)
- [history](https://django-simple-history.readthedocs.io/en/latest/quick_start.html)
