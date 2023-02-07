from models import Joke, DeletedRemoteJoke
import repository


class Cache:
    def __init__(self):
        self.local_ids = repository.fetch_ids_pairs(Joke)
        self.deleted_remote_ids = repository.fetch_ids(DeletedRemoteJoke)

    def add_id_into_local_ids(self, external_id, id):
        self.local_ids[external_id] = id

    def remove_id_from_local_ids(self, id):
        del self.local_ids[id]

    def add_id_into_deleted_remote_ids(self, id):
        self.deleted_remote_ids.add(id)