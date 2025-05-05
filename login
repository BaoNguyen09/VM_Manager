#! /usr/bin/python3

import os
import cgi
import config

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

def main():
    # extract basic request info
    request_method = os.environ["REQUEST_METHOD"]
    extra_path = os.environ.get("PATH_INFO", "").lstrip("/")
    if request_method == "POST": # read request body
        form = cgi.FieldStorage()
        user = form.getvalue("user", "")
        
        if not user:
            print_status_400("Field 'user' is empty")
            return
        
        print(f"Set-Cookie: user={user}; Path=/; HttpOnly; SameSite=Lax")

        print("Status: 303 See Other")
        print(f"Location: {config.ROOT_URL}/index.html")
        print()
    else:
        print_status_405(extra_path, request_method)
    
if __name__ == "__main__":
    main()