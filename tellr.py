from tellr import app
    
if __name__ == '__main__':
    from tellr.db import db
    db.init_app(app)
    app.run(port=1337, debug=True)
