import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL


server = Flask(__name__)
mysql = MySQL(server)


# config
server.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
server.config['MYSQL_USER'] = "root"
server.config['MYSQL_PASSWORD'] = ""
server.config['MYSQL_DB'] = "auth"
# server.config['MYSQL_PORT'] = int(os.environ.get("MYSQL_PORT"))
server.config['MYSQL_PORT'] = 3307

@server.route("/login",methods=['POST'])
def login():
    auth = request.authorization
    
    if not auth :
        return "Missing credentials", 401
    
    #check db for username & password
    cursor = mysql.connection.cursor()
    res = cursor.execute(
        "SELECT email, password FROM user WHERE emails=%s",(auth.username,)
    )

    if res > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password= user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"),True)
        
    else:
        return "invalid credentials", 401
        

@server.route("/validate", methods=['POST'])
def validate():
    encoded_jwt = request.header['Authorization']

    if not encoded_jwt:
        return "Missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorith= ['HS256']
        )
    except:
        return "not authorized", 403
    
    return decoded, 200

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            'username':username,
            'exp':datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat":datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm = "HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)