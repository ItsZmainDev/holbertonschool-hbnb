# TESTING REPORT

**Project:** HBnB RESTful API  
**Part:** 2 – Business Logic and API Endpoints  
**Task:** 6 – Testing and Validation  
**Date:** 2025-06-23  

---

## 🧪 Objective

This report outlines the tests performed to validate the API endpoints implemented for `User`, `Place`, `Amenity`, and `Review` entities. Each test uses `cURL` to simulate client requests and evaluates both valid and invalid cases. The results confirm whether the endpoint behaves according to the expected status codes and data formats.

---

## ✅ USER ENDPOINTS

### Test: Create a valid user

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Expected:** 201 Created  
**Result:** ✅ Passed  

---

### Test: Create a user with invalid email

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name": "", "last_name": "", "email": "invalid"}'
```

**Expected:** 400 Bad Request  
**Result:** ✅ Passed  

---

## 🏠 PLACE ENDPOINTS

### Test: Create a valid place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"type": "apartment", "title": "Lovely Spot", "description": "Close to everything", "price_per_night": 75, "latitude": 48.85, "longitude": 2.35, "max_guests": 3, "is_available": true, "owner_id": "<valid_user_id>", "amenities": []}'
```

**Expected:** 201 Created  
**Result:** ✅ Passed  

---

### Test: Create a place with missing required fields

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"title": "", "latitude": 91, "longitude": 181}'
```

**Expected:** 400 Bad Request  
**Result:** ✅ Passed  

---

### Test: Create a place with negative price

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"type": "studio", "title": "Test", "price_per_night": -50, "latitude": 45, "longitude": 2, "max_guests": 2, "is_available": true, "owner_id": "<valid_user_id>", "amenities": []}'
```

**Expected:** 400 Bad Request  
**Result:** ✅ Passed  

---

## 💡 AMENITY ENDPOINTS

### Test: Create a valid amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name": "Wi-Fi"}'
```

**Expected:** 201 Created  
**Result:** ✅ Passed  

---

### Test: Create an amenity with missing name

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{}'
```

**Expected:** 400 Bad Request  
**Result:** ✅ Passed  

---

## ✍️ REVIEW ENDPOINTS

### Test: Create a valid review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"text": "Amazing stay!", "rating": 5, "user_id": "<valid_user_id>", "place_id": "<valid_place_id>"}'
```

**Expected:** 201 Created  
**Result:** ✅ Passed  

---

### Test: Create review with invalid rating

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"text": "Bad experience", "rating": 6, "user_id": "<valid_user_id>", "place_id": "<valid_place_id>"}'
```

**Expected:** 400 Bad Request  
**Result:** ✅ Passed  

---

### Test: Create review with missing text

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"rating": 3, "user_id": "<valid_user_id>", "place_id": "<valid_place_id>"}'
```

**Expected:** 400 Bad Request  
**Result:** ✅ Passed  

---

### Test: Delete a review

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
```

**Expected:** 200 OK  
**Result:** ✅ Passed  

---

### Test: Get all reviews for a place

```bash
curl http://127.0.0.1:5000/api/v1/places/<place_id>/reviews
```

**Expected:** 200 OK, returns list of reviews  
**Result:** ✅ Passed  

---

## 🧾 Conclusion

All endpoints were tested with both valid and invalid inputs using `cURL`. Each endpoint returned the expected status code and output format. Manual tests using Swagger UI confirmed that the documentation is up-to-date and accurate.

Additionally, automated unit tests were implemented using `unittest`.

> All validations, error handling, and RESTful conventions are respected.
