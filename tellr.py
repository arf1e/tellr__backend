from tellr import app
    # Эта штука для меня как для жс-макаки кажется сложной,
    # Но на самом деле __name__ == '__main__' - это проверка на то, что питону был скормлен именно этот файл
    # То есть буквально что в баше было прописано 'python tellr.py'
    
if __name__ == '__main__':
    from tellr.db import db
    db.init_app(app)
    app.run(port=1337, debug=True)
