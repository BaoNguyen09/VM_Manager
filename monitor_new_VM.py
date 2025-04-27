import sys
from pydo import Client
import time
import MySQLdb
import config

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
        print(str(e))
        raise

def main():
    try:
        if len(sys.argv) != 3:
            raise ValueError("There must only be 3 arguments: script name, droplet id and primary key")
        instance_id = sys.argv[1]
        primary_key = sys.argv[2]
        if instance_id == "" or primary_key == "":
            raise ValueError("The two arguments can't be empty")
        if not instance_id.isnumeric() or not primary_key.isnumeric():
            raise ValueError("The two arguments must be numeric")
        
        # Loop to periodically check status
        vm_ready = False
        client = Client(token=config.DO_API_TOKEN)
        limit = 20
        public_ip = None
        while not vm_ready and limit > 0:
            # Connect to Digital Ocean API to track new VM creation
            resp = client.droplets.get(droplet_id=int(instance_id))
            limit -= 1
            if "droplet" not in resp: # error status
                # report error, sleep for 5 seconds and retry
                print(resp["message"])
                time.sleep(5)
                continue

            status = resp["droplet"]["status"]
            print("VM status: " + status)
            if status != "active":
                # sleep for 5 seconds and retry
                time.sleep(5)
                continue

            if status == "active":
                vm_ready = True
                for net in resp["droplet"]["networks"]["v4"]:
                    if net["type"] == "public":
                        public_ip = net["ip_address"]
                        break
        
        # connect and update the database
        db = get_db_connection()
        cursor = db.cursor()
        # Insert into servers table
        cursor.execute("UPDATE servers \
                       SET ready = %s, public_ip = %s \
                       WHERE id = %s;", 
                       (1, public_ip, int(primary_key)))
        db.commit()
        cursor.close()
        db.close()

    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(str(e))

main()