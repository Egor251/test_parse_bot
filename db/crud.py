import sqlalchemy
import db.main_db as main_db


def select_all_titles():
    with main_db.Session(autoflush=False, bind=main_db.engine) as session:
        return session.query(main_db.News.title).all()  # Возвращаем все заголовки из базы


def select_news(title: str):
    with main_db.Session(autoflush=False, bind=main_db.engine) as session:
        return session.query(main_db.News).filter(main_db.News.title == title).first()  # Возвращаем новость с указанным заголовком


def select_latest():
    with main_db.Session(autoflush=False, bind=main_db.engine) as session:
        return session.query(main_db.News).order_by(main_db.News.id.asc()).first()  # Возвращаем последнюю запись из базы с сортировкой по id


def insert(data: dict):  # Функция для обновления базы
    with main_db.Session(autoflush=False, bind=main_db.engine) as session:
        session.query(main_db.News).delete()  # На всякий случай чтобы избежать ошибки sqlalchemy.exc.IntegrityError
        session.commit()
        session.execute(sqlalchemy.insert(main_db.News), data)  # Уменьшаем колличество обращений к БД засчёт множественного импорта
        session.commit()
