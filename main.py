import flask
from app import app


@app.route("/")
def root():
    return f"App is online ..."


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8081)
