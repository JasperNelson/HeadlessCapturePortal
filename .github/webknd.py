from flask import Flask, request, render_template
from typing import Any

app=Flask(__name__)

@app.route("/", methods=['GET','POST'])
def captiveportal() -> Any:
    return render_template('web.html')

@app.route("/example", methods=['GET','POST'])
def examplelink() -> Any:
    return render_template('exfile-01.html')

@app.route("/submit", methods=['GET','POST'])
def submission() -> Any:
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('psword')
        terms=request.form.get('agreement')
        if username == "paul" and password == "123Sasquatch" and terms is not None:
            return render_template('sub-success.html')
        else:
            return render_template('failure.html')
    return None
    
if __name__ == "__main__": 
    app.run(debug=True) 

