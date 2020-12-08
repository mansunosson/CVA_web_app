# Dependencies
#from selenium import webdriver
#import time
#import re
def fetch_pd(company_name):
    #convert input name to URL format
    company_name.replace(' ', '%20')
    browser = webdriver.Firefox()
    browser.get('https://www.allabolag.se/what/' + company_name) 
    time.sleep(np.random.exponential(scale=2.0, size=None)+1) # random wait time to emulate human
    try:
        names = browser.find_elements_by_class_name('search-results__item__title')
        ct_names  = [elem.text for elem in names]
        names[ct_names.index(company_name)].click()        # click company name    NOTE: THIS DOES NOT DO EXACT STRING MATCH, FIX!   
        time.sleep(np.random.exponential(scale=2.0, size=None)+1) # random wait time to emulate human
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
        return "N/A"
        
        
    
