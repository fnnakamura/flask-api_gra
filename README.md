# flask-api_gra

A Flask REST API designed to serve the Golden Raspberry Awards.


# Requirements

- Python >= 3.7
- Recommended: `pipenv`
- A JDK > 8 installed (for H2 mem database utilization)

# Run

- Install missing packages from pipfile:
    `$ pipenv install`

- Open pipenv environment:
    `$ pipenv shell`

- Run the application with required .csv file as parameter:
    `$ python3 src/app.py <movielist.csv>`

# What Do I Get?

- `localhost:5000`
    - page with the full list of movies
- `localhost:5000/add`
    - form to add new movie
- `localhost:5000/api/movies`
- `localhost:5000/api/movies/id`
    - endpoint to query movies (all or by id)
- `localhost:5000/api/producers`
    - endpoint to query producers
- `localhost:5000/api/awards` <<< **THIS IS WHAT YOU SHOULD BE LOOKING FOR :)**
    - endpoint to query awards
# To Be Done

    {
        "quality": {
            documentation: "swagger",
            validation: "form fields, unformatted csv"
        }
        "refactor layers": {
            db_connection: "isolate H2",
            data: "contract",
            domain: "business rules",
            controllers: "add remaining CRUD operations"
        }
    } 