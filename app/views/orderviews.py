from flask import render_template, request, session, \
                  abort, redirect, url_for
from app import app

@app.route("/orders")
def ordermanage():

    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    return render_template("ordertemps/ordermanage.html")
