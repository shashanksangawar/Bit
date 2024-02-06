import requests , json , ast , random
import mysql.connector
# Configure MariaDB connection
db_config = {
    'host': '192.168.0.115',
    'user': 'ben10',
    'password': 'ben10',
    'database': 'alienx'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as error:
        return error

def close_connection(connection):
    if connection:
        connection.close()

def url_call_apache(req,app,api):
    try:
        server = "serve1"
        
        # Mod APIKey Call
        connection = connect_to_database()  
        cursor = connection.cursor()
        mod_id = (random.randint(4,10))
        query = f"SELECT APIKey FROM auth_user_apikey WHERE UserID = '{mod_id}';"
        cursor.execute(query)
        row = cursor.fetchone()
        apikey1,= row
        
        # Setting URL of icnf for pulling URL of "/inst_calc" 
        # url = "https://bharatincometax.in/icnf/conf"
        url = "http://192.168.0.112:8080/icnf/conf"
        # url = "http://localhost:5000/conf"
        
        headers = {'content-type': 'application/json'}
        
        # Calling Config Api(icnf)
        request = {"app":app,"route":api,"server":server,"apikey":f"{apikey1}"} 
        response = requests.post(f"{url}",data=json.dumps(request),headers=headers, verify=False)
        j_response = ast.literal_eval(response.text)
        n_url = j_response["url"]
        try:
            # Calling "/inst_calc"
            main_response = requests.post(f"{n_url}",data=json.dumps(req),headers=headers, verify=False)
            main_response.raise_for_status()
            main_j_response = ast.literal_eval(main_response.text)
            return main_j_response
  
        except requests.exceptions.Timeout as err:
            return err
        except requests.exceptions.TooManyRedirects as err:
            return err
        except requests.exceptions.HTTPError as err:
            return err
    except : 
        return
