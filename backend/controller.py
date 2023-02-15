import repository
import uuid
import os
from models import Category, JokeCategoryRelation
from models import Joke
from db import session


def insert_joke(icon_url, value, categories, cache):
    external_id = str(uuid.uuid4())
    joke = Joke(
        value=value,
        external_id=external_id,
        icon_url=icon_url,
        url=_get_base_url()
    )
    repository.insert(joke)
    cache.add_id_into_local_ids(joke.external_id, joke.id)

    _create_categories_and_relations(joke.id, categories)
    return _convert_json(joke, categories)


def _create_categories_and_relations(joke_id, categories: list[str]):
    for category_name in categories:
        category = repository.search_by_name(Category, category_name)
        if not category:
            category = Category(name=category_name)
            repository.insert(category)
        relation = JokeCategoryRelation(joke_id=joke_id, category_id=category.id)
        repository.insert(relation)


def _get_base_url():
    return os.getenv('BASE_URL')


def _convert_json(joke, categories):
    return {
        "categories": categories,
        "created_at": str(joke.created_at),
        "icon_url": joke.icon_url or "",
        "id": joke.external_id,
        "updated_at": str(joke.updated_at) if joke.updated_at else None,
        "url": joke.url or "",
        "value": joke.value
    }


def _update_joke_category_relations(joke_id, categories):
    if categories:
        repository.delete_by_joke_id(JokeCategoryRelation, joke_id)
        _create_categories_and_relations(joke_id, categories)
        return categories
    else:
        return repository.search_jokes_categories(JokeCategoryRelation, Category, joke_id)


def search_jokes_categories(relation: object, category: object, joke_id: str):
    categories = session.query(
        category
    ).join(relation).filter(
        relation.joke_id == joke_id
    ).filter(
        category.id == relation.category_id
    ).all()
    return [category.name for category in categories] if categories else []