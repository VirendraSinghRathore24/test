from flask import Flask, render_template
    # , request

# from menuitem import MenuItem

app = Flask(__name__)

# FILE_NAME = "D:\\Work\\test.txt"


@app.route('/')
def hello_world():
    return render_template("login.html")


# @app.route("/search", methods=["POST"])
# def search():
#     return render_template("entry.html")
#
#
# @app.route("/register", methods=["POST"])
# def register():
#     return render_template("entry.html")
#
#
# @app.route("/getAllRestaurants", methods=["GET"])
# def getallrestaurants():
#     with open("D:\\Work\\restaurants.txt") as file:
#         rest = []
#         data = file.readlines()
#         for res in data:
#             rest.append(res.strip())
#     return render_template("restaurants.html", rest1=rest)
#
#
# @app.route("/resclick", methods=["POST"])
# def resclick():
#     restaurantname = request.form["submit_button"]
#     if restaurantname == "Dominos":
#         items = [["Creamy Tomato Pasta Pizza", 245],
#                  ["Moroccan Spice Pasta Pizza", 300],
#                  ["Double Cheese Margherita", 200],
#                  ["Farmhouse Cheese Pizza", 215],
#                  ["Mexican Green Wave Pizza", 117]]
#         return render_template("menu.html", menuitems=items)
#     else:
#         return render_template("entry.html")
#
#
# @app.route("/restaurantclick", methods=["POST"])
# def restaurantclick():
#     items = request.form.getlist("item")
#     amounts = request.form.getlist("amount")
#     quantities = request.form.getlist("quantity")
#     length = len(items)
#     menuitems = []
#     sum = 0
#     for i in range(length):
#         if len(quantities[i].strip()) > 0:
#             menuitem = MenuItem()
#             menuitem.item = items[i]
#             menuitem.amount = int(amounts[i])
#             menuitem.quantity = int(quantities[i])
#             menuitems.append(menuitem)
#             sum += int(amounts[i])
#
#     return render_template("order.html", cartdata=menuitems, sum=sum)
#
#
# @app.route("/account", methods=["POST"])
# def account():
#     username = request.form["username"]
#     password = request.form["password"]
#
#     with open(FILE_NAME, "a") as file:
#         file.write(f"\n{username}:{password}")
#     return f"user {username} registered successfully !!!"
#
#
# @app.route("/cartclick", methods=["POST"])
# def cartclick():
#     return f"<h1>Order Placed successfully!!!</h1>"
#
#
# @app.route("/login", methods=["POST"])
# def receive_data():
#     name = request.form["username"]
#     password = request.form["password"]
#     isvalid = validate_login(name, password)
#     if isvalid:
#         print(loginUser)
#         return render_template("search.html")
#     else:
#         return f"<h2>Login Failed</h2>"
#
#
# def validate_login(username, password):
#     with open(FILE_NAME) as file:
#         contents = file.readlines()
#         for c in contents:
#             details = c.split(':')
#             if details[0] == username and details[1].strip() == password:
#                 return True
#         else:
#             return False
# #
# @app.route('/insert/<name>')
# def haa(name):
#     return "abc"


if __name__ == "__main__":
    app.run(debug=True)
