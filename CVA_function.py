# Dependencies
#from datetime import date

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
        
