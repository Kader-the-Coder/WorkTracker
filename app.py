import os
import sys
from db import init_db
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if app.secret_key is None:
    raise RuntimeError(
        "SECRET_KEY not set in environment! "
        "Please add the following to your environment:\n"
        "$env:SECRET_KEY = \"your-very-secret-random-string\""
    )

if __name__ == "__main__":
    from auth import auth_bp
    from tracker import tracker_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tracker_bp)

    db_exists = os.path.exists("instance\\database.db")
    args = sys.argv[1:]

    if "reset" in args:
        if db_exists:
            os.remove("database.db")
        init_db()
        db_exists = True

    if not db_exists:
        init_db()

    if "local" in args:
        app.run(host="localhost", port=5000, debug=True)
    else:
        app.run()
