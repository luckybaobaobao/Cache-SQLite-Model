## Setup:
1. Git clone the project
2. Cd into main project folder
3. Run docker compose up -d (Or you could open backend folder, Run - python main.py)


## Database:

- I choose **SQLite** as the database, which is lightweight relational database and it is a popular choice for 
small-scale applications and offers simplicity and ease of use.
- I choose SQLAlchemy to interact with the SQLite database and provide the Object-Relational Mapping (ORM) service. 
**SQLAlchemy** is a powerful SQL toolkit and ORM library that supports various database systems, including SQLite. 
- It provides a convenient and intuitive way to interact with the database using Python code.
By utilizing SQLite as the database and SQLAlchemy as the SQL toolkit and ORM, you can effectively manage and manipulate your data within your application.


## Tables:

There are **four tables** in total:
- 1. **Joke table**: This table saves all jokes, and I will not save the categories field in this joke table.
- 2. **Category table**: This table saves all categories. When a user sends a POST request, we will check if the category exists. 
If not, we will create a new category and save it.
- 3. **JokeCategoryRelation table**: This table saves the one-to-one relationship between jokes and categories. 
Jokes and categories have a many-to-many relationship, so it is easier to save them in the relation table. 
If there are more category types, it will be easier to scale.
- 4. **DeleteRemoteTable**: If we find the joke locally, we will directly delete it; otherwise, we will save the joke ID in this table. 
When a user visits with this ID next time, we will not check if this ID is in the DeleteRemoteTable or not.


## Cache:

To improve performance, I have implemented caching.
- 1. Local Joke IDs Cache: This cache stores all local joke IDs. When a user visits with an ID, 
it allows for easy and efficient checking of whether the ID exists in our local database. 
If the ID is not found in the database, there is no need to query the database further.
- 2. Deleted IDs Cache: Similar to the previous cache, this cache stores deleted IDs. 
It eliminates the need to query the database to verify if a particular ID has been deleted or not. 
By checking the deleted IDs cache, we can quickly determine whether an ID has been deleted without accessing the database.
Implementing these caching mechanisms helps optimize performance by reducing the number of unnecessary database queries and improving response times.


## How my tiny app works:

When you run main.py, it will start the server. It will setup up the database, it the database dose not exist.
And it will create all the table, if tables are not exist (db.py).
In main.py there are several apis. When you call the apis, the controller (controller.py) will controller how to handle
this request, like send remote reqeust (query remote), check cache, access to local database and so on.
If controller decide to access the database, will call repository, repository will have all function how to visit 
the database.


## Here's an overview of how my tiny app works:
1. Running main.py: When you execute main.py, it starts the server. If the database doesn't exist, it sets it up. 
Additionally, it creates any required tables if they don't already exist (implemented in db.py).
2. APIs and Controller: main.py contains several APIs.
When you call these APIs, the controller (controller.py) determines how to handle the request. 
It may involve sending remote requests, checking the cache, or accessing the local database.
3. Accessing the Database: If the controller decides to access the database, it calls the repository. 
The repository contains functions that define how to interact with the database. 
These functions handle tasks such as querying data, updating records, or performing other database operations.
By following this architecture, your app separates concerns, allowing the controller to handle the request logic 
while the repository handles the database operations. This structure promotes modularity and maintainability, making it easier to manage and extend your application in the future.



## Test part:

This is I test it from postman.

1. Post - http://127.0.0.1:8000/api/jokes/ - {
    "value": "tofu go to run",
    "categories": ["animal", "sunshine"]
}

Response:
{
    "categories": [
        "animal",
        "sunshine"
    ],
    "created_at": "2023-05-29 12:56:24.161196",
    "icon_url": "",
    "id": "6bc2bb5b-765f-4ed0-8735-df967e067d96",
    "updated_at": null,
    "url": "",
    "value": "tofu go to run"
}

2. Get - http://127.0.0.1:8000/api/joke/6bc2bb5b-765f-4ed0-8735-df967e067d96
Response:
{
    "categories": [
        "animal",
        "sunshine"
    ],
    "created_at": "2023-05-29 12:56:24.161196",
    "icon_url": "",
    "id": "6bc2bb5b-765f-4ed0-8735-df967e067d96",
    "updated_at": null,
    "url": "",
    "value": "tofu go to run"
}

3. Put - http://127.0.0.1:8000/api/joke/6bc2bb5b-765f-4ed0-8735-df967e067d96 
{
    "value": "tofu is my baby",
    "categories": ["animal", "girl", "baby"]
}

Response:
{
    "categories": [
        "animal",
        "girl",
        "baby"
    ],
    "created_at": "2023-05-29 12:56:24.161196",
    "icon_url": "",
    "id": "6bc2bb5b-765f-4ed0-8735-df967e067d96",
    "updated_at": "2023-05-29 12:56:24.161326",
    "url": "",
    "value": "tofu is my baby"
}

4. Delete (remote jokes)

This is remote joke: https://api.chucknorris.io/jokes/AOHw7jMuQoyhHmO0VowSgg
   Step - 1: send request - Get - http://127.0.0.1:8000/api/joke/AOHw7jMuQoyhHmO0VowSgg
             response: {
                    "categories": [],
                    "created_at": "2020-01-05 13:42:22.089095",
                    "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
                    "id": "AOHw7jMuQoyhHmO0VowSgg",
                    "updated_at": "2020-01-05 13:42:22.089095",
                    "url": "https://api.chucknorris.io/jokes/AOHw7jMuQoyhHmO0VowSgg",
                    "value": "When Chuck Norris has an erection lasting more than 4 hours he doesn't call your doctor, he calls your mother."
             }
   step - 2: send request - Delete - http://127.0.0.1:8000/api/joke/AOHw7jMuQoyhHmO0VowSgg
             response: success delete
   step - 3: send request - Get - http://127.0.0.1:8000/api/joke/AOHw7jMuQoyhHmO0VowSgg
             response: 404 Not Found - This joke has already be deleted by user


4. Delete (local jokes)
   step - 1: send request - Delete - http://127.0.0.1:8000/api/joke/6bc2bb5b-765f-4ed0-8735-df967e067d96
             response: success delete
   step - 2. send request - Get - http://127.0.0.1:8000/api/joke/6bc2bb5b-765f-4ed0-8735-df967e067d96
             response: 404 Deleted

5. Query 
   send request - Get - http://127.0.0.1:8000/jokes/?query=tofu
   (will request both local and remote, can combine the result together)
   response: {
    "result": [
        {
            "categories": [],
            "created_at": "2020-01-05 13:42:23.484083",
            "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
            "id": "vbFAZXvoQC6ayyLSNZSzpA",
            "updated_at": "2020-01-05 13:42:23.484083",
            "url": "https://api.chucknorris.io/jokes/vbFAZXvoQC6ayyLSNZSzpA",
            "value": "Chuck Norris was at a restaurant when the waitress asked if he would like to try their Tofu. Chuck said \"lady, I'd rather piss upwind in a hurricane\"."
        },
        {
            "categories": [],
            "created_at": "2020-01-05 13:42:28.420821",
            "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
            "id": "uvUi4Df3TzGLFjjiqcPQxw",
            "updated_at": "2020-01-05 13:42:28.420821",
            "url": "https://api.chucknorris.io/jokes/uvUi4Df3TzGLFjjiqcPQxw",
            "value": "Chuck Norris had a Doctor that suggested he needed to eat tofu instead of red meat. Chuck immediately suggested the Doctor needed to have the teeth slapped out of his mouth."
        },
        ....
        {
            "categories": [
                "animal",
                "sunshine"
            ],
            "created_at": "2023-05-29 12:28:01.134879",
            "icon_url": "",
            "id": "d53a83e0-a0ac-4ea0-bc1d-839841f5f42b",
            "updated_at": null,
            "url": "",
            "value": "tofu go to run"
        }
    ],
    "total": 22
}



