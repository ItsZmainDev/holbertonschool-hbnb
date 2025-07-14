-- Admin user (password hash = bcrypt("admin1234"))
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$eQFMRmh.xP93z6bN/4UcuOlnZQzKKjG2kQyUcBBAcYHmfph0nJj0S',  -- bcrypt hash of "admin1234"
    TRUE
);

-- Amenities
INSERT INTO amenities (id, name) VALUES
('11111111-aaaa-bbbb-cccc-111111111111', 'WiFi'),
('22222222-aaaa-bbbb-cccc-222222222222', 'Swimming Pool'),
('33333333-aaaa-bbbb-cccc-333333333333', 'Air Conditioning');