-- ============================================================
-- ANALIZA DANYCH NBP – Zestaw zapytań SQL
-- ============================================================
-- Zawiera:
-- 1. Podstawowy podgląd danych
-- 2. Zmiany dzień do dnia (pct_change)
-- 3. Ranking zmienności walut (volatility)
-- 4. Porównania międzywalutowe
-- 5. Korelacje
-- 6. Ranking walut po średnim kursie
-- 7. Analiza wzrostów w czasie
-- ============================================================


-- 1. Podstawowy podgląd tabeli
SELECT *
FROM nbp_rates
ORDER BY effective_date, code;


-- 2. Zmiana dzień do dnia (pct_change)
SELECT
    code,
    effective_date,
    mid,
    ROUND(
        (mid - LAG(mid) OVER (PARTITION BY code ORDER BY effective_date))
        / NULLIF(LAG(mid) OVER (PARTITION BY code ORDER BY effective_date), 0) * 100,
    6) AS pct_change
FROM nbp_rates
ORDER BY code, effective_date;


-- 3. Ranking zmienności walut
SELECT
    code,
    ROUND(STDDEV(mid), 6) AS volatility
FROM nbp_rates
GROUP BY code
ORDER BY volatility DESC;


-- 4. Porównanie dwóch walut – przykład: RON vs EUR
SELECT 
    r.effective_date,
    r.mid AS waluta_A,
    e.mid AS waluta_B,
    r.mid - e.mid AS diff
FROM nbp_rates r
JOIN nbp_rates e 
    ON r.effective_date = e.effective_date
WHERE r.code = 'RON'
  AND e.code = 'EUR'
ORDER BY r.effective_date;


-- 5. Korelacja między dwiema walutami – przykład: RON vs EUR
SELECT corr(r.mid, e.mid) AS correlation
FROM nbp_rates r
JOIN nbp_rates e 
    ON r.effective_date = e.effective_date
WHERE r.code = 'RON'
  AND e.code = 'EUR';


-- 6. Ranking walut po średnim kursie
SELECT
    code,
    ROUND(AVG(mid), 6) AS avg_mid
FROM nbp_rates
GROUP BY code
ORDER BY avg_mid DESC;


-- 7. Top wzrosty walut w okresie (proc)
WITH t AS (
    SELECT
        code,
        FIRST_VALUE(mid) OVER (PARTITION BY code ORDER BY effective_date) AS first_mid,
        LAST_VALUE(mid) OVER (
            PARTITION BY code 
            ORDER BY effective_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_mid
    FROM nbp_rates
)
SELECT DISTINCT
    code,
    ROUND((last_mid - first_mid) / first_mid * 100, 6) AS total_pct_change
FROM t
ORDER BY total_pct_change DESC;


-- 8. Heatmapa korelacji – pivot + corr
WITH pivot_data AS (
    SELECT * FROM nbp_rates
    PIVOT (MAX(mid) FOR code)
)
SELECT corr_matrix.*
FROM (
    SELECT corr(*) AS corr_matrix
    FROM pivot_data
);
