## StrykerBackend
[![Python package](https://github.com/DeadlyFirex/StrykerBackend/actions/workflows/python-package.yml/badge.svg)](https://github.com/DeadlyFirex/StrykerBackend/actions/workflows/python-package.yml) \
Backend for the Strykers applications, does all the processing for all the applications we run.

### Description
Application built in pure Python, acts as an REST API.\
Made with Flask and several extensions and uses JWT to authenticate

### Installation
The main file `application.py` is your target.\
You can run the app on Linux by executing
```
/usr/bin/python3 -m flask run -h 0.0.0.0 -p 8000
```
Docker support will soon be available.

### Roadmap
The roadmap can be found right [here](https://github.com/DeadlyFirex/StrykerBackend/projects/1) \
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
