document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            if (!email || !password) {
                alert('Email and password are required');
                return;
            }
            try {
                await loginUser(email, password);
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred while logging in. Please try again.');
            }
        });
    }
    const page = window.location.pathname.split('/').pop();
    if (page === 'index.html') {
        checkAuthentication();
    }
    if (page === 'place.html') {
        checkPlaceAuthentication();
    }
    if (page === 'add_review.html') {
        handleAddReviewPage();
    }
});

async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:55697/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
        alert('Login successful!');
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-button');
    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchPlaces(token) {
    const response = await fetch("http://127.0.0.1:55697/api/v1/places", {
        method: "GET",
    });
    if (response.ok) {
        const data = await response.json();
        displayPlaces(data);
    } else {
        console.error("Failed to fetch places:", response.statusText);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById("places-list");
    const placesDiv = placesList.querySelector(".places");
    placesDiv.innerHTML = "";
    places.forEach(place => {
        const placeCard = document.createElement("div");
        placeCard.className = "place-card";
        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>Type: <strong>${place.type}</strong></p>
            <p>Price per night: <strong>$${place.price_per_night}</strong></p>
            <p>Max guests: <strong>${place.max_guests}</strong></p>
            <p>Available: <strong>${place.is_available ? "Yes" : "No"}</strong></p>
            <button class="details-button" onclick="location.href='place.html?id=${place.id}'">View details</button>
        `;
        placesDiv.appendChild(placeCard);
    });
    if (places.length === 0) {
        placesDiv.innerHTML = "<p>No places available.</p>";
    }
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function checkPlaceAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();
    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
        fetchPlaceDetails(null, placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch(`http://127.0.0.1:55697/api/v1/places/${placeId}`, {
        method: "GET",
        headers: headers
    });
    if (response.ok) {
        const data = await response.json();
        const reviews = await fetch(`http://127.0.0.1:55697/api/v1/reviews/places/${placeId}/reviews`, {
            method: "GET",
            headers: headers
        });
        if (reviews.ok) {
            const reviewsData = await reviews.json();
            data.reviews = reviewsData;
        }
        displayPlaceDetails(data);
    } else {
        console.error("Failed to fetch place details:", response.statusText);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById("place-details");
    placeDetails.innerHTML = "";
    const title = document.createElement("h2");
    const description = document.createElement("p");
    const infoDiv = document.createElement("div");
    infoDiv.className = "place-info";
    infoDiv.innerHTML = `
        <h2>${place.title}</h2>
        <h5>Description:</h5>
        <p>${place.description}</p>
        <p>Type: <strong>${place.type}</strong></p>
        <p>Price per night: <strong>$${place.price_per_night}</strong></p>
        <p>Max guests: <strong>${place.max_guests}</strong></p>
        <p>Available: <strong>${place.is_available ? "Yes" : "No"}</strong></p>
    `;
    const amenitiesDiv = document.createElement("div");
    amenitiesDiv.className = "place-amenities";
    const amenitiesTitle = document.createElement("h3");
    amenitiesTitle.textContent = "Amenities";
    amenitiesDiv.appendChild(amenitiesTitle);
    const amenitiesList = document.createElement("ul");
    if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(am => {
            const li = document.createElement("li");
            li.textContent = am;
            amenitiesList.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.textContent = "None";
        amenitiesList.appendChild(li);
    }
    amenitiesDiv.appendChild(amenitiesList);
    placeDetails.appendChild(title);
    placeDetails.appendChild(description);
    placeDetails.appendChild(infoDiv);
    placeDetails.appendChild(amenitiesDiv);
    console.log(place.reviews);
    if (place.reviews && place.reviews.length > 0) {
        const reviewsSection = document.createElement("section");
        reviewsSection.className = "place-reviews";
        const reviewsTitle = document.createElement("h3");
        reviewsTitle.textContent = "Reviews";
        reviewsSection.appendChild(reviewsTitle);
        place.reviews.forEach(review => {
            const reviewDiv = document.createElement("div");
            reviewDiv.className = "review-card";
            reviewDiv.innerHTML = `
                <p>${review.text}</p>
                <span>User: ${review.user_id}</span>
                <span>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
            `;
            reviewsSection.appendChild(reviewDiv);
        });
        placeDetails.appendChild(reviewsSection);
    }
}

function handleAddReviewPage() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    const placeId = getPlaceIdFromURL();
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;
            if (!reviewText || !rating) {
                alert('Please fill in all fields');
                return;
            }
            try {
                const response = await submitReview(token, placeId, reviewText, rating);
                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                } else {
                    const errorData = await response.json();
                    alert(errorData.message || 'Failed to submit review');
                }
            } catch (error) {
                alert('Failed to submit review');
            }
        });
    }
}

async function submitReview(token, placeId, reviewText, rating) {
    return fetch('http://127.0.0.1:55697/api/v1/reviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating),
            place_id: placeId
        })
    });
}