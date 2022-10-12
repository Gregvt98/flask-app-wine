IO Group Project

Steps:

1. Pull latest changes from repository with git pull <remote branch>

2. Create database.db file if it doesn't already exist:
-start a python shell (enter "python" in powershell/git bash)
-run "from app import db" then "db.create_all()" (a database.db file should be created)
-finally insert new rows in the database with "python insert_data.py"

