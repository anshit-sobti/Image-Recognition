from flask import Flask, request, render_template
import json
import utils
import VisualSearch

app = Flask(__name__)

@app.route('/api/v1/scripts',methods=['POST'])
def post_file():
    print("inside post")
    file = request.files['data']
    location = utils.store_file(file)
    res = VisualSearch.predict(location)
    return json.dumps({"response":res})

@app.route('/api/file-upload',methods=['POST'])
def post_file_web():
    print("inside post")
    file = request.files['data']
    location = utils.store_file(file)
    res = VisualSearch.predict(location)
    results = VisualSearch.get_docs(res.get('doc_id'))
    return render_template("products.html",results=results)

@app.route('/suggestions',methods=['GET'])
def get_suggestions():
    doc_id = request.args.get('sugId')
    results = VisualSearch.get_docs(doc_id)
    return render_template("suggestions.html",results=results)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')