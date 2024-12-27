from flask import Flask, render_template, request, jsonify
import pickle

with open('model.pkl', 'rb') as f:
    rules = pickle.load(f)

app = Flask(__name__, template_folder='./')

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        transaction_items = set(data.get('items', [])) 

        if not transaction_items:
            return jsonify({'error': 'No items provided'}), 400

        all_products = set(rules['antecedents'].explode().unique()).union(
            set(rules['consequents'].explode().unique())
        )
        if transaction_items == all_products:
            return jsonify({'recommendations': []}) 

        recommendations = []

        for index, rule in rules.iterrows():
            antecedents = rule['antecedents']
            if antecedents.issubset(transaction_items):  
                recommendations.extend(rule['consequents'])  

        recommendations = sorted(set(recommendations)) 

        return jsonify({'recommendations': recommendations})

    except Exception as e:
        print(f"Error processing recommendation: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/products', methods=['GET'])
def products():
    try:
        product_set = set()
        for index, row in rules.iterrows():
            product_set.update(row['antecedents'])
            product_set.update(row['consequents'])

        product_list = sorted(product_set)

        return jsonify(product_list)  
    except Exception as e:
        print(f"Error processing products: {e}")
        return jsonify({'error': 'Unable to retrieve products'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
