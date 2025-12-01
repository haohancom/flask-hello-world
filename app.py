from flask import Flask, request

app = Flask(__name__)

@app.route('/demo/echo', methods=['GET', 'POST'])
def echo():
    if request.method == 'POST':
        data = request.get_json()
        return data
    elif request.method == 'GET':
        data = request.args
        return data

def main():
    app.run(port=8080)

if __name__ == '__main__':
    main()
