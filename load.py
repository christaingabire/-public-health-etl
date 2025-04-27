import sqlite3
import pandas as pd

#Connect to SQLite database

conn = sqlite3.connect('data/health_data.db')
cursor = conn.cursor()

print("Connected to SQLite database!")

#Creating a table

create_table_query = '''
CREATE TABLE IF NOT EXISTS public_health_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT,
    country_code TEXT,
    indicator_name TEXT,
    indicator_code TEXT,
    year INTEGER,
    value REAL
);
'''

cursor.execute(create_table_query)
conn.commit()

print("Created the table!")

#Read cleaned CSV

df = pd.read_csv('data/hnp_data_cleaned.csv')

print("\nFirst few rows of the cleaned CSV:")
print(df.head())

#Insert data into the table

# Inserting row, one by one
for index, row in df.iterrows():
    insert_query = '''
    INSERT INTO public_health_indicators 
    (country_name, country_code, indicator_name, indicator_code, year, value)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (
        row['Country Name'],
        row['Country Code'],
        row['Indicator Name'],  
        row['Indicator Code'],
        int(row['Year']),
        float(row['Value'])
    ))

conn.commit()

print(f"Inserted {len(df)} rows into the table!")


#Verification

cursor.execute('SELECT * FROM public_health_indicators LIMIT 5;')
rows = cursor.fetchall()

print("\nSample data from database:")
for row in rows:
    print(row)


#Close the connection

conn.close()
print("\nDatabase connection closed!")
