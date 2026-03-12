---
title: "SQL Cheat Sheet"
date: 2026-03-12
type: "page"
comments: false
---

# SQL Quick Reference

A condensed reference of all 16 SQL study notes. Covers syntax, functions, optimization, and advanced features.

---

## 1. Query Basics (Note 1)

```sql
-- Filtering
SELECT DISTINCT col FROM t WHERE col IN (1,2,3);
SELECT * FROM t WHERE col BETWEEN 10 AND 20;
SELECT * FROM t WHERE col LIKE '%pattern%';       -- % = any chars
SELECT * FROM t WHERE col LIKE '_attern';          -- _ = single char
SELECT * FROM t WHERE col REGEXP '^[A-Z].*end$';
SELECT * FROM t WHERE col IS NULL;

-- Sorting & Limiting
SELECT * FROM t ORDER BY col1 DESC, col2 ASC;
SELECT * FROM t LIMIT 10 OFFSET 20;   -- pagination
```

### JOIN Types

| Join | Returns |
|------|---------|
| `INNER JOIN` | Matching rows from both tables |
| `LEFT JOIN` | All left rows + matching right (NULL if no match) |
| `RIGHT JOIN` | All right rows + matching left (NULL if no match) |
| `CROSS JOIN` | Cartesian product (every combination) |
| `SELF JOIN` | Table joined with itself (use aliases) |

```sql
-- Simplified join when column names match
SELECT * FROM a JOIN b USING (shared_col);

-- Combine result sets
SELECT col FROM t1
UNION          -- removes duplicates (slower)
SELECT col FROM t2;

SELECT col FROM t1
UNION ALL      -- keeps all rows (faster)
SELECT col FROM t2;
```

---

## 2. DML Operations (Note 2)

```sql
-- Insert
INSERT INTO t (col1, col2) VALUES (v1, v2), (v3, v4);
INSERT INTO t2 SELECT * FROM t1 WHERE condition;
SELECT LAST_INSERT_ID();   -- get auto-generated ID

-- Update
UPDATE t SET col = val WHERE id = 1;
UPDATE t SET col = val WHERE id IN (SELECT id FROM t2 WHERE ...);

-- Delete
DELETE FROM t WHERE condition;
TRUNCATE TABLE t;   -- faster, resets auto-increment, no undo
```

### Column Attributes

| Attr | Meaning |
|------|---------|
| PK | Primary Key |
| NN | NOT NULL |
| UQ | Unique |
| AI | Auto Increment |
| UN | Unsigned |
| DEFAULT | Default value |

---

## 3. Functions (Note 3)

### Aggregate Functions

| Function | Description |
|----------|-------------|
| `COUNT(*)` | Count all rows (including NULLs) |
| `COUNT(col)` | Count non-NULL values |
| `COUNT(DISTINCT col)` | Count unique non-NULL values |
| `SUM(col)` | Sum of values |
| `AVG(col)` | Average |
| `MAX(col)` / `MIN(col)` | Maximum / Minimum |

### GROUP BY & HAVING

```sql
SELECT dept, COUNT(*) AS cnt
FROM employees
WHERE salary > 50000        -- filters ROWS (before aggregation)
GROUP BY dept
HAVING COUNT(*) > 5         -- filters GROUPS (after aggregation)
ORDER BY cnt DESC;
```

`WITH ROLLUP` adds subtotal/grand total rows (MySQL-specific).

### Subqueries

```sql
-- IN / NOT IN
SELECT * FROM t WHERE col IN (SELECT col FROM t2);

-- EXISTS (short-circuits, often faster than IN)
SELECT * FROM t WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.fk = t.id);

-- ALL / ANY
SELECT * FROM t WHERE col > ALL (SELECT col FROM t2);
SELECT * FROM t WHERE col > ANY (SELECT col FROM t2);

-- Correlated subquery (runs once per outer row)
SELECT *, (SELECT MAX(val) FROM t2 WHERE t2.fk = t.id) AS max_val FROM t;
```

### String Functions

| Function | Example | Result |
|----------|---------|--------|
| `CONCAT(a, b)` | `CONCAT('Hello', ' World')` | `Hello World` |
| `LENGTH(s)` | `LENGTH('abc')` | `3` |
| `UPPER(s)` / `LOWER(s)` | `UPPER('abc')` | `ABC` |
| `TRIM(s)` | `TRIM('  abc  ')` | `abc` |
| `SUBSTRING(s, pos, len)` | `SUBSTRING('Hello', 1, 3)` | `Hel` |
| `REPLACE(s, from, to)` | `REPLACE('abc', 'b', 'x')` | `axc` |
| `LOCATE(sub, s)` | `LOCATE('lo', 'Hello')` | `4` |
| `LEFT(s, n)` / `RIGHT(s, n)` | `LEFT('Hello', 3)` | `Hel` |

### Numeric Functions

| Function | Description |
|----------|-------------|
| `ROUND(n, d)` | Round to d decimal places |
| `TRUNCATE(n, d)` | Truncate to d decimals (no rounding) |
| `CEILING(n)` / `FLOOR(n)` | Round up / down to integer |
| `ABS(n)` | Absolute value |
| `RAND()` | Random float 0-1 |

### Date/Time Functions

| Function | Returns |
|----------|---------|
| `NOW()` | Current datetime |
| `CURDATE()` / `CURTIME()` | Current date / time |
| `YEAR(d)`, `MONTH(d)`, `DAY(d)` | Extract components |
| `DATE_FORMAT(d, '%Y-%m-%d')` | Format date as string |
| `DATE_ADD(d, INTERVAL 1 DAY)` | Add interval |
| `DATEDIFF(d1, d2)` | Days between dates |

### Conditional Logic

```sql
SELECT IF(score >= 60, 'Pass', 'Fail') AS result FROM t;

SELECT CASE
  WHEN score >= 90 THEN 'A'
  WHEN score >= 80 THEN 'B'
  ELSE 'C'
END AS grade FROM t;

SELECT IFNULL(col, 'default') FROM t;      -- NULL replacement
SELECT COALESCE(c1, c2, c3, 'fallback');   -- first non-NULL
```

---

## 4. Views (Note 4)

```sql
CREATE OR REPLACE VIEW v AS SELECT col1, col2 FROM t WHERE condition;
DROP VIEW IF EXISTS v;
```

- Views store **query logic**, not data
- **Updatable** if no: DISTINCT, aggregates, GROUP BY, HAVING, UNION, subqueries
- `WITH CHECK OPTION` prevents updates that would remove rows from the view

---

## 5. Stored Procedures & Functions (Note 5)

```sql
DELIMITER $$
CREATE PROCEDURE get_orders(IN customer_id INT, OUT total DECIMAL(10,2))
BEGIN
  SELECT SUM(amount) INTO total FROM orders WHERE cid = customer_id;
END$$
DELIMITER ;

CALL get_orders(1, @result);
SELECT @result;
```

```sql
-- User-defined function (returns single value, usable in expressions)
CREATE FUNCTION calc_tax(amount DECIMAL) RETURNS DECIMAL
DETERMINISTIC READS SQL DATA
BEGIN
  RETURN amount * 0.1;
END;
```

- **Validate parameters** with `SIGNAL SQLSTATE '22003' SET MESSAGE_TEXT = 'Invalid input'`
- **User variables**: `@var` (session scope). **Local variables**: `DECLARE var TYPE` (procedure scope)

---

## 6. Triggers & Events (Note 6)

```sql
-- Trigger: auto-execute on data changes
CREATE TRIGGER trg AFTER INSERT ON orders FOR EACH ROW
BEGIN
  INSERT INTO audit_log (action, order_id, ts)
  VALUES ('INSERT', NEW.id, NOW());
END;
```

| Keyword | Access |
|---------|--------|
| `NEW.col` | Inserted/updated row values |
| `OLD.col` | Deleted/pre-update row values |

```sql
-- Scheduled event
CREATE EVENT cleanup
ON SCHEDULE EVERY 1 DAY STARTS NOW()
DO DELETE FROM logs WHERE created < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## 7. Transactions (Note 7)

```sql
START TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK;
```

### Isolation Levels

| Level | Dirty Read | Non-repeatable Read | Phantom Read | Lock Type |
|-------|-----------|---------------------|-------------|-----------|
| READ UNCOMMITTED | Yes | Yes | Yes | None |
| READ COMMITTED | No | Yes | Yes | Row-level |
| REPEATABLE READ | No | No | Yes | Row-level |
| SERIALIZABLE | No | No | No | Table-level |

```sql
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

---

## 8. Data Types (Note 8)

### String Types

| Type | Max Size | Use For |
|------|----------|---------|
| `VARCHAR(n)` | 65,535 bytes | Variable-length strings (preferred) |
| `CHAR(n)` | 255 bytes | Fixed-length (country codes, hashes) |
| `TEXT` | 64 KB | Long text |
| `MEDIUMTEXT` | 16 MB | Articles, documents |
| `LONGTEXT` | 4 GB | Very large text |

### Numeric Types

| Type | Bytes | Range |
|------|-------|-------|
| `TINYINT` | 1 | -128 to 127 (UNSIGNED: 0-255) |
| `SMALLINT` | 2 | -32K to 32K |
| `INT` | 4 | -2.1B to 2.1B |
| `BIGINT` | 8 | -9.2E18 to 9.2E18 |
| `DECIMAL(p,s)` | variable | Exact precision (use for money) |
| `FLOAT` / `DOUBLE` | 4 / 8 | Approximate (scientific data) |

### Date/Time Types

| Type | Range | Use For |
|------|-------|---------|
| `DATETIME` | 1000-9999 | General date/time storage |
| `TIMESTAMP` | 1970-2038 | Auto-updated creation/modification times |

### JSON Type

```sql
-- Create and query
SELECT JSON_EXTRACT(data, '$.name') FROM t;
SELECT data->>'$.name' FROM t;    -- returns string (not JSON)

-- Modify
UPDATE t SET data = JSON_SET(data, '$.age', 30);
UPDATE t SET data = JSON_REMOVE(data, '$.old_field');
```

---

## 9. Schema Design & Normalization (Note 9)

### Normal Forms

| Form | Rule | Violation Example |
|------|------|-------------------|
| 1NF | Atomic values, no repeating groups | `tags: "a,b,c"` in one column |
| 2NF | 1NF + no partial dependencies on composite key | Non-key depends on part of PK |
| 3NF | 2NF + no transitive dependencies | `zip -> city` stored with `customer` |

### Foreign Key Actions

| Action | ON DELETE / ON UPDATE |
|--------|----------------------|
| `RESTRICT` | Block if referenced (default, safest) |
| `CASCADE` | Delete/update referencing rows |
| `SET NULL` | Set FK to NULL (creates orphans) |

```sql
ALTER TABLE orders ADD CONSTRAINT fk_customer
  FOREIGN KEY (customer_id) REFERENCES customers(id)
  ON DELETE RESTRICT ON UPDATE CASCADE;
```

---

## 10. Indexes (Note 10)

```sql
CREATE INDEX idx_name ON t(col);                    -- single column
CREATE INDEX idx_multi ON t(col1, col2, col3);      -- composite
CREATE FULLTEXT INDEX idx_ft ON t(title, body);     -- full-text
CREATE INDEX idx_prefix ON t(col(10));              -- prefix (first 10 chars)
```

### Index Usage Rules

| Do | Don't |
|----|-------|
| Index columns in WHERE, JOIN, ORDER BY | Apply functions on indexed column: `WHERE YEAR(date) = 2024` |
| Use leftmost prefix of composite index | Skip left columns: index(a,b,c) but query only on b |
| Use covering indexes for frequent queries | Over-index: each index slows writes |
| Check selectivity with `COUNT(DISTINCT)` | Index low-cardinality columns (boolean) |

```sql
EXPLAIN SELECT * FROM t WHERE col = 'val';   -- check execution plan
SHOW INDEXES IN t;                            -- list indexes
```

### Full-Text Search

```sql
SELECT * FROM t WHERE MATCH(title, body) AGAINST('search terms');
SELECT * FROM t WHERE MATCH(title) AGAINST('+required -excluded' IN BOOLEAN MODE);
```

---

## 11. User Management (Note 11)

```sql
CREATE USER 'user'@'%.company.com' IDENTIFIED BY 'password';
GRANT SELECT, INSERT ON db.* TO 'user'@'host';
REVOKE INSERT ON db.* FROM 'user'@'host';
SHOW GRANTS FOR 'user'@'host';
DROP USER 'user'@'host';
SET PASSWORD FOR 'user'@'host' = 'new_password';
```

---

## 12. CTEs & UNION (Note 12)

```sql
-- Common Table Expression (MySQL 8.0+)
WITH cte AS (
  SELECT dept, AVG(salary) AS avg_sal FROM employees GROUP BY dept
)
SELECT * FROM cte WHERE avg_sal > 80000;

-- Recursive CTE (hierarchical data, sequences)
WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM seq WHERE n < 100
)
SELECT * FROM seq;

-- Hierarchy traversal
WITH RECURSIVE tree AS (
  SELECT id, parent_id, name, CAST(name AS CHAR(500)) AS path
  FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.parent_id, c.name, CONCAT(t.path, ' > ', c.name)
  FROM categories c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

---

## 13. Window Functions (Note 13)

### Ranking Functions

| Function | Ties Example (scores: 90,90,80) |
|----------|--------------------------------|
| `RANK()` | 1, 1, 3 (gap after tie) |
| `DENSE_RANK()` | 1, 1, 2 (no gap) |
| `ROW_NUMBER()` | 1, 2, 3 (unique, arbitrary tie-break) |

```sql
SELECT name, dept, salary,
  RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dept_rank,
  SUM(salary) OVER (PARTITION BY dept) AS dept_total,
  AVG(salary) OVER (
    ORDER BY hire_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS moving_avg_3
FROM employees;
```

### Window Frame Syntax

```
ROWS BETWEEN {UNBOUNDED PRECEDING | n PRECEDING | CURRENT ROW}
         AND {CURRENT ROW | n FOLLOWING | UNBOUNDED FOLLOWING}
```

### Useful Patterns

```sql
-- Running total
SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)

-- Moving average (3-row window)
AVG(val) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)

-- Previous/next row values
LAG(salary, 1) OVER (ORDER BY hire_date)    -- previous row
LEAD(salary, 1) OVER (ORDER BY hire_date)   -- next row

-- Percentile / distribution
NTILE(4) OVER (ORDER BY score)              -- quartile assignment
PERCENT_RANK() OVER (ORDER BY score)        -- 0.0 to 1.0
```

---

## 14-16. Query Optimization

### Optimization Priority (High to Low Impact)
1. SQL and index design
2. Table structure / schema
3. System configuration
4. Hardware

### Index Invalidation Scenarios (Index NOT Used When...)

| Scenario | Fix |
|----------|-----|
| `WHERE YEAR(date) = 2024` | Extract: `WHERE date >= '2024-01-01' AND date < '2025-01-01'` |
| `WHERE col LIKE '%pattern'` | Use `FULLTEXT` or `INSTR()` |
| `WHERE a = 1 OR b = 2` | Rewrite as `UNION` |
| `WHERE varchar_col = 123` | Match types: `WHERE varchar_col = '123'` |
| Composite index(a,b,c), query on b only | Must use leftmost prefix (a, or a+b, or a+b+c) |
| `WHERE col IS NULL` | Set default value; avoid NULL in indexed columns |
| `WHERE col != value` | Avoid index on inequality-heavy columns |

### SELECT Optimization

| Practice | Why |
|----------|-----|
| Specify columns (no `SELECT *`) | Reduces I/O, enables covering index |
| Use `WHERE` instead of `HAVING` | Filters before aggregation (less data) |
| Use `UNION ALL` instead of `UNION` | Skips duplicate removal |
| Batch INSERTs | One statement with multiple VALUES |
| Avoid `ORDER BY RAND()` | Full scan + sort; randomize in app layer |

### Deep Pagination Optimization

```sql
-- Slow (scans and discards 100000 rows):
SELECT * FROM t ORDER BY id LIMIT 10 OFFSET 100000;

-- Fast (index-only scan for IDs, then join):
SELECT t.* FROM t
JOIN (SELECT id FROM t ORDER BY id LIMIT 10 OFFSET 100000) AS sub
ON t.id = sub.id;
```

### Query Hints

```sql
SELECT * FROM t USE INDEX (idx_name) WHERE ...;
SELECT * FROM t IGNORE INDEX (idx_name) WHERE ...;
SELECT * FROM t FORCE INDEX (idx_name) WHERE ...;
```

### Other Tips

- `ORDER BY NULL` after GROUP BY to skip implicit sorting
- Prefer JOIN over subqueries (better index utilization)
- Smaller table on left side of JOIN (MySQL scans left-to-right)
- `TRUNCATE` > `DELETE` when removing all rows (faster, no undo log)
- VARCHAR > CHAR for most cases (variable length, smaller storage)
- Use numeric types over strings when possible (faster comparison)
- Place most selective WHERE conditions first
