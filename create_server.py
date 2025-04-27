import cgi
import os
import MySQLdb
import config
from pydo import Client

root_url = ""

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

def get_db_connection():
    try:
        db = MySQLdb.connect(
            host=config.DB_HOST, 
            user=config.DB_USER, 
            passwd=config.DB_PASS, 
            db=config.DB_NAME
        )
        return db
    
    except MySQLdb.Error as e:
        print_status_500(str(e))

def create_server(user: str, desc: str) -> int:
    try:
        if (user == "" and desc is None):
            raise ValueError("Fields 'user' (str) and 'desc' (str) are required")
        
        client = Client(token=config.DO_API_TOKEN)

        req = {
            "name": f"{user}-server",
            "region": "sfo3",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-22-04-x64",
            "ssh_keys": [
                config.DO_SSH_KEY_ID,
                config.DO_SSH_KEY_FINGER_PRINT
            ],
            "backups": False,
            "ipv6": True,
            "monitoring": True,
        }

        resp = client.droplets.create(body=req)
        if "droplet" not in resp: # this means status code is non-200
            print_status_500(resp["message"])
            return
        
        return resp["droplet"]["id"]

    except ValueError as e:
        print_status_400(str(e))

def add_server_to_db(user: str, desc: str, instance_id: int, ready: bool):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Insert into servers table
        cursor.execute("INSERT INTO servers (owner, description, instance_id, ready) VALUES (%s, %s, %s, %s);", 
                       (user, desc, instance_id, ready))
        new_server_id = cursor.lastrowid # id of new row created in MySQL table
        db.commit()
        cursor.close()
        db.close()

        # run background script
        os.system(f"python3 /monitor_new_VM.py {instance_id} {new_server_id} 1>/dev/null 2>/dev/null &")

        print("Status: 303 See Other")
        print(f"Location: {root_url}/api/servers/{new_server_id}")
        print()

    except Exception as e:
        print_status_500(str(e))

def main():
    # extract basic request info
    request_method = os.environ["REQUEST_METHOD"]
    extra_path = os.environ.get("PATH_INFO", "").lstrip("/")
    path_component = extra_path.split("/")
    if request_method == "POST" or request_method == "GET": # read query parameter case of GET/POST method
        form = cgi.FieldStorage()
        user = form.getvalue("user", "")
        desc = form.getvalue("desc", None)
        droplet_id = create_server(user, desc)

        if droplet_id:
            add_server_to_db(user, desc, droplet_id, False)
    else:
        print_status_405(extra_path, request_method)
    
if __name__ == "__main__":
    main()


