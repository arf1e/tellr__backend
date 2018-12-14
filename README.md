# Бэкэнд для курсового проекта по программированию

### Что нужно, чтобы запустить эту штуку:
1. Прописать `pipenv install`, это установит все зависимости проекта
2. Прописать `pipenv shell`, это активирует виртуальное окружение
3. В папке tellr создать файл `config.py`, где нужно прописать следующие параметры:
 * SECRET_KEY
 * SQLALCHEMY_DATABASE_URI
 * SQLALCHEMY_TRACK_MODIFICATIONS
 * PROPAGATE_EXCEPTIONS
 * JWT_BLACKLIST_ENABLED
 * JWT_BLACKLIST_TOKEN_CHECKS
4. Некоторые из вышеуказанных опциональные, это просто содержание моего файла.
5. Прописать `python tellr.py`
