from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import csv

# http://127.0.0.1:5000/product?product_id=XYZ&api_key=12345

app = Flask(__name__)

old_api = "newapi"
data = pd.read_csv('normal.csv')

@app.route('/', methods=['GET'])
def index():
    return render_template('admin.html')

@app.route('/apisetup', methods=['GET', 'POST'])
def api():
    global old_api
    if request.method == 'POST':
        new_api = request.form['apiKey']
        old_api=new_api
        return render_template('apikey.html',apikey=old_api)
    
    return render_template('apikey.html',apikey = old_api)

@app.route('/log', methods=['GET'])
def log():
    date_data = pd.read_csv("date.csv")
    return render_template('logs.html', tables=[date_data.to_html(classes='data')], titles=date_data.columns.values)

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    file_df = pd.read_csv("proxy.csv")
    if request.method == 'POST':
        ip = request.form['ipRoot']
        port = request.form['port']
        user = request.form['userid']
        password = request.form['password']
        data = [[ip,port,user,password]]
        file = 'proxy.csv'
        with open(file, 'a', newline='') as file:
            dwriter = csv.writer(file)
            for row in data:
                dwriter.writerow(row)
        new_file_df = pd.read_csv("proxy.csv")
        return render_template('proxy.html', tables=[new_file_df.to_html(classes='data')], titles=new_file_df.columns.values)
    return render_template('proxy.html', tables=[file_df.to_html(classes='data')], titles=file_df.columns.values)

@app.route('/scrapped', methods=['GET'])
def scrapped():
    codecan_scrap_len = len(pd.read_csv("normal.csv"))
    theme_scrap_len = len(pd.read_csv("normal.csv"))-20
    print(theme_scrap_len)
    return render_template('total.html',no_code=codecan_scrap_len,no_theme=theme_scrap_len)


@app.route('/product', methods=['GET'])
def get_product():
    product_id = request.args.get('product_id')
    api_key = request.args.get('api_key')
    if api_key != old_api:
        return jsonify({'error': 'Invalid API Key'}), 403

    results = data.loc[data["pid"] == int(product_id)]
    if not results.empty:
        return jsonify(results.to_dict(orient='records')[0])
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)