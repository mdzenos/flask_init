## Installation

Install with pip:

```
$ pip install -r requirements.txt

```

## Flask Application Structure 
```
.
├── app
│   ├── authentication
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── __init__.py
│   ├── models
│   │   ├── users
│   │   └── __init__.py
│   ├── static
│   │   ├── css
│   │   ├── img
│   │   └── js
│   ├── template
│   │   ├── layouts
│   │   └── views
│   ├── urls.py
│   └── __init__.py
├── common
│   └── __init__.py
├── config
│   ├── database.py
│   ├── logging.py
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