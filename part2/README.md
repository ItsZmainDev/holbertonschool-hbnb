# HBnB - Part 2: Implementation of Business Logic and API Endpoints

This repository contains the second part of the **HBnB Project**, focusing on building the core API functionalities of the application using Python and Flask. This phase brings to life the documented design from Part 1 by implementing the **Business Logic Layer** and the **Presentation Layer**, along with essential validation and testing.

---

## 🚀 Objectives

By the end of this part, the application includes:

- A modular and maintainable project structure
- Core business logic classes: `User`, `Place`, `Review`, `Amenity`
- RESTful API endpoints using Flask and `flask-restx`
- Integration of a **Facade pattern** to bridge the API and business logic
- In-memory data storage for persistence (temporary, will be replaced in Part 3)
- Full endpoint testing and validation via `cURL`, Swagger UI, and unit tests

---

## 🗂️ Project Structure

```
part2/
├── app/
│   ├── api/
│   │   └── v1/               # Presentation layer with Flask-RESTx endpoints
│   ├── models/               # Core business logic classes
│   ├── services/             # Facade logic and business coordination
│   └── persistence/          # In-memory repository layer
├── run.py                    # Flask app runner
├── TESTING.md                # Manual cURL test report
└── README.md
```

---

## 📦 Key Technologies

- **Python 3**
- **Flask** – micro web framework
- **Flask-RESTx** – for building structured REST APIs with Swagger docs
- **unittest** – Python's standard testing framework
- **cURL** – for manual black-box testing

---

## 🛠️ Implemented Features

### ✅ Business Logic
- `User` – basic user model with validation and ID generation
- `Place` – includes geolocation, price, availability, owner, and amenities
- `Amenity` – supports dynamic amenity creation and update
- `Review` – includes validation for rating (1-5), text, and associations

### ✅ API Endpoints
| Entity   | Methods Implemented     |
|----------|--------------------------|
| User     | POST, GET, PUT           |
| Place    | POST, GET, PUT           |
| Amenity  | POST, GET, PUT           |
| Review   | POST, GET, PUT, DELETE   |

> JWT authentication will be introduced in **Part 3**


## 🧪 Testing

- **Manual Testing**: via `cURL` and Swagger UI (`http://127.0.0.1:5000/api/v1/`)
- **Validation Checks**: each entity validates its data fields (e.g. email, rating)
- **Unit Tests**: located in `tests/` (if present), using `unittest`

Manual test results are documented in [TESTING.md](./TESTING.md)


## 📘 Learning Outcomes

- Design and implement clean modular Python projects
- Build and document RESTful APIs with Flask-RESTx
- Apply business logic, validation, and data integrity rules
- Use the **Facade design pattern** to structure logic access
- Test and debug APIs with professional tools and strategies


## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Docs](https://flask-restx.readthedocs.io/)
- [RESTful API Design Guide](https://restfulapi.net/)
- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
- [Facade Design Pattern](https://refactoring.guru/design-patterns/facade/python/example)


## 👨‍💻 Author

Part of the **Holberton School** Higher-Level Programming Curriculum  
Project evaluated via checkpoints, testing, and review.

- **Martin Clement** - [Github Profile](https://github.com/ItsZmainDev)
- **Florian Chereau** - [Github Profile](https://github.com/C-Florian)