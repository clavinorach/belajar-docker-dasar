CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO customers (name, email) 
VALUES
('John', 'john@example.com'),
('Bagus', 'bagus@example.com'),
('Tenxi', 'tenxi@example.com')
ON CONFLICT (email) DO NOTHING;
