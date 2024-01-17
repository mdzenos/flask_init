## Installation

Install with pip:

```
$ pip install -r requirements.txt

```

## Flask Application Structure 
```
.
├── app
│   ├── package
│   │   ├── models
│   │   └── views.py
│   ├── routes
│   │   ├── api
│   │   │   ├──v1
│   │   │   │   ├──__init__.py
│   │   │   │   └── urls.py
│   │   │   ├──v2
│   │   │   │   ├──__init__.py
│   │   │   │   └── urls.py
│   │   │   ├──__init__.py
│   │   │   └── urls.py
│   │   ├── web
│   │   │   ├──__init__.py
│   │   │   └── urls.py
│   │   └── __init__.py
│   ├── static
│   │   ├── css
│   │   ├── img
│   │   └── js
│   ├── template
│   │   ├── layouts
│   │   └── views
│   └── __init__.py
├── common
│   └── __init__.py
├── config
│   └── __init__.py
├── logs
│   └── __init__.py
├── migrations
│   ├── versions
│   │   └── 68263128f8a0_init_migrate.py
│   ├── alembic.ini
│   ├── env.py
│   ├── README.md
│   └── script.py.mako
├── test
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```