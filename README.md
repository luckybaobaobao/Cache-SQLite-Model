
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
