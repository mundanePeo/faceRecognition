from flask import Flask
from flask_script import Manager, Server
from App import create_app

app = create_app()
manager = Manager(app=app)
manager.add_command('runserver', Server(use_debugger=False))

if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', port=10091)
    manager.run()