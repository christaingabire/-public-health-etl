import json
import pandas as pd


#Read the JSON file 

json_file_path = "data/Health Nutrition and Population Statistics.json"

with open(json_file_path, 'r') as file:
    json_data = json.load(file)

print("\nTop level keys in JSON:")
print(json_data.keys())

print("\nIdentification Section:")
print(json_data.get('identification', {}))


#Read the Excel file

excel_file_path = 'data/HNP_StatsEXCEL.xlsx'

xls = pd.ExcelFile(excel_file_path)
print("\nSheets available in Excel file:")
print(xls.sheet_names)

#Loading the main data sheet
df = pd.read_excel(excel_file_path, sheet_name='Data')

print("\nFirst 5 rows of the Excel data:")
print(df.head())

#Saving the raw version for backup
df.to_csv('data/hnp_data_raw.csv', index=False)
print("\nSaved raw Excel data to 'data/hnp_data_raw.csv'!")



# Filtering Data/ Transformation Phase

#Defining target countries and indicators to work with
target_countries = ['Kenya', 'Ghana', 'South Africa', 'Ethiopia']
target_indicators = [
    'Life expectancy at birth, total (years)', 
    'Immunization, DPT (% of children ages 12-23 months)', 
    'Maternal mortality ratio (modeled estimate, per 100,000 live births)'
]

#Filtering for selected countries
df_filtered = df[df['Country Name'].isin(target_countries)]

#Filtering for selected indicators
df_filtered = df_filtered[df_filtered['Indicator Name'].isin(target_indicators)]

print("\nFiltered data shape:", df_filtered.shape)


#Reshaping the Data 

years = [str(year) for year in range(1960, 2024)]  # 1960 to 2023
df_melted = df_filtered.melt(
    id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
    value_vars=years,
    var_name='Year',
    value_name='Value'
)

print("\nFirst 5 rows after melting (reshaping):")
print(df_melted.head())

#Cleaning Missing Values

df_cleaned = df_melted.dropna(subset=['Value'])

print("\nShape after dropping missing values:", df_cleaned.shape)

#Save Cleaned Data

df_cleaned.to_csv('data/hnp_data_cleaned.csv', index=False)

print("\nSaved cleaned data to 'data/hnp_data_cleaned.csv'!")
print("\nFirst few rows of cleaned data:")
print(df_cleaned.head())
