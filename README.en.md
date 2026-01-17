[Version française](README.md)
---
# SAE15 – University Success
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success)](#)
[![Data Source](https://img.shields.io/badge/Data-data.gouv.fr-orange)](https://www.data.gouv.fr/api/1/datasets/r/18e77311-5d8f-424d-b73e-defc8f446ef6)

## Participants
- **DIAZENZA MOUANDA Regis Japhet**
- **BELGOUR Aicha Soulef**
- **ROLIN Tom**

---
## Project Overview

- This project is an automated ETL (Extract, Transform, Load) pipeline designed to process open data regarding the academic paths and success rates of baccalaureate graduates 
in French **DUT (Diplôme Universitaire de Technologie)** programs.

- The system downloads raw CSV data from the French government, cleans it using **Pandas**, transforms it into **JSON**, and generates interactive graphical visualizations via the **QuickChart API**.
---

## Project Objectives

- **Extraction**: Download CSV files from the data.gouv.fr platform.
- **Transformation**: Analyze the data structure and clean values (conversion of textual fields into numerical data).
- **Loading**: Produce a results file in JSON format (`donnees_filtrees.json`) as well as a graph generated using **QuickChart**.

---
## Steps to Run the script :
1. Prerequisites :
Make sure Python3 is installed with the packages `pandas` and `requests` (os, csv, json, sys, webbrowser are already included in Python3):  
```bash
  pip install pandas requests
```
2. Save the script [code_final.py](./code_final.py) and run it:
```bash
  python3 code_final.py
```
3. The script automatically:
- Downloads the CSV from data.gouv.fr
- Cleans the data (removes certain columns, replaces missing values with 0, removes duplicates)
- Saves the cleaned CSV
- Converts it to JSON (donnees.json)
- Filters relevant columns into donnees_filtrees.json
- Generates charts
- Opens the charts in the browser

## Gantt Chart

This Gantt chart presents the complete planning of our project.

![Gantt Chart](GANTT.png)

---

## Technologies Used

- **Python 3**
- **requests**: data download
- **pandas**: data cleaning and processing
- **csv / json / os**: data transformation
- **webbrowser**: automatic opening of results in a web browser

---

## 1. File Extraction — by DIAZENZA MOUANDA Regis Japhet

### Objective
Download the CSV file from **data.gouv.fr** and clean it to make it usable.

### Libraries Used
- **requests**: data retrieval  
- **pandas**: data cleaning  

### Script Workflow
- Download the CSV file via the data.gouv.fr API  
- Remove unnecessary columns (`Id`, `sigle`)  
- Replace missing values with `0`  
- Remove duplicate rows  
- Save the cleaned CSV file  

---

## 2. CSV to JSON Transformation — by ROLIN Tom

### Objective
Convert the cleaned CSV file into **JSON**, a format more suitable for data exchange.

### Libraries Used
- **csv**: reading CSV files  
- **json**: writing JSON files  
- **os**: checking file existence  

### Script Workflow
- Check that the CSV file exists  
- Read the CSV file using a semicolon (`;`) separator  
- Convert each row into a Python dictionary  
- Store all rows in a list  
- Write the formatted result into a JSON file  

---

## 3. Visualization (Filtering & Display) — by BELGOUR Aicha Soulef

### Objective
This code filters and classifies the data, then generates representative graphs using **QuickChart**.

### Libraries Used
- **pandas**: intelligent data filtering and calculations (`groupby`)  
- **requests**: sending data to the QuickChart API to generate the image  
- **webbrowser**: automatic display in a web browser  
- **os**: input/output file management  

### Script Workflow
- **Filtering**: Reads the JSON file and keeps only columns related to *Success* (Graduation) and *Progression* (Advancement)  
- **Preparation**: Sorts DUT programs by success rate (Top 20)  
- **Generation**: Creates a chart URL via QuickChart  
- Bar chart for Graduation  
- Line chart for Advancement  
- **Display**: Automatically opens the generated URL in the web browser  
---
