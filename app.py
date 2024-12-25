from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import pickle

app = Flask(__name__)
CORS(app)  # Tambahkan ini untuk mengaktifkan CORS

with open('apriori_model.pkl', 'rb') as f:
    loaded_rules = pickle.load(f)

def cari_rekomendasi(transaksi_baru, rules):
    rekomendasi = []
    for index, rule in rules.iterrows():
        if set(transaksi_baru).issubset(rule['antecedents']):
            rekomendasi.append(list(rule['consequents']))
    return rekomendasi

@app.route('/predict', methods=['POST'])
def predict():
    try:
        transaksi_baru = request.json.get('transaksi')

        if not transaksi_baru:
            return jsonify({"error": "Transaksi tidak ditemukan dalam permintaan"}), 400
        
        rekomendasi = cari_rekomendasi(transaksi_baru, loaded_rules)

        if not rekomendasi:
            return jsonify({"message": "Tidak ada rekomendasi ditemukan untuk transaksi tersebut."}), 200
        
        return jsonify({"rekomendasi": rekomendasi}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
