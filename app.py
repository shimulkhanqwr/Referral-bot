from flask import Flask, request, jsonify
import referrals

app = Flask(__name__)

@app.route('/')
def index():
    return "Binance Tricks API Running!"

@app.route('/track', methods=['POST'])
def track_ref():
    data = request.json
    user_id = data.get('user_id')
    result = referrals.track_binance_ref(user_id)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run()
