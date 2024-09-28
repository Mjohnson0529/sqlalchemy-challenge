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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement


# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Create the homepage
@app.route("/")
def welcome():
    """All available API routes."""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"<p>'Start' and 'End' must be in YYYY-MM-DD format, from 2010-01-01 to 2017-08-23.</p>"
    )
# Create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB.
    session = Session(engine)
    
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()

    # Close the session
    session.close()
    
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    precip_analysis = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_analysis.append(precip_dict)
        
    return jsonify(precip_analysis)

# Create stations route
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB.
    session = Session(engine)

    stations = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    # close the session
    session.close()

    # Covert query results to a dictionary
    stations_list = []
    for station, count in stations:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["count"] = count
        stations_list.append(stations_dict)
        
    return jsonify(stations_list)

# Create tobs route
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB.
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year of data.
    most_rct = dt.date(2017, 8, 23)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]

    date_temps = session.query(measurement.date, measurement.tobs).filter(measurement.date>= last_year, measurement.station == tobs).all()

    # close the session
    session.close()

    # Covert query results to a dictionary
    station_analysis = []
    for date, tobs in date_temps:
        date_tobs = {}
        date_tobs["date"] = date
        date_tobs["tobs"] = tobs
        station_analysis.append(date_tobs)

        
    return jsonify(station_analysis)

# Create route for start date
@app.route("/api/v1.0/<start>")
def start_date(start):

    # Create our session (link) from Python to the DB.
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%m-%d")
    start_range = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()

    # close the session
    session.close()

    # Covert query results to a dictionary
    start_range_analysis = []
    for min, max, avg in start_range:
        start_dict = {}
        start_dict["Min Temp"] = min
        start_dict["Max Temp"] = max
        start_dict["Avg Temp"] = avg
        start_range_analysis.append(start_dict)
        
    return jsonify(start_range_analysis)

# Create route for start and end date range
@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):

    # Create our session (link) from Python to the DB.
    session = Session(engine)

    start_end_range = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()

    # close the session
    session.close()

    # Covert query results to a dictionary
    range_analysis = []
    for min, max, avg in start_end_range:
        range_dict = {}
        range_dict["Minimum Temperature"] = min
        range_dict["Maxium Temperature"] = max
        range_dict["Average Temperature"] = avg
        range_analysis.append(range_dict)
        
    return jsonify(range_analysis)

    
if __name__ == '__main__':
    app.run(debug=True)