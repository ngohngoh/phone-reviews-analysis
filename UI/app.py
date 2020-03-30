from flask import Flask, render_template

app = Flask(__name__, template_folder="template")

app.config['SECRET_KEY'] = "mysecretkey"

@app.route('/')
def main_page():
    categories = ['Battery', 'Screen', 'Memory', 'Size', 'Weight']
    return render_template('home.html', categories=categories)

@app.route('/search', method=['POST'])
def search():
    if request.method == "POST":
        category_select = request.form['category']
        print(category_select)
    # return the value from our dataframe 
    


if __name__ == '__main__':
    app.run(debug=True, port=3000)
