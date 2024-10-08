import requests

BASE_URL = 'http://127.0.0.1:5000/api'

def test_create_equipment():
    data = {
        "name": "X-ray Machine",
        "latitude": 40.7128,
        "longitude": -54.0060,
        "address": "123 Hospital St, New York, NY 10001",
        "contact_info": "212-555-1234",
        "availability_status": True
    }
    print(f"Sending POST request to {BASE_URL}/equipment")
    response = requests.post(f"{BASE_URL}/equipment", json=data)
    print("Create Equipment Status Code:", response.status_code)
    print("Create Equipment Response Text:", response.text)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print("Failed to create equipment")
        return None

def test_get_all_equipment():
    response = requests.get(f"{BASE_URL}/equipment")
    print("Get All Equipment:", response.status_code, response.json())

def test_get_equipment(equipment_id):
    response = requests.get(f"{BASE_URL}/equipment/{equipment_id}")
    print("Get Equipment:", response.status_code, response.json())

def test_update_equipment(equipment_id):
    data = {
        "name": "Updated X-ray Machine",
        "availability_status": False
    }
    response = requests.put(f"{BASE_URL}/equipment/{equipment_id}", json=data)
    print("Update Equipment:", response.status_code, response.json())

def test_nearby_equipment():
    params = {
        "lat": 40.7128,
        "lon": -74.0060,
        "radius": 10
    }
    response = requests.get(f"{BASE_URL}/equipment/nearby", params=params)
    print("Nearby Equipment:", response.status_code, response.json())

def test_delete_equipment(equipment_id):
    response = requests.delete(f"{BASE_URL}/equipment/{equipment_id}")
    print("Delete Equipment:", response.status_code, response.text)

if __name__ == "__main__":
    print("Starting API tests...")
    equipment_id = test_create_equipment()
    if equipment_id:
        test_get_all_equipment()
        test_get_equipment(equipment_id)
        test_update_equipment(equipment_id)
        test_nearby_equipment()
        test_delete_equipment(equipment_id)
    else:
        print("Skipping remaining tests due to failure in equipment creation.")