Installation
------------

1) Clone the github repository by running `git clone https://github.com/rajul-iitkgp/ginga-sunpy.git`

2) Run `python setup.py develop` inside the home folder of the above repository

3) Open your terminal and run `ginga-sunpy`

Database Parameters
-------------------

1) **Driver**: Database name such as mysql, oracle, postgresql, etc., and driver the name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc.”

2) **Database Name**: Name of the database to which to connect. (Can also specify the path to the database here)

3) **User**: Username of the user

4) **Password**: Password of the User

Optional Parameters
-------------------

1) Default Wavelength Unit
2) Set Database as default

Actions
-------

1) **Connect**: Connects to a database based on passed arguments. Defaults to sqlite:///sunpydb

2) **Add file to Database**: Adds new entries to database based on the selected file from a File Dialog Box

3) **View Database**: Opens a new tab with tabular display of database entries

4) **Open Database**: Connects to a sqlite database selected from a File Dialog Box

5) **Commit to Database**: Commits the new entries added, changes made to the database

Database Table
--------------

- Entries are displayed one-per row
- The following attributes are displayed
    - id
    - path
    - observation_time_start
    - observation_time_end
    - instrument
    - min_wavelength
    - max_wavelength
    - is_starred
- On clicking on any database entry's row, the FITS file associated to that entry opens in Ginga
- Can display only the starred entires by selecting the 'Show starred entries only' checkbox below the table 
