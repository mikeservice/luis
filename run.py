import os
from src import app, manager

config_name = os.getenv('FLASK_CONFIG')

if __name__ == '__main__':
    manager.run()
