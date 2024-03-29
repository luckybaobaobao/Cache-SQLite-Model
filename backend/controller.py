import repository
import uuid
import os
from models import Category, JokeCategoryRelation, DeletedRemoteJoke
from models import Joke
from query_remote import query_joke_from_remote
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


def update_joke(external_id, icon_url, value, categories):
    parameters = {}
    if icon_url:
        parameters["icon_url"] = icon_url
    if value:
        parameters["value"] = value
    _joke = repository.update_by_external_id(Joke, external_id, parameters)
    _categories = _update_joke_category_relations(_joke.id, categories)
    return _convert_json(_joke, _categories)


def get_joke_from_local(external_id):
    joke = repository.search_by_external_id(Joke, external_id)
    _categories = repository.search_jokes_categories(JokeCategoryRelation, Category, joke.id)
    return _convert_json(joke, _categories)


def _query_local_jokes(query):
    _jokes = []
    jokes = repository.free_search(Joke, '%' + query + '%')
    for joke in jokes:
        categories = repository.search_jokes_categories(JokeCategoryRelation, Category, joke.id)
        _jokes.append(_convert_json(joke, categories))
    return _jokes


def _combine_results(local_jokes, remote_jokes):
    local_jokes_nums = len(local_jokes)
    remote_jokes['result'] += local_jokes
    remote_jokes['total'] += local_jokes_nums
    return remote_jokes


def query_jokes(query):
    local_jokes = _query_local_jokes(query)
    remote_jokes = query_joke_from_remote(query)
    return _combine_results(local_jokes, remote_jokes)


def _delete_joke(id):
    repository.delete_by_id(Joke, id)


def _delete_joke_category_relationship_by_joke_id(id):
    repository.delete_by_joke_id(JokeCategoryRelation, id)


def _delete_joke_from_local(id, cache):
    _id = cache.local_ids[id]
    _delete_joke(_id)
    _delete_joke_category_relationship_by_joke_id(_id)
    cache.remove_id_from_local_ids(id)


def _delete_remote_joke(id, cache):
    deleted_remote_joke = DeletedRemoteJoke(external_id=id)
    repository.insert(deleted_remote_joke)
    cache.add_id_into_deleted_remote_ids(id)


def delete_joke(id, cache):
    if id in cache.local_ids:
        _delete_joke_from_local(id, cache)
    else:
        _delete_remote_joke(id, cache)
    return True
