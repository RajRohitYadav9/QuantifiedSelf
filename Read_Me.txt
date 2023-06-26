Modern Application Developement I (MAD I)
Final Project (Quantified Self Web Application)

By Raj Rohit Yadav


Read_Me.txt


Submission Structure:

> static
> app.py
> api.py
> models.py
> controller.py
> error.py
> Read_Me.txt
> client.sqlite3
> requirements.txt
> templates
        >	Boolean.html
        >	Dashboard.html
	>	editBoolean.html
        >	editingShadow.html
        >	editMultiple Choice.html
        >	editNumerical.html
        >	Multiple Choice.html
        >	Numerical.html
        >	Root.html
        >	Shadow.html
        >	shadowManagement.html



Database Design:

> Users
        > user_id (Integer, Primary Key, Not Null, Unique)
        > username (String, Not Null, Unique)
        > password (String, Not Null)

> ShadowManager
        > user_id (Integer, Foreign Key, not null)
        > shadow_id (Integer, unique, Primary Key)
        > shadow_name (String)
        > about (String)
        > shadow_type (String)
        > last_seen (String)
        
        
> Logs
        > user_id(Integer, Foreign Key, not null)
        > shadow_id(Integer, Foreign Key, not null)
        > log_id(Integer, Primary Key, unique, not null)
        > time(DateTime, Primary Key, not null)
        > value(String, not null)
        > note(String, not null)

API Design:
    1)	ShadowMangerAPI
            End point to read, update, delete and post ShadowManager resources.
            >	GET
                  For getting a tracker detail
            >	PUT
                  For updating tracker detail
            >	DELETE
                  For deleting tracker
            >	POST
                  For adding new tracker
    2)	LogsAPI
            End point to read, update, delete and post logs
            >	GET
                  For getting log of tracker
            >	PUT
                  For updating logs of tracker
            >	DELETE
                  For deleting logs of tracker
            >	POST
                  For adding new log to that tracker.


Python Libraries Used:

> flask
> flask_sqlalchemy
> werkzeug.exceptions
> Flask-RESTful
> Matplotlib




Description & Features:

> First page is for user login authentication.
> On giving the correct username and password, the user will be redirected to his Dashboard.
> On his Dashboard user can create a new tracker for him and also log new event for the same tracker.
> On the tracker page users can see and analyze their tracker logs through trend lines.
> All created trackers will be reflected on Dashboard.
> Users can edit/delete any tracker or there logs with time as per needs.
