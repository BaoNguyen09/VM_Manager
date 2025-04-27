import cgi
import os
import MySQLdb
import requests
import config
import json

def print_status_400(body: str):
    print("Status: 400 Bad Request")
    print("Content-Type: text/plain\n")
    print(f"Invalid Request: {body}")

def print_status_405(extra_path: str, allowed_method: str):
    print("Status 405: Method Not Allowed")
    print("Content-Type: text/plain\n")
    print(f"Method '{allowed_method}' isn't allowed for path: '{extra_path}'\n \
            Allowed method: POST")

def print_status_500(body: str):
    print("Status: 500 Internal Server Error")
    print("Content-Type: text/plain\n")
    print(f"Database Connection Error: {body}")

async def get_db_connection():
    try:
        db = await MySQLdb.connect(
            host=config.DB_HOST, 
            user=config.DB_USER, 
            passwd=config.DB_PASS, 
            db=config.DB_NAME
        )
        return db
    
    except MySQLdb.Error as e:
        print_status_500(e)

def create_server(user: str, desc: str):
    try:
        if (user == "" and desc is None):
            raise ValueError("Fields 'user' (str) and 'desc' (str) are required")
        
    except ValueError as e:
        print_status_400(str(e))

def main():
    # extract basic request info
    request_method = os.environ["REQUEST_METHOD"]
    extra_path = os.environ.get("PATH_INFO", "").lstrip("/")
    path_component = extra_path.split("/")
    if request_method == "POST" or request_method == "GET": # read query parameter case of GET/POST method
        form = cgi.FieldStorage()
        user = form.get("user", "")
        desc = form.get("desc", None)
        create_server(user, desc)
    else:
        print_status_405(extra_path, request_method)
    

if __name__ == "__main__":
    main()


