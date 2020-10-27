# sqlalchemy-challenge
## Background
Using SQLAlchemy ORM queries and Pandas to perform climate analysis of Hawaii's weather year-round

## Climate Analysis and App
The first portion of this project uses Python and SQLAlchemy to do basic climate analysis and data exploration of the Hawaii climate database. Namely analysis of precipitation measurements and temperature observations of multiple weather stations in a given date range. In the next step, Flask was used to create a climate app to display the information queried in the initial analysis.

## Additional Analysis
The second portion of this project expands on the initial climate analysis. The notebook contains the function `calc_temps` that accepts a start date and end date in the format `%Y-%m-%d` and returns the minimum, average, and maximum temperatures for that range of dates and the function `daily_normals` that calculates the daily normals for a specific date `%m-%d`

## Submission
This repository contains:
- The raw file `hawaii.sqlite`
- Notebook `climate.ipynb` with all climate analysis
- Python script `app.py` with the Flask API code for the Climate app
