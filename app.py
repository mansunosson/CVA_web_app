from flask import Flask, render_template, url_for, flash, redirect
from form import CVAform
from selenium import webdriver
import time
import re
from datetime import date
from zeep import Client
import numpy as np
import pickle

# Import req. functions
from fetch_interest_function import fetch_10Yrate
from fetch_pd_function import fetch_pd
from CVA_function import CVA

# Load PD model
classifier = pickle.load(open('pd_model.sav', 'rb'))
  
app = Flask(__name__)
app.config['SECRET_KEY'] = '27cffa341fa53894'

# Call to fetch_10Yrate grabs interest rate of 10Y Treasury Bond from Riksbankens API 
RF_rate = fetch_10Yrate()

@app.route('/', methods  = ['GET', 'POST'])
def evaluate():
    form = CVAform()
    if form.validate_on_submit(): 
        flash(CVA(form.companyname.data, float(form.facevalue.data), form.maturity.data, RF_rate))
    return render_template('cva.html', title = 'Credit Valutation Adjustment', form = form)

if __name__ == '__main__':
    app.run(debug = True)
