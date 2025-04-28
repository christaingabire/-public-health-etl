import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


conn = sqlite3.connect('data/health_data.db')
cursor = conn.cursor()

print("Connected to the database!")

#Creating plots folder 
if not os.path.exists('plots'):
    os.makedirs('plots')

#
sns.set(style="whitegrid")

#Add queries + plots one by one

#Query 1: Total records?
query = '''
SELECT COUNT(*) FROM public_health_indicators;
'''

cursor.execute(query)
total_records = cursor.fetchone()[0]

fig, ax = plt.subplots(figsize=(6, 3))
ax.text(0.5, 0.5, f"Total Records:\n{total_records}", 
        fontsize=20, ha='center', va='center', fontweight='bold')
ax.axis('off')
plt.title("Database Summary", fontsize=14)
plt.savefig('plots/total_records_card.png')
plt.close()


#Query 2: Records per Country
query = '''
SELECT country_name, COUNT(*) AS records
FROM public_health_indicators
GROUP BY country_name
ORDER BY records DESC;
'''
df = pd.read_sql_query(query, conn)


plt.figure(figsize=(8,5))
sns.barplot(x='country_name', y='records', data=df, palette='Blues_d')
plt.title('Records per Country')
plt.xlabel('Country')
plt.ylabel('Number of Records')
plt.savefig('plots/records_per_country.png')
plt.close()


#Query 3: Average Life Expectancy in 2020
query = '''
SELECT country_name, AVG(value) AS avg_life_expectancy
FROM public_health_indicators
WHERE indicator_name LIKE '%Life expectancy%'
AND year = 2020
GROUP BY country_name
ORDER BY avg_life_expectancy DESC;
'''
df = pd.read_sql_query(query, conn)

plt.figure(figsize=(8,5))
sns.barplot(x='country_name', y='avg_life_expectancy', data=df, palette='Greens_d')
plt.title('Average Life Expectancy by Country (2020)')
plt.xlabel('Country')
plt.ylabel('Life Expectancy (years)')
plt.savefig('plots/life_expectancy_2020.png')
plt.close()


#Query 4: Life Expectancy Trends (1960–2020)
query = '''
SELECT country_name, year, value AS life_expectancy
FROM public_health_indicators
WHERE indicator_name LIKE '%Life expectancy%'
AND year BETWEEN 1960 AND 2020
ORDER BY country_name, year;
'''
df = pd.read_sql_query(query, conn)


g = sns.FacetGrid(df, col="country_name", col_wrap=2, height=4, aspect=1.5)
g.map(sns.lineplot, 'year', 'life_expectancy')
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Life Expectancy")
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Life Expectancy Trends (1960–2020)')
g.savefig('plots/life_expectancy_trends.png')
plt.close()


#Query 5: Immunization Trends (1980–2020)
query = '''
SELECT country_name, year, value AS immunization_rate
FROM public_health_indicators
WHERE indicator_name LIKE '%DPT%'
AND year BETWEEN 1980 AND 2020
ORDER BY country_name, year;
'''
df = pd.read_sql_query(query, conn)

g = sns.FacetGrid(df, col="country_name", col_wrap=2, height=4, aspect=1.5)
g.map(sns.lineplot, 'year', 'immunization_rate')
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Immunization Rate (%)")
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Immunization Trends (1980–2020)')
g.savefig('plots/immunization_trends.png')
plt.close()


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
top_country_name = top_country[0]
top_immunization_rate = top_country[1]

fig, ax = plt.subplots(figsize=(6, 3))
ax.text(0.5, 0.5, f"Top Immunization Country (2020):\n{top_country_name} ({top_immunization_rate}%)", 
        fontsize=18, ha='center', va='center', fontweight='bold')
ax.axis('off')
plt.title("Public Health Highlight", fontsize=14)
plt.savefig('plots/top_immunization_card.png')
plt.close()



#Query 7: Maternal Mortality Trends (1990–2020)
query = '''
SELECT country_name, year, value AS maternal_mortality
FROM public_health_indicators
WHERE indicator_name LIKE '%Maternal mortality%'
AND year BETWEEN 1990 AND 2020
ORDER BY country_name, year;
'''
df = pd.read_sql_query(query, conn)

g = sns.FacetGrid(df, col="country_name", col_wrap=2, height=4, aspect=1.5)
g.map(sns.lineplot, 'year', 'maternal_mortality')
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Maternal Mortality (per 100k births)")
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Maternal Mortality Trends (1990–2020)')
g.savefig('plots/maternal_mortality_trends.png')
plt.close()


#Query 8: Maternal Mortality Improvement
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

plt.figure(figsize=(8,5))
sns.barplot(x='country_name', y='change', data=df, palette='Reds_d')
plt.title('Maternal Mortality Changes (1990–2020)')
plt.xlabel('Country')
plt.ylabel('Change (Deaths per 100k births)')
plt.savefig('plots/maternal_mortality_changes.png')
plt.close()
