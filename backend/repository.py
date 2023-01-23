from db import session


def insert(item: object):
    session.add(item)
    session.commit()
