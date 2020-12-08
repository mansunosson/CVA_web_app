from flask import Flask, render_template, url_for, flash, redirect
from form import CVAform
from selenium import webdriver
import time
import re
from datetime import date
from zeep import Client
import numpy as np
import pickle

# Load PD model
classifier = pickle.load(open('pd_model.sav', 'rb'))


# Define fetch_10Yrate function
def fetch_10Yrate():
    wsdl_url = "https://swea.riksbank.se/sweaWS/wsdl/sweaWS_ssl.wsdl"
    soap_client = Client(wsdl_url)
    RB_api_result = soap_client.service.getLatestInterestAndExchangeRates('en', 'SEGVB10YC').groups[0].series[0].resultrows[0].value;
    return RB_api_result*0.01

# Define fetch_pd function
def fetch_pd(company_name):
    #convert input name to URL format
    company_name.replace(' ', '%20')
    browser = webdriver.Firefox()
    browser.get('https://www.allabolag.se/what/' + company_name) 
    time.sleep(np.random.exponential(scale=4.0, size=None)+1) # random wait time to emulate human
    try:
        names = browser.find_elements_by_class_name('search-results__item__title')
        ct_names  = [elem.text for elem in names]
        names[ct_names.index(company_name)].click()        # click company name 
        time.sleep(np.random.exponential(scale=4.0, size=None)+1) # random wait time to emulate human
        KPI1element = browser.find_element_by_class_name('table--border-separator.figures-table').text.replace(" ", "")
        KPI1 = [int(d) for d in re.findall(r'-?\d+', KPI1element)] 
        KPI2element= browser.find_elements_by_class_name('cc-block-value')
        KPI2 = [elem.text for elem in KPI2element]
        KPI2 = [val.replace(',', '.') for val in KPI2] 
        KPI2 = [val.replace('%', '') for val in KPI2]
        KPI2 = [float(i) for i in KPI2] 
        browser.close()
        return float(classifier.predict_proba(np.transpose(np.array([KPI1[0], KPI1[1], KPI1[2], KPI1[3], KPI2[0], KPI2[1], KPI2[2], KPI2[3]]).reshape(-1, 1)))[:,1])
    except:
        browser.close()
        return "N/A"  
    
# Define CVA function
def CVA(company_name, nominal_value, maturity_date, risk_free_rate):
    try:
        duration_coef = ((maturity_date-date.today()).days)/365 # Duration as proportion of full year 
        annual_PD = fetch_pd(company_name) # Call to fetch_pd scrapes the key performance indicators used in pd_model from *REDACTED*
        duration_PD = 1-(1-annual_PD)**duration_coef # This calculation of duration probability of default prob assumes flat term structure, see https://www.openriskmanual.org/wiki/How_to_Estimate_Lifetime_PD_from_12_month_PD
        adj_value = (1-duration_PD)*nominal_value/((1+risk_free_rate)**duration_coef) # This values the credit by calculating the present value and multiplying by the default probability, which assumes Loss Given Defauly = nominal value   
        return str('Invoice value: ' + str(round(adj_value,1)) + ', annual PD: ' + str(round(annual_PD*100,1)) + '% , duration: '+ str(round(duration_coef*365,0))+ ' days, and duration PD: ' + str(round(duration_PD*100,1)) + '%') 
    except TypeError:
        return str('Could not find parameters to adjust credit valuation, check spelling of company name and/or date')
  
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