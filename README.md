# Demo Coupon Scraper

System to scrape coupons from stores

## Getting Started
### Clone project repository
```
$ git clone git@github.com:puma10/coupon_scraper.git
```
If you are new to this project and just cloned, please don't forget to create your own branch and pull `dev` branch because it has the latest working code in development.
```
$ git checkout -b <your_identifier>
$ git pull origin dev
```
### Launching the project on local
Copy **config.py.example** to create the main configuration file and correct the configuration according to your environment.
```
$ cp config.py.example config.py
```
create a new file named `env.py` within **src** folder and put the following content according to your environment.
```
DEFAULT_FLASK_CONFIG = 'dev'
```
Next, create a new database according to the **db_name** in `config.py` file.
Don't forget to give system environment variable.
#### Unix System
```
$ export FLASK_APP=run.py
$ export FLASK_CONFIG=dev
$ export FLASK_DEBUG=1
```
#### Windows
```
$ set FLASK_APP=run.py
$ set FLASK_CONFIG=dev
$ set FLASK_DEBUG=1
```

Now you are ready to initialize database. Please make sure that your `config.py` is correct.
```
flask db upgrade
```

Finally, launch the server.
```
flask run
```
