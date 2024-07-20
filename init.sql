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

CREATE TABLE contents (
    id SERIAL PRIMARY KEY,
    protection_system INTEGER NOT NULL,
    encryption_key VARCHAR(255) NOT NULL,
    encrypted_payload TEXT NOT NULL,
    FOREIGN KEY (protection_system) REFERENCES protection_systems(id)
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
