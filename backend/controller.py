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


