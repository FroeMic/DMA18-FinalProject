# FullStack_Info_FinalProject
Final Project for INFO 254 at UC Berkeley in Spring 2018

## Initial Setup

After **initially cloning** the repository make sure that

1. All the dependecies in `requirements.txt` are installed. You can install them by running `pip install -r requirements.txt`.
2. You created and configured the dotenv file (`.env`). Just copy and rename the `.env.example` and fill in the blank spots.
3. You created the database. In your terminal navigate to this folder and run `python` to bring up the python interactive shell. Then run the following three commands: `import app`, then `app._create_database()` and finally `exit()`.

## Folder Structure

```
|— requirements.txt     (all the required python packages)
|— .env                 (store environment variables that should not end up on github)
|— config.py            (loads variables from .env)
|— run.py               (runs the flask server)
|— app/                     
    |— data/            (user generated data. Not pushed to github.)
    |— models/          (all SQLAlchemy models)
    |— routes.py        (the routes of the app)  
    |— static/          (static files i.e. css, js, images)
    |— templates/       (Jinja2 templates)
    |— utils/           (additional functions such as custom decorators)
    |— __init__.py      

```
