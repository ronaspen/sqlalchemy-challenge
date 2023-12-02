import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    
    precipitation = []
    
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        precipitation.append(prcp_dict)
            
    return jsonify(precipitation)
        

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    
    
    stations = []
    
    for station, name, latitude, longitude, elevation in results:
        st_dict = {}
        st_dict["station"] = station
        st_dict["name"] = name 
        st_dict["latitude"] = latitude
        st_dict["longitude"] = longitude 
        st_dict["elevation"] = elevation
        stations.append(st_dict)
            
    return jsonify(stations)
        

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(lateststr, '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)
    result = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= querydate).all()


    session.close()
    
    tobs = []
    
    for date, tobs in result:
        t_dict = {}
        t_dict["date"] = date
        t_dict["tobs"] = tobs
        tobs.append(t_dict)
        
    return jsonify(tobs)
    

@app.route('/api/v1.0/<start>')
def get_start(start):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    
    stats = []
    for min,avg,max in result:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Average"] = avg
        stats_dict["Max"] = max
        stats.append(stats_dict)

    return jsonify(stats)
     


@app.route('/api/v1.0/<start>/<end>')
def get_start_end(start,end):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    
    stats = []
    for min,avg,max in result:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Average"] = avg
        stats_dict["Max"] = max
        stats.append(stats_dict)

    return jsonify(stats)
    