from flask import Flask, render_template
app = Flask(__name__)


@app.route("C:\Users\mohanrajhan\OneDrive\Desktop\IBM Projects\Assessment\Team lead\Assignment 2\sign in.html")
def sign_in():
    return render_template("sign in.html")

@app.route("C:\Users\mohanrajhan\OneDrive\Desktop\IBM Projects\Assessment\Team lead\Assignment 2\sign up.html")
def sign_up():
    return render_template("sign up.html")

@app.route("C:\Users\mohanrajhan\OneDrive\Desktop\IBM Projects\Assessment\Team lead\Assignment 2\home.html")
def home():
    return render_template("home.html")

@app.route("C:\Users\mohanrajhan\OneDrive\Desktop\IBM Projects\Assessment\Team lead\Assignment 2\about.html")
def about():
    return render_template("aboutus.html")
    
if __name__ == '__main__':
    app.run(debug=True)