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
    
@put("/user/update/<key>")
def _(key):
    try:
        ic(key)
        new_first_name = request.forms.get(f"{key}_first_name")
        new_last_name = request.forms.get(f"{key}_last_name")

        # print(f"########################################     {new_first_name}     ######################################")

        user = x.db({f"query":f"""FOR user IN users FILTER user._key == '159' UPDATE user WITH {{first_name: '{new_first_name}', last_name: '{new_last_name}'}} IN users RETURN NEW"""})

        result = user["result"][0]
        



        print(f"########################################     {result}     ######################################")


        return f"""
        <template mix-target="[id='{key}']" mix-replace><div
  id="{result['_key']}"
  class="user"
>
  <div>{result['_key']}</div>
  <form id="existing_user">
    <input
      name="{result['_key']}_first_name"
      value="{result['first_name']} "
      mix-blur
      mix-data="#existing_user"
      mix-put="user/update/{result['_key']}"
    />
     <input
      name="{result['_key']}_last_name"
      value="{result['last_name']}"
      mix-blur
      mix-data="#existing_user"
      mix-put="user/update/{result['_key']}"
    />
  </form>
  <button
    mix-delete="/users/delete/{result['_key']}"
    mix-default="Delete"
    mix-await="Deleting..."
  >
    Delete
  </button>
</div></template>
        """
    except Exception as ex:
        print("error  error error error error error", ex)
    finally:
        print("333333333333333333333333")















