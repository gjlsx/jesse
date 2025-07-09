-- PostgreSQL Basic Operations Test (English)
-- Drop existing table if exists
DROP TABLE IF EXISTS test_users;

-- Create test table
CREATE TABLE test_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    age INTEGER,
    salary DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data
INSERT INTO test_users (username, email, age, salary) VALUES
('john_doe', 'john@example.com', 28, 5000.00),
('jane_smith', 'jane@example.com', 32, 6200.00),
('bob_wilson', 'bob@example.com', 25, 4800.00),
('alice_brown', 'alice@example.com', 29, 5500.00),
('charlie_davis', 'charlie@example.com', 35, 7000.00);

-- Test basic queries
SELECT 'Basic SELECT test' AS test_description;
SELECT COUNT(*) as total_users FROM test_users;

SELECT 'Users with salary > 5000' AS test_description;
SELECT username, salary FROM test_users WHERE salary > 5000 ORDER BY salary DESC;

SELECT 'Average salary' AS test_description;
SELECT ROUND(AVG(salary), 2) as average_salary FROM test_users;

-- Test UPDATE
SELECT 'Before UPDATE' AS test_description;
SELECT username, salary FROM test_users WHERE username = 'john_doe';

UPDATE test_users SET salary = 5500.00 WHERE username = 'john_doe';

SELECT 'After UPDATE' AS test_description;
SELECT username, salary FROM test_users WHERE username = 'john_doe';

-- Test DELETE (delete and restore)
SELECT 'Before DELETE' AS test_description;
SELECT COUNT(*) as total_users FROM test_users;

DELETE FROM test_users WHERE username = 'charlie_davis';

SELECT 'After DELETE' AS test_description;
SELECT COUNT(*) as total_users FROM test_users;

-- Restore deleted record
INSERT INTO test_users (username, email, age, salary) VALUES
('charlie_davis', 'charlie@example.com', 35, 7000.00);

SELECT 'After RESTORE' AS test_description;
SELECT COUNT(*) as total_users FROM test_users;

-- Test aggregation
SELECT 'Aggregation test' AS test_description;
SELECT 
    COUNT(*) as total_users,
    AVG(age) as avg_age,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM test_users;

-- Final verification
SELECT 'Final verification - All users' AS test_description;
SELECT username, email, age, salary FROM test_users ORDER BY username;
