# Company-AI DB Operations

### Description
This repo contains a flask application which allows various operations on database.

```
1. Database setup : table-creation

2. CRUD operation : Read, Write, Delete, Update

3. Database migration : table modification
```

### Local Run Instruction

To run:
```
1. Clone the repo
2. Copy .env.sample as .env and enter the right values/credentials
3. pip install -r requirements.txt
4. flask db init
5. flask db migrate -m "Migration name"
6. flask db upgrade
7. flask run
```
### Prod Run Instruction
```
source .env
source venv/bin/activate
nohup flask run --host=0.0.0.0 --port=8765 > nohup-output.log 2>&1 &

```


### Useful Snippets


To initialize | modify db
```
flask db init (first time)
flask db migrate -m "Initial migration." (When there are changes in models)
flask db upgrade (To apply)
```

Working method for prod and dev env:
```
Create migration files in development
Push the migration files to prod once it is okay
flask db upgrade (Only run upgrade command in production, not migrate command)

Extra command:
to make new head in alembic, use: flask db stamp head
```


To run command:
```
set FLASK_ENV=development|production in .env file
flask run
```

### Linting

Packages used
```
1. pylint   : to find out errors, improvement, breach of pep8 conventions
2. black    : to autocorrect the issues
```

To use linting:
```
1. Make changes to the files
2. After the changes are complete, run check_fix_lint.sh
3. The code will do linting and highlight remaining issues
4. Keep improving the code until the linting score is more than 8.5.
5. Once the score is more than the threshold, push the code. 

```

Happy Coding !!