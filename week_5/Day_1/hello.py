from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index() -> str:
    """
    Route handler for the root URL ('/'). 

    This function will respond to HTTP requests made to the root URL with a 
    simple "Hello World" message.

    Returns:
        str: The HTML response to be returned to the client.
    """
    return '<h1>Hello Flask</h1>'

if __name__ == '__main__':
    """
    Start the Flask application when the script is executed directly.
    
    This will launch the Flask app on all available network interfaces (0.0.0.0)
    with debugging enabled for easier development and testing.

    Host '0.0.0.0' allows the app to be accessed externally, not just locally.
    """
    app.run(host='0.0.0.0', debug=True)
