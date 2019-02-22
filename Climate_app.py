#   Climate apps
#   Routes
#   * `/`
#    * Home page.

#   * List all routes that are available.
#   * `/api/v1.0/precipitation`
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.

#   * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.

#   * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.

#   * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
#**********************************************************************************

# Import all relevent modules
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import bindparam
from sqlalchemy import text
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation Data for the last one year:<br/>"
        #f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"A list of station and the station name:<br/>"
        #f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature observations for last one year:<br/>"
        #f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Type in date like 2016-08-24 to get Average, Max and Min Temperatures:<br/>"
        #f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"Type in date range like 2016-08-24\2017-08-24 to get Average, Max and Min Temperatures for that range:<br/>"
        #f"<br/>"
        f"/api/v1.0/<start><end><br/>"
    )

#**********************************************************************************

@app.route("/api/v1.0/precipitation")
def precipitaion():
    # Query to get dates and precipitaion for the last year from last date, order by date ascending
    precp = engine.execute('select date, prcp from measurement WHERE DATE >= DATE("2017-08-23", "-365 days")\
    order by date asc').fetchall()
    # Create a list of dictionaries with date and precp as keys with corresponding values
    precp_totals = []
    for result in precp:
        row = {}
        row["Date"] = result['date']
        row["Precipitation"] = result['prcp']
        precp_totals.append(row)
    return jsonify(precp_totals)

#**********************************************************************************
@app.route("/api/v1.0/stations")
def stations():
    # Query to get sattion and name from the station table
    station = engine.execute('select station, name from station order by station').fetchall()
    # Create a list of dictionaries with station and name as keys with corresponding values
    station_totals = []
    for results in station:
        row = {}
        row["Station"] = results['station']
        row["Name"] = results['name']
        station_totals.append(row)
    return jsonify(station_totals)

#**********************************************************************************
@app.route("/api/v1.0/tobs")
def tobs():
    # Query for the dates and temperature observations from a year from the last data point
    station_tobs = engine.execute('select station, date, tobs from measurement WHERE DATE >= DATE("2017-08-23", "-365 days") \
        order by station').fetchall()
    # Create a list of dictionaries with station, date, tobs as keys with corresponding values
    tobs_totals = []
    for results in station_tobs:
        row = {}
        row["Station"] = results['station']
        row["Date"] = results['date']
        row["Temperature"] = results['tobs']
        tobs_totals.append(row)
    return jsonify(tobs_totals)

#**********************************************************************************
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Query for the minimum temperature, the average temperature, and the max temperature for a given start date
    stmt = 'select date, min(tobs), avg(tobs), max(tobs) from measurement WHERE DATE >= :startdate group by date order by date'
    temp_stats = engine.execute(text(stmt), startdate = start)
    # Create a list of dictionaries with date, Min Temp, Avg Temp and Max Temp as keys with corresponding values
    temp_totals = []
    for results in temp_stats:
        row = {}
        row["Date"] = results['date']
        row["Min Temp"] = results['min(tobs)']
        row["Avg Temp"] = results['avg(tobs)']
        row["Max Temp"] = results['max(tobs)']
        temp_totals.append(row)
    return jsonify(temp_totals)

#**********************************************************************************
@app.route("/api/v1.0/<start>/<end>")
def temp_end(start, end):
    # Query for the minimum temperature, the average temperature, and the max temperature for a given start date
    stmt1 = 'select date, min(tobs), avg(tobs), max(tobs) from measurement WHERE DATE >= :startdate \
        and DATE <= :enddate group by date order by date'
    temp_stats1 = engine.execute(text(stmt1), startdate = start, enddate = end)
    # Create a list of dictionaries with date, Min Temp, Avg Temp and Max Temp as keys with corresponding values
    temp_totals1 = []
    for results in temp_stats1:
        row = {}
        row["Date"] = results['date']
        row["Min Temp"] = results['min(tobs)']
        row["Avg Temp"] = results['avg(tobs)']
        row["Max Temp"] = results['max(tobs)']
        temp_totals1.append(row)
    return jsonify(temp_totals1)

#**********************************************************************************

if __name__ == '__main__':
    app.run(debug=True)
