from flask import Flask, render_template, request, jsonify
import pickle

# Muat aturan asosiasi dari file pickle
with open('association_rule.pkl', 'rb') as f:
    rules = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Menyajikan halaman utama HTML

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        transaction_items = set(data.get('items', []))  # Menggunakan set untuk pencocokan

        # Jika tidak ada items yang diberikan
        if not transaction_items:
            return jsonify({'error': 'No items provided'}), 400

        recommendations = []

        # Cari aturan yang sesuai dengan item yang ada dalam transaksi
        for index, rule in rules.iterrows():
            antecedents = rule['antecedents']
            if antecedents.issubset(transaction_items):  # Cek apakah antecedents adalah subset dari transaksi
                # Konversi frozenset menjadi list
                recommendations.append(list(rule['consequents']))

        return jsonify({'recommendations': recommendations})

    except Exception as e:
        print(f"Error processing recommendation: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
