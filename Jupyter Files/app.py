import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of prcp data including the date and prcp measurement for each date"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date>="2016-08-23").filter(measurement.date<="2017-08-23").all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        percipitation_dict = {}
        percipitation_dict["date"] = date
        percipitation_dict["prcp"] = prcp
        all_prcp.append(percipitation_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(station.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all prcp data for the most active station"""
    # Query all stations
    results = session.query(station.name, measurement.station, measurement.date, measurement.tobs).filter(measurement.station == station.station).filter(measurement.station == 'USC00519281').filter(measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def user_input(start, end):
    
    session = Session(engine)
    
    if end:
        results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date.between(start, end)).all()
    else:
        results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>= start).all()
    
    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
