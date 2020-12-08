# Dependencies
#pip install zeep
#from zeep import Client
def fetch_10Yrate():
    wsdl_url = "https://swea.riksbank.se/sweaWS/wsdl/sweaWS_ssl.wsdl"
    soap_client = Client(wsdl_url)
    RB_api_result = soap_client.service.getLatestInterestAndExchangeRates('en', 'SEGVB10YC').groups[0].series[0].resultrows[0].value;
    return RB_api_result*0.01







    
    
    
