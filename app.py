from bottle import delete, get, post, request, static_file, template,put
import x
from icecream import ic

##############################
@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

##############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

@get("/")
def _():
    try:
        x.disable_cache()
        users = x.db({  "query":"FOR user IN users RETURN user"})
        return template( "index.html", users=users["result"])
    except Exception as ex:
        print(ex)
    finally:
        pass

##############################
@post("/users")
def _():
    try:

        user_first_name = x.validate_user_name(request.forms.get("user_first_name", ""))
        user_last_name = x.validate_user_name(request.forms.get("user_last_name", ""))
        user = {"first_name":user_first_name, "last_name": user_last_name}
        res = x.db({"query":"INSERT @doc IN users RETURN NEW", "bindVars":{"doc":user}})
        print(res)
        html = template("_user.html", user=res["result"][0])
        return f"""
        <template mix-target="#users" mix-top>
            {html}
        </template>
        """
    except Exception as ex:
        ic(ex)
        if "user_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """            
    finally:
        pass


##############################
@delete("/users/delete/<key>")
def _(key):
    try:
        ic(key)
        res = x.db({"query":"""
                    FOR user IN users
                    FILTER user._key == @key
                    REMOVE user IN users RETURN OLD""", 
                    "bindVars":{"key":key}})
        print(res)
        return f"""
        <template mix-target="[id='{key}']" mix-replace></template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        pass







##############################
#UPDATE USER
    
@put("/users/update/<key>")
def _(key):
    try:
        new_first_name = request.forms.get(f"{key}_first_name")

        # user = x.update_user(key, 'first_name', new_first_name)



        print(f"########################################       {new_first_name}         ######################################")
    except Exception as ex:
        print("2222222222222222222222", ex)
    finally:
        print("333333333333333333333333")















