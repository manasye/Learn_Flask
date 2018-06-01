# Learning back-end with Flask

## Module Instalation
```
pip install Flask
pip install flask-restful
pip install Flask-JWT
pip install Flask-SQLAlchemy
```

## Run Your App
```
python app.py
```

## Implementation
This project is implemented using Flask, and is a REST API for stores, items, and users

## Change Database
In Flask-Alchemy folder, SQLAlchemy could use various type of database without changing
any single code. To change database configuration, change this following code according
to your type of database
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
```
Notice that i am using sqlite in this project