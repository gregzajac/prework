from myrent_app import app

@app.route('/')
def index():
    return 'Flask is running!'


if __name__ == "__main__":
    app.run()
