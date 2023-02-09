import repository
import uuid
import os
from models import Category, JokeCategoryRelation
from models import Joke


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


