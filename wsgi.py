from server import app, socket

if __name__ == "__main__":
    socket.run(app)  # This line won't be executed when running with Gunicorn