import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


def get_db_inf_from_yaml(filepath="config/db_access_inf.yml") -> dict:
    with open(filepath, "r", encoding="utf-8") as file:
        db_config = yaml.safe_load(file)
    return db_config


def get_db_engine(db_url: str):
    engine = create_engine(db_url)
    return engine


def get_session_factory(db_url: str):
    session_factory = sessionmaker(
        autocommit=False, autoflush=True, bind=get_db_engine(db_url)
    )
    return session_factory


def get_db_connection(db_url):
    try:
        connection = sqlite3.connect(db_url)
        connection.row_factory = sqlite3.Row  # 行を辞書形式で取得可能にする
        return connection
    except sqlite3.Error as e:
        print(f"SQLite connection error: {e}")
        return None


@contextmanager
def get_db_session(db_url) -> Generator[Session, None, None]:
    db_session = get_session_factory(db_url)
    db = db_session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise ValueError("")
    finally:
        db.close()


@contextmanager
def get_db_cursor(db_url):
    """
    データベースカーソルを取得し、操作後にクローズします。
    """
    connection = get_db_connection(db_url)
    if connection is None:
        raise Exception("Failed to connect to the database.")
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()  # トランザクションをコミット
    except Exception as e:
        connection.rollback()  # エラー時はロールバック
        print(f"Database operation error: {e}")
        raise
    finally:
        cursor.close()
        connection.close()
