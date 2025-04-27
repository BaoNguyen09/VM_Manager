import cgi
import os
import MySQLdb
import requests
import config

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

def print_status_400(body: str):
    print("Status: 400 Bad Request")
    print("Content-Type: text/plain\n")
    print(f"Invalid Request: {body}")

def print_status_500(body: str):
    print("Status: 500 Internal Server Error")
    print("Content-Type: text/plain\n")
    print(f"Database Connection Error: {body}")



