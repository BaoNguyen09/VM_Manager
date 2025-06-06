import os
import config
import json
import MySQLdb
from http.cookies import SimpleCookie

def print_json_200(data: any):
    # respond with json data
    print("Status: 200 OK")
    print("Content-Type: application/json\n")
    print(json.dumps(data))

def print_redirect_300(location: str):
    print("Status: 303 See Other")
    print(f"Location: {config.ROOT_URL}/{location}")
    print()

def print_status_400(body: str):
    print("Status: 400 Bad Request")
    print("Content-Type: text/plain\n")
    print(f"Invalid Request: {body}")

def print_status_403(body: str):
    print("Status: 403 Forbidden")
    print("Content-Type: text/plain\n")
    print(f"Forbidden: {body}")

def print_status_405(extra_path: str, allowed_method: str):
    print("Status 405: Method Not Allowed")
    print("Content-Type: text/plain\n")
    print(f"Method '{allowed_method}' isn't allowed for path: '{extra_path}'\n \
            Allowed method: POST")

def print_status_500(body: str):
    print("Status: 500 Internal Server Error")
    print("Content-Type: text/plain\n")
    print(f"Database Connection Error: {body}")

def get_db_connection():
    try:
        db = MySQLdb.connect(
            host=config.DB_HOST, 
            user=config.DB_USER, 
            passwd=config.DB_PASSWORD, 
            db=config.DB_NAME,
            port=config.DB_PORT,
            ssl={"ssl": {}}
        )
        return db
    
    except MySQLdb.Error as e:
        print_status_500(str(e))
        exit(1)

def get_authenticated_user() -> str | None:
    # Get user field from cookie
    cookie_string = os.environ.get("HTTP_COOKIE", "")
    parsed = SimpleCookie(cookie_string)
    user = parsed.get("user").value if "user" in parsed else None
    if user is None:
        return None
    
    # Query the sessions table to authenticate
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM sessions WHERE username = %s;", 
                    (user,))
    username = cursor.fetchone() # id of new row created in MySQL table
    
    db.commit()
    cursor.close()
    db.close()

    if not username:
        return None
    return user