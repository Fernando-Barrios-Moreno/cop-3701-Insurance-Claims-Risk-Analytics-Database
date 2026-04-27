Step 1: Use the “create_db.sql” to create the database.
Step 2: Run preprocess.py to convert raw data into specific data for each table.
Step 3: Use the dataload.py to populate the database with real/toy data.
        Make sure to change lines 8 - 10 to your username and password of your online sql.
Step 4: Change lines 6 to 8 in app.py similar to step 3 and add your database credentials.
Step 5: Run the app.py using the command below
        python3 app.py