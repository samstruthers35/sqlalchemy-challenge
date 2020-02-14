import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

engine = create_engine('sqlite:///hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

app = Flask(__name__)
@app.route("/")
def index():
    return(
        "Welcome to the Climate App!<br />"
        "Available Routes:<br />"
        "/api/v1.0/precipitation<br />"
        "/api/v1.0/stations<br />"
        "/api/v1.0/tobs<br />"
        "/api/v1.0/<start> ENTER START DATE AT END OF URL <br /> "
        "/api/v1.0/<start><end> ENTER START DATE/END DATE AT END OF URL<br />"
    ) 

@app.route("/api/v1.0/precipitation")
def precipitation():
        todays_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        precipitation = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date > twelve_months)
        
        rain = []
        for rains in precipitation:
            row = {}
            row["date"] = rains[0]
            row["prcp"] = rains[1]
            rain.append(row)
       
        return jsonify(rain)    

@app.route("/api/v1.0/stations")
def stations():
        station_names = session.query(Station.station, Station.name).group_by(Station.station).all()
        names_dict = []
        for names in station_names:
            row_names = {}
            row_names["station name"] = names[0]
            names_dict.append(row_names)
              
        return jsonify(names_dict)
    
@app.route("/api/v1.0/tobs")
def tobs():
        todays_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        tobs_session = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > twelve_months)
        
        temperature = []
        for degrees in tobs_session:
            row_tobs = {}
            row_tobs["date"] = degrees[0]
            row_tobs["tobs"] = degrees[1]
            temperature.append(row_tobs)
            
        return jsonify(temperature)    

@app.route("/api/v1.0/<start>")
def starting(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    starting_date = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
                         filter(Measurement.date >= start_date)
    date_tobs = []
    for tobs in starting_date:
        tobs_json = {}
        tobs_json["AVERAGE TEMPERATURE"] = tobs[2]
        tobs_json["MAXIMUM TEMPERATURE"] = tobs[0]
        tobs_json["MINIMUM TEMPERATURE"] = tobs[1]
        
        date_tobs.append(tobs_json)

    
    
    return jsonify(date_tobs)

@app.route("/api/v1.0/<start>/<end>")
def range(start,end):
    start_range = dt.datetime.strptime(start, '%Y-%m-%d')
    end_range = dt.datetime.strptime(end, '%Y-%m-%d')
    date_range = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).\
                         filter(Measurement.date >= start_range, Measurement.date <= end_range)
    date_range_tobs = []
    for tobs_range in date_range:
        tobs_json_range = {}
        tobs_json_range["AVERAGE TEMPERATURE"] = tobs_range[2]
        tobs_json_range["MAXIMUM TEMPERATURE"] = tobs_range[0]
        tobs_json_range["MINIMUM TEMPERATURE"] = tobs_range[1]
        
        date_range_tobs.append(tobs_json_range)

    
    
    return jsonify(date_range_tobs)

if __name__ == "__main__":
    app.run(debug=True)