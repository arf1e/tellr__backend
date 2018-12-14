from tellr import app

if __name__ == "__main__":
    from tellr.db import db

    db.init_app(app)
    app.run(host="0.0.0.0", port=1337, debug=True)
    # 0.0.0.0 makes the app accessible from the local network
