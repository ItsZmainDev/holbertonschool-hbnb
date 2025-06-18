# HBnB UML

## Introduction

The HBnB project is a web-based application inspired by platforms like Airbnb, enabling users to register, create listings for places, submit reviews, and search for available accommodations. This technical documentation compiles the architectural and design diagrams developed in the initial planning phases, providing a comprehensive blueprint to guide the development of the HBnB system.

## HBnB Evolution - Technical Documentation

## 1. Overview

This document provides a technical overview of the HBnB Evolution project. It includes UML diagrams and explanations covering the architecture, class structures, and the main user flows of the application.

The application is built in layers:

* **Presentation Layer**: Handles HTTP requests (e.g., Flask REST API).
* **Business Logic Layer**: Core logic, user authentication, data validation.
* **Persistence Layer**: Interacts with the database (CRUD operations).

## 2. UML Diagrams

### 2.1 Layered Architecture (Package Diagram)

```mermaid
classDiagram
    class PresentationLayer {
        <<interface>>
        +UserAPI
        +PlaceAPI
        +ReviewAPI
        +AmenityAPI
    }

    class BusinessLogicLayer {
        +UserService
        +PlaceService
        +ReviewService
        +AmenityService
        +User
        +Place
        +Review
        +Amenity
    }

    class PersistenceLayer {
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
        +DatabaseConnector
    }

    PresentationLayer --> BusinessLogicLayer : uses (via facade)
    BusinessLogicLayer --> PersistenceLayer : accesses (repositories)
```

### 2.2 Class Diagram

```mermaid
classDiagram
    class BaseModel {
        +UUID id
        +DateTime created_at
        +DateTime updated_at
        +save()
        +to_dict()
    }

    class User {
        +String first_name
        +String last_name
        +String phone_number
        +String profile_picture
        +String address
        +String email
        +String password
        +Boolean is_admin 'False'
        +Boolean is_owner 'False'
        +List<Place> places
        +List<Review> reviews
        +create_place(place: Place): Place
        +write_review(review: Review): Review
    }

    class Place {
        +String type
        +String description
        +Float longitude
        +Float latitude
        +Float price_per_night
        +Integer max_guests
        +Boolean is_available
        +User owner
        +List<Amenity> amenities
        +List<Review> reviews
        +add_amenity(amenity: Amenity): void
        +remove_amenity(amenity: Amenity): void
        +get_reviews(): List<Review>
    }

    class Amenity {
        +String name
        +String description
        +Place place
    }

    class Review {
        +String text
        +Interger rating
        +User user
        +Place place
        +edit_text(new_text: String, new_rating: Integer): void
        +delete(): void
    }

    %% Inheritance
    BaseModel <|-- User : inherits
    BaseModel <|-- Place : inherits
    BaseModel <|-- Amenity : inherits
    BaseModel <|-- Review : inherits

    %% Relationships
    User "1" --> "0..*" Place : owns
    Place "0..*" o-- "0..*" Amenity : has
    Place "1" --> "0..*" Review : receives
    User "1" --> "0..*" Review : writes
    Review --> Place: reviews
```

## 3. API Interaction Flow

### Sequence Diagrams Overview

This section provides sequence diagrams for five core user flows through the HBnB API. These illustrate how client requests are handled by the API layer, passed through the business logic layer, and interact with the persistence layer.

### 1. User Registration and Login

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Send request (POST /register)
    API->>BusinessLogic: Validate request
    BusinessLogic->>Database: Check if user exists
    alt User not found
        Database-->>BusinessLogic: User not found
        BusinessLogic->>Database: Create new user
        Database-->>BusinessLogic: User created
        BusinessLogic-->>API: User created successfully
        API-->>User: Respond with success message
    else User already exists
        Database-->>BusinessLogic: User already exists
        BusinessLogic-->>API: Registration failed
        API-->>User: Respond with error message (user already exists)
    end

    User->>API: Send request (POST /login)
    API->>BusinessLogic: Validate login credentials
    BusinessLogic->>Database: Check user credentials
    alt Valid credentials
        Database-->>BusinessLogic: Valid credentials
        BusinessLogic-->>API: Login successful
        API-->>User: Respond with success message and jwt token
    else Invalid credentials
        Database-->>BusinessLogic: Invalid credentials
        BusinessLogic-->>API: Login failed
        API-->>User: Respond with error message (invalid credentials)
    end
```

### 2. Place Creation

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Send request (POST /create_place)
    API->>BusinessLogic: Check user is authenticated (jwt token) and validate request data
    BusinessLogic->>Database: Create new place
    alt Place created successfully
        Database-->>BusinessLogic: Place created
        BusinessLogic-->>API: Place created successfully
        API-->>User: Respond with success message
    else Place creation failed
        Database-->>BusinessLogic: Place creation failed
        BusinessLogic-->>API: Place creation failed
        API-->>User: Respond with error message (creation failed)
    end
```

### 3. Review Submission

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Send request (POST /create_review)
    API->>BusinessLogic: Verify authentication (jwt) and validate request data
    alt Valid data and authenticated user
        BusinessLogic->>Database: Check if place exists
        alt Place exists
            Database-->>BusinessLogic: Place found
            BusinessLogic->>Database: Create a new review for the place
            alt Creation successful
                Database-->>BusinessLogic: Review created
                BusinessLogic-->>API: Review creation successful
                API-->>User: Respond with success message
            else Creation failed
                Database-->>BusinessLogic: Review creation failed
                BusinessLogic-->>API: Review creation failed
                API-->>User: Respond with error message (creation failed)
            end
        else Place does not exist
            Database-->>BusinessLogic: Place not found
            BusinessLogic-->>API: Review creation failed (place not found)
            API-->>User: Respond with error message (place not found)
        end
    else Invalid data or unauthenticated user
        BusinessLogic-->>API: Review creation failed (invalid data or unauthenticated)
        API-->>User: Respond with error message (invalid data or unauthenticated)
    end
```

### 4. Place Search by Criteria

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Send request (GET /places?criteria)
    API->>BusinessLogic: Validate criteria and user authentication (if required)
    BusinessLogic->>Database: Query places with criteria
    alt Places found
        Database-->>BusinessLogic: List of places
        BusinessLogic-->>API: Places fetched successfully
        API-->>User: Respond with list of places
    else No places found
        Database-->>BusinessLogic: No places found
        BusinessLogic-->>API: No places found
        API-->>User: Respond with empty list or not found message
    end
```

### Explanation

These diagrams highlight how the application logic is separated into layers:

* **API Layer** validates the request and delegates to the business logic.
* **Business Logic Layer** checks business rules, user permissions, and request validity.
* **Persistence Layer** performs database operations and returns results.

JWT authentication and request validation are integrated at multiple levels to ensure security and robustness of operations.


## Conclusion

This technical documentation presents a thorough blueprint of the HBnB project’s structure and behavior. From a layered architectural perspective to detailed class responsibilities and dynamic API interactions, the documentation captures how the system is built for scalability, modularity, and maintainability. These diagrams and descriptions will serve as a continuous reference throughout the software development lifecycle, promoting consistency and clarity in implementation and future extension.


