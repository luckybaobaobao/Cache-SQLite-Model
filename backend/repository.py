from db import session


def insert(item: object):
    session.add(item)
    session.commit()

def update_by_external_id(item: object, external_id: str, values: dict):
    _item = session.query(item).filter_by(external_id=external_id)
    _item.update(values)
    session.commit()
    return _item.first()