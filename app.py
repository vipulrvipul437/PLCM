from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sample in-memory database of tractors
tractors_db = {
    "TRAC-001": {
        "model": "AgriMotion 50HP",
        "owner": "Ramesh Kumar",
        "status": "active",  # active, maintenance, idle
        "location": {"lat": 12.2958, "lng": 76.6394},  # Mysuru region
        "engine_hours": 420.5,
        "last_service": "2026-08-15"
    },
    "TRAC-002": {
        "model": "AgriMotion 75HP Turbo",
        "owner": "Suresh Patel",
        "status": "idle",
        "location": {"lat": 12.3050, "lng": 76.6500},
        "engine_hours": 185.0,
        "last_service": "2026-10-01"
    }
}

# 1. Get all tractors in the fleet
@app.route('/api/tractors', methods=['GET'])
def get_tractors():
    return jsonify({"status": "success", "data": tractors_db}), 200

# 2. Get details for a specific tractor
@app.route('/api/tractors/<tractor_id>', methods=['GET'])
def get_tractor(tractor_id):
    tractor = tractors_db.get(tractor_id)
    if not tractor:
        return jsonify({"status": "error", "message": "Tractor not found"}), 404
    return jsonify({"status": "success", "data": tractor}), 200

# 3. Update telemetry (engine hours & location from IoT device)
@app.route('/api/tractors/<tractor_id>/telemetry', methods=['POST'])
def update_telemetry(tractor_id):
    tractor = tractors_db.get(tractor_id)
    if not tractor:
        return jsonify({"status": "error", "message": "Tractor not found"}), 404
    
    data = request.get_json()
    
    if "lat" in data and "lng" in data:
        tractor["location"] = {"lat": data["lat"], "lng": data["lng"]}
    if "hours_added" in data:
        tractor["engine_hours"] += float(data["hours_added"])
    if "status" in data:
        tractor["status"] = data["status"]
        
    return jsonify({
        "status": "success", 
        "message": f"Telemetry updated for {tractor_id}",
        "updated_data": tractor
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
