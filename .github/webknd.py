from flask import Flask, request

app=Flask(__name__)

@app.route("./web.html", methods=['GET','POST'])
def captiveportal():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        terms=request.form.get('agreement')
        
