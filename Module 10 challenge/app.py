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
