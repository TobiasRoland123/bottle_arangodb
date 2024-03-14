from bottle import request, response
import re
import requests

##############################
def disable_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)   

url = "http://docker.for.mac.host.internal:8529/_api/cursor"

##############################

def db(query):
    try:
    
        res = requests.post( url, json = query )
        print(res.json())
        return res.json()
    except Exception as ex:
        print("#"*50)
        print(ex)
    finally:
        pass


##############################
USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = "^.{2,20}$"

def validate_user_name(name):
    error = f"user_name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_name = name
    user_name = user_name.strip()
    if not re.match(USER_NAME_REGEX, user_name): raise Exception(400, error)
    return user_name




##############################
# def update_user(key, type, new_value):
#     query = f""" FOR user in users FILTER user._key == '{key}'
#         UPDATE user WITH {{ {type}: '{new_value}' }} IN users
#         RETURN NEW"""   
#     res = db({"query": {query}})
#     return res.json()