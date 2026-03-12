---
title: SQL-Study-Note-13 Window Function
date: 2022-05-05 14:26:39
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "Window function is also known as Online Analytical Processing function (LAP), which is able to conduct realtime processing and analyzing on the database data."
key_concepts:
  - Window Functions
series: SQL
series_index: 13
takeaways:
  - Window functions compute values across related rows without collapsing them like GROUP BY does
  - RANK, DENSE_RANK, and ROW_NUMBER differ in how they handle ties in ordering
  - PARTITION BY defines the window scope while ORDER BY determines computation order within partitions
  - Sliding window frames (ROWS/RANGE BETWEEN) enable running totals and moving averages
---

Window function is also known as **Online Analytical Processing function (LAP)**, which is able to conduct realtime processing and analyzing on the database data. 
{% asset_img sql.jpg SQL Study Note 13 cover: Window Functions %}

<!-- more -->

# Motivation
In order to solve the following problems:
1. **Ranking**: rank each department with its own performance 
2. **TOP N**: find out the top $N$ department interms of performance

# Syntax
```SQL
SELECT *, <window function> OVER
(
PARTITION BY <col_name used for grouping>
ORDER BY <col_name used for sorting>
)
AS ranking
FROM 
table
```
# Types of window functions
The <window function> above can be replaced by two types of functions:
- **Specialized Window Functions**: RANK, DENSE_RANK, ROW_NUMBER
- **Aggregate Window Function**: SUM, AVG, COUNT, MAX, MIN

## Specialized Window Functions
Considering that we have a column A with value of $\\{3,3,3,7\\}$ and we would get the ranking in the form of ***RANK() OVER A***.
1. **RANK**: Multiple rows with the same value would occupy their following ranking place. 
**Result**: $\\{1,1,1,4\\}$
2. **DENSE_RANK**: Multiple rows with the same value woud **NOT** occupy their following ranking place. 
**Result**: $\\{1,1,1,2\\}$
3. **ROW_NUMBER**: Multiple rows with the same value woud **NOT** share the same ranking. The tie would be broken via a lexicographical order or something.
**Result**: $\\{1,2,3,4\\}$

Example of these three functions shown below:
{% asset_img 1.jpg Comparison of RANK, DENSE_RANK, and ROW_NUMBER window functions %}

## Summary
1. It should be noted that, the window function operates on the intermediate result after **WHERE / GROUP BY**. Thus, it should be written in the **SELECT** clause.
2. The **PARTITION** can be ignored (means sorting without grouping).  
3. **Difference** between **PARTITION BY** and **GROUP BY**: **GROUP BY** has the summary functionality, which would summarize multiple records in a group into **one** (**reducing** the number of rows), while **PARTITION** would keep all these records (leave the number of rows **unchanged**).
4. Specialized Window Functions realize the functionality of **sorting** and **grouping** at the same time, and **would NOT reduce** the number of rows.

# Examples:
1. Get each student's **ranking by class**:
```SQL
SELECT *, 
DENSE_RANK() over (order by 成绩 desc) as dese_rank 
from 班级表;
```
2. Solve **TOP N** question:
```SQL
SELECT * FROM
(
SELECT *, ROW_NUMBER() OVER 
(PARTITION BY col_name_to_be_part
ORDER BY col_name_to_be_sort DESC
) AS ranking
FROM table 
) AS A
WHERE ranking <= N;
```

3. Find the grades which are **above average**:
```SQL
SELECT * FROM
(
SELECT *, AVG(grade) OVER 
(PARTITION BY course_id) AS avg_grade
FROM table 
) AS A
WHERE  grade > avg_grade;
```
This is solved with a **2-step** manner. **For each row**, the corresponding average value is found. Then, **filter** those courses whose  grades are above average.
4. Find the cumulative SUM / AVG / MAX ... of each course:
```SQL
SELECT *,
SUM(grade) over w as curr_sum,
AVG(grade) over w as curr_avg,
MAX(grade)over w as curr_max,
MIN(grade) over w as curr_min
FROM score
WINDOW w AS (partition by course_id order by student_id)
```
If the aggregate functions of `AVG()
BIT_AND()
BIT_OR()
BIT_XOR()
COUNT()
JSON_ARRAYAGG()
JSON_OBJECTAGG()
MAX()
MIN()
STDDEV_POP(), STDDEV(), STD()
STDDEV_SAMP()
SUM()
VAR_POP(), VARIANCE()
VAR_SAMP()` is followed by `OVER()` clause, it would become **aggregate window function.**
However, if you want to get **cumulative** result rather than a **constant** result of the **entire group**, you must specify PARTITION and ORDER BY at the same time.

It should be noted that the **WINDOW** keyword can apply an alia to a window, so that it can be referred for multiple times.
The expected result is shown below:
{% asset_img 2.png Expected result of cumulative SUM, AVG, MAX, MIN using aggregate window functions %}

# **Sliding** Window
The range of **Sliding Window** can be specified either by **ROWS** or by **RANGE**.
## By ROWS
```SQL
SELECT *,
AVG(grade) OVER 
(ORDER BY id ROWS 2 PRECEDING ) 
-- Ways to decide the range of window by specifying rows
(ORDER BY id ROWS 2 FOLLOWING ) 
-- Two end interval:
(ORDER BY id ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) 
AS current_avg
FROM class
```
The **PRECEDING / FOLLOWING** clause is also known as **Frame** clause.

## By RANGE
Sometimes, the range cannot be represented by neighbor rows. *E.g.*, when you want to select the orders within a **time frame** of a given date (rathe than a row frame).
```SQL
SELECT *,
AVG(price) OVER 
(ORDER BY id 
INTERVAL BETWEEN 7 DAY PRECEDING AND 7 DAY FOLLOWING) 
AS current_avg
FROM orders
```
## Window Functions with constant frame
> cume_dist() / dense_rank() / lag() / lead() / ntile() / percent_rank() / rank() / row_number()

> In these cases, built-in rules would specify the frame.

# MySQL 8.0 source code analysis (on execution process)

## stage of optimization
1. **setup windows**: during the optimization process, if `select_lex->m_windows` is not NULL, then first call `Window::setup_windows`; The crucial interface would be `Window::check_window_functions(THD *thd, SELECT_LEX *select)`.

a. First judge the current window is *dynamic* or *static*. Static window (`m_static_aggregates=True`) would judge if the lower and upper bound of the window are defined.

b. If the conditon is not satisfied, i.e., `m_static_aggregates=False`. Then further decide if it is based on range (`m_range_optimizable`) or rows (`m_row_optimizable`). Then decide if a **row_buffer** is required to calculate the result (if we need **neighbor rows**, no matter whether the window is static / dynamic).

Use `Optimize-> make_tmp_tables_info` to decide if a temporary table is required as a windodw frame buffer.

c. Stack calling:  `unit->first_select()->join->exec()->evaluate_join_record()->sub_select_op() 
->QEP_tmp_table::put_record()->end_write_wf()`
{% asset_img buf1.jpg MySQL 8.0 window function execution stack call diagram %}
{% asset_img buf2.jpg MySQL 8.0 window function frame buffer processing flow %}

## Code example:
`SUM(A+FLOOR(B)) OVER (ROWS 2 FOLLOWING)`
1. First finish the function calculation (FLOOR) not related with the window frame formulation. 
2. Then the result is put into the frame buffer, and frame buffer decides if the set of rows within the frame is already calculated (done in `process_buffered_windowing_record`).
3. If the result does not satisfy the definition of window frame, then the calculation continues. Otherwise, the result is put into frame buffer and continue on processing the non-window function operators.
4. `process_buffered_windowing_record` has two strategies of moving the sliding window, `native strategy`  and `optimizable strategy`.
The prior would go through all the rows within the row buffer. However, the latter would find the **inverse** function to eliminate the out-of-frame rows' contribution made to the aggregation. Then, a **normal** aggregation function would add the contribution made by the row which just entered the frame.

