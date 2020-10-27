import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
import numpy as np

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)
@app.route("/")
def home():
	return (
		f"Welcome to the Climate API!<br/>"
		f"Available Routes:<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/&lt;start&gt;<br/>"
        	f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
		)

@app.route("/api/v1.0/precipitation")
def precipitation():
	session = Session(engine)
	
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	one_year_ago = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')
	results = session.query(Measurement.date, Measurement.prcp).\
filter(Measurement.date>=one_year_ago).order_by(Measurement.date).all()

	session.close()
	
	# Convert list of tuples into dictionary
	date_prcp = []
	for date, prcp in results:
		prcp_dict = {}
		prcp_dict["date"] = date
		prcp_dict["prcp"] = prcp
		date_prcp.append(prcp_dict)
	
	return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)
	
	results = session.query(Station.station).all()

	session.close()

	station_list = list(np.ravel(results))

	return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)
	
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	one_year_ago = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')
	
	results = session.query(Measurement.date, Measurement.tobs).\
filter(Measurement.station=='USC00519281').\
filter(Measurement.date>=one_year_ago).\
order_by(Measurement.date).all()
	
	session.close()

	return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_date(start):
	session = Session(engine)

	sel = [Measurement.date,\
		func.min(Measurement.tobs),\
		func.max(Measurement.tobs),\
		func.avg(Measurement.tobs)]
	results = session.query(*sel).filter(Measurement.date>=start).group_by(Measurement.date).all()
	
	tobs_list = []
	for date, min, avg, max in results:
		tobs_dict = {}
		tobs_dict["Date"] = date
		tobs_dict["TMIN"] = min
		tobs_dict["TMAX"] = max
		tobs_dict["TAVG"] = avg
		tobs_list.append(tobs_dict)

	session.close()

	return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

	session = Session(engine)

	sel = [Measurement.date,\
		func.min(Measurement.tobs),\
		func.max(Measurement.tobs),\
		func.avg(Measurement.tobs)]
	results = session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).group_by(Measurement.date).all()
	
	tobs_list = []
	for date, min, avg, max in results:
		tobs_dict = {}
		tobs_dict["Date"] = date
		tobs_dict["TMIN"] = min
		tobs_dict["TMAX"] = max
		tobs_dict["TAVG"] = avg
		tobs_list.append(tobs_dict)

	session.close()

	return jsonify(tobs_list)

if __name__ == "__main__":
	app.run(debug=True)