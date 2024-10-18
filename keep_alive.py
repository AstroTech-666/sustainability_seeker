from flask import Flask  
from threading import Thread  

app = Flask(__name__)  # Changed '' to __name__ for best practices

@app.route('/')  
def home():  
    return "I'm alive"  # Response to ensure the server is up

def run():  
    app.run(host='0.0.0.0', port=8080)  # Run the Flask app

def keep_alive():  
    t = Thread(target=run)  # Create a thread to run the Flask app
    t.start()  # Start the thread
