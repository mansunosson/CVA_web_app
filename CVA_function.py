#from datetime import date
def CVA(company_name, nominal_value, maturity_date, risk_free_rate):
    try:
        duration_coef = ((maturity_date-date.today()).days)/365 # Duration as proportion of full year 
        annual_PD = fetch_pd(company_name) # Call to fetch_pd scrapes the key performance indicators used in pd_model from *REDACTED*
        duration_PD = 1-(1-annual_PD)**duration_coef # This calculation of duration probability of default prob assumes flat term structure, see https://www.openriskmanual.org/wiki/How_to_Estimate_Lifetime_PD_from_12_month_PD
        adj_value = (1-duration_PD)*nominal_value/((1+risk_free_rate)**duration_coef) # This values the credit by calculating the present value and multiplying by the default probability, which assumes Loss Given Defauly = nominal value   
        return print('The present value is ' + str(adj_value) + ' when accounting for an annual default probability of ' + str(annual_PD) + ', a duration of '+ str(duration_coef*365)+ ' days, and a duration default probability of ' + str(duration_PD)) 
    except TypeError:
        return print('Could not find default probability, check spelling of company name')
        