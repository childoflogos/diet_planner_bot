from typing import List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import base
import config


url = f"sqlite:///{config.database_name}.sqlite3"

engine = create_engine(url, echo=True)
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


class Base(declarative_base()):
    __abstract__ = True

    def __repr__(self):
        try:
            return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
        except AttributeError:
            return "<{0.__class__.__name__}>".format(self)

    def save(self):
        with Session() as session:
            try:
                session.add(self)
            except InvalidRequestError:
                pass
            try:
                session.commit()
            except AttributeError:
                session.commit()
            session.refresh(self)
            return self

    def delete(self):
        with Session() as session:
            session.delete(self)
            session.commit()

    @classmethod
    def get(cls: base, **kwargs):
        """
        return one or none object
        :param kwargs:
        :return:
        """
        with Session() as session:
            obj: cls = session.query(cls).filter_by(**kwargs).one_or_none()
        return obj

    @classmethod
    def get_all(cls: base, **kwargs):
        order = kwargs.pop('order', None)
        limit = kwargs.pop('limit', None)
        with Session() as session:
            objects: List[cls] = session.query(cls).filter_by(**kwargs).order_by(order).limit(limit).all()
        return objects


class Menu(Base):
    __tablename__ = 'menus',
    menu_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    breakfast_meal_id = Column(Integer, nullable=False)
    lunch_meal_id = Column(Integer, nullable=False)
    dinner_meal_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, name, breakfast_meal_id, lunch_meal_id, dinner_meal_id):
        self.name = name
        self.breakfast_meal_id = breakfast_meal_id
        self.lunch_meal_id = lunch_meal_id
        self.dinner_meal_id = dinner_meal_id


class Meal(Base):
    __tablename__ = 'meals',
    meal_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, name, ingredients, calories):
        self.name = name
        self.ingredients = ingredients
        self.calories = calories


Base.metadata.create_all(engine)
