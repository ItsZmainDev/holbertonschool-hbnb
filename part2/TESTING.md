# HBnB - Task 6: Testing and Validation Report

## ✅ Amenity Endpoints

### 1. Create Amenity (POST /api/v1/amenities/)

**Valid Request**:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name": "Wi-Fi"}'
