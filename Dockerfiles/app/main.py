# coding: utf-8

from flask import Flask, jsonify, request, app

# port number
web_port_number = 5002

# start the application
app = Flask(__name__)


# default home page & API instructions
@app.route('/')
def instruction():
    instruction = "<br>This is kubernetes jenkins CI/CD demo 4.</br>"
    return instruction


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=web_port_number, debug=True)
