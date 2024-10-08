from geopy.distance import geodesic
from app.models import Equipment

def get_nearby_equipment(lat, lon, radius):
    all_equipment = Equipment.query.all()
    nearby = []
    for equipment in all_equipment:
        distance = geodesic((lat, lon), (equipment.latitude, equipment.longitude)).km
        if distance <= radius:
            nearby.append(equipment)
    return nearby