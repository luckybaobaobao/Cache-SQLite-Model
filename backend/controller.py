import repository
import os
from models import Category, JokeCategoryRelation


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


