# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite://hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
#define welcome route and display available routes
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"x/api/v1.0/temp/start<br/>"
    )
@app.route("/api/v1.0/precipitation")
#Define precipitation route to display data from the last year
def precipitation():
    one_year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_data = {date: prcp for date, prcp in data}
    return jsonify(precipitation_data)
#Define stations route that returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    station_results = list(np.ravel(results))
    return jsonify(station_results)
#Define tobs route that returns jsonified data for the most active station for the last year
@app.route("/api/v1.0/tobs")
def temps():
    one_year_ago = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(measurement.date >= one_year_ago).all()
    temps_list = list(np.ravel(results))
    return jsonify(temps_list)

#Define dynamic route when given start date
@app.route("/api/v1.0/temp/<start>")
def start_stats(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    one_year = dt.timedelta(days=365)
    start = start_date-one_year
    end_date = dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end_date).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
#Define dynamic route when given start and end date
@app.route("/api/v1.0/temp/<start>/<end>")
def date_info(start,end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    ending_date = dt.datetime.strptime(end, '%Y-%m-%d')
    one_year = dt.timedelta(days=365)
    start = start_date-one_year
    dates_data = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    data_list = list(np.ravel(dates_data))
    return jsonify(data_list)

if __name__ == "main":
    app.run(debug=True)


