
# Stage 2

### Task: 
Create a Backend Application with O-Auth Integration with Session Management

Here flask is used as the web framework and mySQL used for the database. 







### Installation requirements to run this project:
```bash
pip install flask
```
```bash
pip install pymysql
```
```bash
pip install config
```
```bash
pip install authlib
```
```bash
pip install requests
```

### Modules used
To run this project, the following modules need to be added

```bash
from flask import Flask, render_template, jsonify, request, redirect, url_for
import pymysql
import config
from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
```

Note: MySQL Server(workbench) should be installed on the PC. Dump the “stage2.sql” in the same directory.

### Steps to Launch the website:
- Move all the files in one folder. Open folder as code in VS Code.
- Install required libraries (mentioned above)
- Insert the mySQL credentials(root,host,password,database) in config.py file
- Run the “app.py” file using command:
```bash
python app.py
```
- Click on the URL
    
