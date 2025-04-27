import sqlite3
import pandas as pd

#Connect to the database
conn = sqlite3.connect('data/health_data.db')
cursor = conn.cursor()

print("Connected to the database!")

#Query 1: Total records?
query = '''
SELECT COUNT(*) FROM public_health_indicators;
'''

cursor.execute(query)
total_records = cursor.fetchone()[0]
print(f"\nTotal records: {total_records}")

#Query 2: Records per country
query = '''
SELECT country_name, COUNT(*) AS records
FROM public_health_indicators
GROUP BY country_name
ORDER BY records DESC;
'''
df = pd.read_sql_query(query, conn)
print("\nRecords per country:")
print(df)

#Query 3: Life expectancy 2020
query = '''
SELECT country_name, AVG(value) AS avg_life_expectancy
FROM public_health_indicators
WHERE indicator_name LIKE '%Life expectancy%'
AND year = 2020
GROUP BY country_name
ORDER BY avg_life_expectancy DESC;
'''
df = pd.read_sql_query(query, conn)
print("\nAverage Life Expectancy in 2020:")
print(df)

#Query 4: Life Expectacy Trend Over Time
query = '''
SELECT country_name, year, value AS life_expectancy
FROM public_health_indicators
WHERE indicator_name LIKE '%Life expectancy%'
AND year BETWEEN 1960 AND 2020
ORDER BY country_name, year;
'''
df = pd.read_sql_query(query, conn)
print("\nLife Expectancy Trends (1960–2020):")
print(df)

#Query 5: Immunization trends
query = '''
SELECT country_name, year, value AS immunization_rate
FROM public_health_indicators
WHERE indicator_name LIKE '%DPT%'
AND year BETWEEN 1980 AND 2020
ORDER BY country_name, year;
'''
df = pd.read_sql_query(query, conn)
print("\nImmunization Trends (1980–2020):")
print(df)

#Query 6: Top Country in Immunization 2020
query = '''
SELECT country_name, value AS immunization_rate
FROM public_health_indicators
WHERE indicator_name LIKE '%DPT%'
AND year = 2020
ORDER BY immunization_rate DESC
LIMIT 1;
'''
cursor.execute(query)
top_country = cursor.fetchone()
print(f"\nTop country in immunization rate (2020): {top_country}")

#Query 7: Maternal mortality trends
query = '''
SELECT country_name, year, value AS maternal_mortality
FROM public_health_indicators
WHERE indicator_name LIKE '%Maternal mortality%'
AND year BETWEEN 1990 AND 2020
ORDER BY country_name, year;
'''
df = pd.read_sql_query(query, conn)
print("\nMaternal Mortality Trends (1990–2020):")
print(df)

#Query 8: Improvement in Marternal Mortality
query = '''
SELECT country_name,
       MIN(value) AS lowest_maternal_mortality,
       MAX(value) AS highest_maternal_mortality,
       (MAX(value) - MIN(value)) AS change
FROM public_health_indicators
WHERE indicator_name LIKE '%Maternal mortality%'
AND year BETWEEN 1990 AND 2020
GROUP BY country_name
ORDER BY change DESC;
'''
df = pd.read_sql_query(query, conn)
print("\nMaternal Mortality Changes 1990 - 2020 (Biggest to Smallest):")
print(df)


# Close connection
conn.close()
print("\nConnection closed!")
