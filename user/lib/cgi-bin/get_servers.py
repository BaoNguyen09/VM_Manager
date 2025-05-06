from utils import get_db_connection

def get_all_servers(user: str) -> list[dict]:
    db = get_db_connection()
    cursor = db.cursor()
    # return all instances in database
    cursor.execute("SELECT * FROM servers WHERE owner = %s;", (user,))
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    resp = []
    for row in rows:
        resp.append(
            {
            "id": row[0],
            "owner": row[1],
            "description": row[2],
            "instance_id": row[3],
            "public_ip": row[4],
            "ready": row[5]
            }
        )
    return resp

def get_server(primary_key: int, user: str) -> dict:
    db = get_db_connection()
    cursor = db.cursor()
    # return a single instance in db
    cursor.execute("SELECT * FROM servers WHERE id = %s AND owner = %s;", (primary_key, user,))
    row = cursor.fetchone()

    cursor.close()
    db.close()

    if row is None:
        return {}
    
    resp = {
            "id": row[0],
            "owner": row[1],
            "description": row[2],
            "instance_id": row[3],
            "public_ip": row[4],
            "ready": row[5]
        }
    return resp