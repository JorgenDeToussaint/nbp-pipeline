-- 1. Podstawowy podgląd tabeli
SELECT *
FROM nbp_rates
ORDER BY effective_date DESC
LIMIT 20;

-- 2. Kurs średni USD w czasie
SELECT effective_date, mid
FROM nbp_rates
WHERE code = 'USD'
ORDER BY effective_date;

-- 3. Najwyższy i najniższy kurs każdej waluty (summary)
SELECT 
    code,
    MIN(mid) AS min_mid,
    MAX(mid) AS max_mid,
    AVG(mid) AS avg_mid,
    COUNT(*) AS obs_count
FROM nbp_rates
GROUP BY code
ORDER BY avg_mid DESC;

-- 4. Dzienne widełki zmiany wartości walut (VOLATILITY VIEW)
WITH daily AS (
    SELECT 
        code,
        effective_date,
        mid,
        LAG(mid) OVER (PARTITION BY code ORDER BY effective_date) AS prev_mid
    FROM nbp_rates
)
SELECT 
    code,
    effective_date,
    ROUND(mid - prev_mid, 4) AS delta,
    ROUND((mid - prev_mid) / prev_mid * 100, 4) AS pct_change
FROM daily
WHERE prev_mid IS NOT NULL
ORDER BY effective_date DESC, code;

-- 5. Top 10 walut o największej zmienności
WITH vol AS (
    SELECT 
        code,
        STDDEV(mid) AS volatility
    FROM nbp_rates
    GROUP BY code
)
SELECT *
FROM vol
ORDER BY volatility DESC
LIMIT 10;

-- 6. Sprawdzenie braków danych
SELECT code, COUNT(*) AS cnt
FROM nbp_rates
GROUP BY code
ORDER BY cnt ASC;

-- 7. Daty z niekompletnymi danymi (walidacja pipeline)
SELECT effective_date, COUNT(*) AS rows
FROM nbp_rates
GROUP BY effective_date
HAVING rows < (SELECT MAX(x) FROM (
    SELECT COUNT(*) AS x FROM nbp_rates GROUP BY effective_date
))
ORDER BY effective_date DESC;
