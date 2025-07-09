-- PostgreSQL UTF-8 测试脚本
-- 删除已存在的表
DROP TABLE IF EXISTS employees;

-- 创建测试表
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入测试数据
INSERT INTO employees (name, email, department, salary, hire_date) VALUES
('张三', 'zhangsan@example.com', 'IT', 8000.00, '2023-01-15'),
('李四', 'lisi@example.com', 'HR', 6500.00, '2023-02-20'),
('王五', 'wangwu@example.com', 'Finance', 7200.00, '2023-03-10'),
('赵六', 'zhaoliu@example.com', 'IT', 9500.00, '2023-04-05'),
('陈七', 'chenqi@example.com', 'Marketing', 7800.00, '2023-05-12');

-- 基础查询测试
SELECT 'All Employees' AS test_name;
SELECT * FROM employees;

SELECT 'IT Department' AS test_name;
SELECT name, email, salary FROM employees WHERE department = 'IT';

SELECT 'Order by Salary' AS test_name;
SELECT name, department, salary FROM employees ORDER BY salary DESC;

SELECT 'Statistics' AS test_name;
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary
FROM employees 
GROUP BY department;

-- 更新操作测试
SELECT 'Before Update' AS test_name;
SELECT name, salary FROM employees WHERE name = '张三';

UPDATE employees SET salary = 8500.00 WHERE name = '张三';

SELECT 'After Update' AS test_name;
SELECT name, salary FROM employees WHERE name = '张三';

-- 创建索引测试
CREATE INDEX idx_department ON employees(department);
CREATE INDEX idx_email ON employees(email);

-- 查看表结构
SELECT 'Table Structure' AS test_name;
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'employees'
ORDER BY ordinal_position;

-- 最终验证
SELECT 'Final Verification' AS test_name;
SELECT COUNT(*) as total_records FROM employees;

-- 显示所有员工信息（最终测试）
SELECT 'Final Employee List' AS test_name;
SELECT id, name, department, salary, hire_date FROM employees ORDER BY id;
