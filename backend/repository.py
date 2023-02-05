from db import session


def insert(item: object):
    session.add(item)
    session.commit()

def update_by_external_id(item: object, external_id: str, values: dict):
    _item = session.query(item).filter_by(external_id=external_id)
    _item.update(values)
    session.commit()
    return _item.first()

def search_by_name(item: object, value: str):
    return session.query(item).filter_by(name=value).first()

def search_by_external_id(item: object, value: str):
    return session.query(item).filter_by(external_id=value).first()


def free_search(item: object, text: str):
    return session.query(item).filter(item.value.like(text)).all()
