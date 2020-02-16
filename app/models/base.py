from contextlib import contextmanager

from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import asc, desc


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def create(cls, **kwargs):
        base = cls()
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        try:
                            setattr(base, key, value)
                        except:
                            pass
            db.session.add(base)
        return base

    def modify(self, **kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(self, key):
                        try:
                            setattr(self, key, value)
                        except:
                            pass

    def delete(self):
        with db.auto_commit():
            db.session.delete(self)

    @classmethod
    def search(cls, **kwargs):
        res = cls.query
        for key, value in kwargs.items():
            if value is not None:
                if hasattr(cls, key):
                    if isinstance(value, str):
                        res = res.filter(getattr(cls, key).like(value))
                    else:
                        res = res.filter(getattr(cls, key) == value)

        if kwargs.get('order'):
            for key, value in kwargs['order'].items():
                if hasattr(cls, key):
                    if value == 'asc':
                        res = res.order_by(asc(getattr(cls, key)))
                    if value == 'desc':
                        res = res.order_by(desc(getattr(cls, key)))

        data = {
            'count': res.count(),
            'data': res.all()
        }

        return data
