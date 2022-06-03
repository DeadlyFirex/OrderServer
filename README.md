## OrderServer
[![Python package](https://github.com/DeadlyFirex/OrderServer/actions/workflows/pylint.yml/badge.svg)](https://github.com/DeadlyFirex/OrderServer/actions/workflows/pylint.yml) [![wakatime](https://wakatime.com/badge/user/a56c956d-565b-4ddd-a43e-fb7d155c4232/project/49805ccd-7c26-4262-b361-5b05415d3c0a.svg)](https://wakatime.com/badge/user/a56c956d-565b-4ddd-a43e-fb7d155c4232/project/49805ccd-7c26-4262-b361-5b05415d3c0a)\
Backend for the order applications, does all the processing for all the applications ran.

### Description
Application built in pure Python, acts as an REST API.\
Made with Flask and several extensions and uses JWT to authenticate

### Installation
Looking in the flaskr folder, the init file is the file to run.\
It is however recommended to run the application through flask itself.\
You can run the app on Linux by executing
```
/usr/bin/python3 -m flask run -h 0.0.0.0 -p 8000
```
Docker support will soon be available.

### Roadmap
The roadmap can be found right [here](https://github.com/DeadlyFirex/OrderServer/projects/1) \
Vision for the project is quite simple.

### Configuration
Configuration is accessible [here](config-sample.json), rename the file to `config.json` on finish.\
Extended explanation will be provided soon.

### URL mapping
Will be provided soon.

### Database
Currently, the application only supports local SQLite3 databases.\
Extended support for different database structures will be added later.

### Libraries
- [Flask](https://github.com/pallets/flask)
- [flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended)
- [flask-sqlalchemy](https://github.com/pallets/flask-sqlalchemy)
- [Flask-Limiter](https://github.com/alisaifee/flask-limiter)
- [python_json_config](https://github.com/janehmueller/python-json-config)
- [uuid](https://github.com/python/cpython/blob/main/Lib/uuid.py)
- [datetime](https://github.com/python/cpython/blob/main/Lib/datetime.py)
- [random](https://github.com/python/cpython/blob/main/Lib/random.py)
