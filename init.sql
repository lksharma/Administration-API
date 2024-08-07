-- Create tables
CREATE TABLE protection_systems (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    encryption_mode VARCHAR(50) NOT NULL
);

CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    protection_system INTEGER NOT NULL,
    FOREIGN KEY (protection_system) REFERENCES protection_systems(id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE contents (
    id SERIAL PRIMARY KEY,
    protection_system INTEGER NOT NULL,
    encryption_key VARCHAR(255) NOT NULL,
    encrypted_payload TEXT NOT NULL,
    FOREIGN KEY (protection_system) REFERENCES protection_systems(id)
);

CREATE TABLE user_devices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    device_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (device_id) REFERENCES devices(id)
);

-- Insert into protection_systems first
INSERT INTO protection_systems (id, name, encryption_mode) VALUES
(1, 'AES 1', 'AES + ECB'),
(2, 'AES 2', 'AES + CBC');

-- Then insert into devices
INSERT INTO devices (id, name, protection_system) VALUES
(1, 'Android', 1),
(2, 'Samsung', 2),
(3, 'iOS', 1),
(4, 'LG', 2);

-- Insert into users
INSERT INTO users (id, name) VALUES
(1, 'User1'),
(2, 'User2'),
(3, 'User3');

-- Insert into user_devices
INSERT INTO user_devices (user_id, device_id) VALUES
(1, 1),
(1, 3),
(2, 2),
(3, 4);
