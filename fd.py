import os,json
from datetime import datetime
from config import url_call_apache
import pandas as pd

source_path = os.path.dirname(__file__)
source_path = str(source_path) 

def fds_calculate(form):
     # Request 
    rows = (form.get('rowCount')) ; rows = int(rows)
    print(rows)
    json_data = {}
    for row in range(1,rows):
        # User Input
        principal = (form.get(f'principal{row}')) 
        rate = (form.get(f'rate{row}'))
        start = form.get(f'start{row}')
        maturity = form.get(f'maturity{row}')

        try:
            
            slice_start = form.get(f'slice_start{row}')
            slice_end = form.get(f'slice_end{row}')
        except:
            pass

        compounding = form.get(f'compound{row}')
        payout = form.get(f'payout{row}') 

        # Convert the string to a datetime object
        start = datetime.strptime(start, "%Y-%m-%d")
        maturity = datetime.strptime(maturity, "%Y-%m-%d")
        json_data["apikey"] = "4f6cf513f9c56a5cde0d104f8c42c86376d85ab98bbeef0d1e5f81272dff3c6c" 
        json_data["no_of_slices"] = 1
        json_data["no_of_instruments"] = rows


        # Converting user input to json request
        try:
            slice_start = datetime.strptime(slice_start, "%Y-%m-%d")
            slice_end = datetime.strptime(slice_end, "%Y-%m-%d")
            
        except:
            pass
  
def fd_calculate(form):
    # Request json
    values = []
    slices = []
    json_file_path = source_path+'\\json_data\\fd.json'
    try:
        with open(json_file_path, 'r') as json_file:
            data = json_file.read()
            json_data = json.loads(data)
    except FileNotFoundError:
        return "JSON file not found", 404
    except Exception as e:
        return str(e), 500
    
    # User Input
    principal = (form.get('principal')) ; values.append(principal)
    rate = (form.get('rate')); values.append(rate)
    start = form.get('start');  values.append(start)
    maturity = form.get('maturity');  values.append(maturity)
    
    try:
        
        slice_start = form.get('slice_start');  slices.append(slice_start)
        slice_end = form.get('slice_end');  slices.append(slice_end)        
    except:
        pass
    
    
    compounding = form.get('compound');  values.append(compounding)
    payout = form.get('payout');  values.append(payout) 

    # Convert the string to a datetime object
    start = datetime.strptime(start, "%Y-%m-%d")
    maturity = datetime.strptime(maturity, "%Y-%m-%d")
    
    # Converting user input to json request
    try:
        slice_start = datetime.strptime(slice_start, "%Y-%m-%d")
        slice_end = datetime.strptime(slice_end, "%Y-%m-%d")
        
        # User's Slice Input 
        json_data["slicing_periods"]["0"]["slice_start"] = datetime.strftime(slice_start, "%m/%d/%Y")
        json_data["slicing_periods"]["0"]["slice_end"] = datetime.strftime(slice_end, "%m/%d/%Y")
        
        # Current Evaluation
        todays_date = datetime.now()
        json_data["slicing_periods"]["1"]["slice_start"] = datetime.strftime(start, "%m/%d/%Y")
        json_data["slicing_periods"]["1"]["slice_end"] = datetime.strftime(todays_date, "%m/%d/%Y")
        
        # Total Interest
        json_data["slicing_periods"]["2"]["slice_start"] = datetime.strftime(start, "%m/%d/%Y")
        json_data["slicing_periods"]["2"]["slice_end"] = datetime.strftime(maturity, "%m/%d/%Y")
        
    except Exception as e:
        # Giving whole Instrument as Slice
        json_data["slicing_periods"]["0"]["slice_start"] = datetime.strftime(start, "%m/%d/%Y")
        json_data["slicing_periods"]["0"]["slice_end"] = datetime.strftime(maturity, "%m/%d/%Y")
        
        # Current Evaluation
        todays_date = datetime.now()
        json_data["slicing_periods"]["1"]["slice_start"] = datetime.strftime(start, "%m/%d/%Y")
        json_data["slicing_periods"]["1"]["slice_end"] = datetime.strftime(todays_date, "%m/%d/%Y")
        
        # Total Interest
        json_data["slicing_periods"]["2"]["slice_start"] = datetime.strftime(start, "%m/%d/%Y")
        json_data["slicing_periods"]["2"]["slice_end"] = datetime.strftime(maturity, "%m/%d/%Y")
        
        
    json_data["instruments"]["0"]["compounding_period"] = int(compounding)
    json_data["instruments"]["0"]["principal"] = int(principal)
    json_data["instruments"]["0"]["interest_rate"] = float(rate)/100
    json_data["instruments"]["0"]["start_date"] = datetime.strftime(start, "%m/%d/%Y")
    json_data["instruments"]["0"]["end_date"] = datetime.strftime(maturity, "%m/%d/%Y")
    json_data["instruments"]["0"]["interest_payment_period"] = int(payout)
    json_response = url_call_apache(req=json_data, app='idep', api='cd_slice_interest')
    try:
        
        fd_df = pd.DataFrame(json_response['Out'])
        
        # For Finding Today's Valuation of the instrument
        current_evaluate_df = fd_df[fd_df['SliceNo']==1]
        current_evaluation_interest = current_evaluate_df['Amount'].sum()

        # For Finding Total Valuation of the instrument
        total_df = fd_df[fd_df['SliceNo']==2]
        total_interest = total_df['Amount'].sum()
        
        # For Overall Slice/Instrument
        fd_df = fd_df[fd_df['SliceNo']==0]
        fd_df['Amounts'] = fd_df['Amount'].cumsum()
        fd_df['Principal'] = fd_df['Amounts'] + float(principal)
        principal_amounts = fd_df["Principal"].to_list()
        line_labels = fd_df["EndDate"].to_list()
        skips = int(compounding);  skips = 12//skips
        line_labels = line_labels[::skips]
        slice_interest = fd_df['Amount'].sum()
        return line_labels, principal_amounts, slice_interest ,principal, values, slices, current_evaluation_interest, total_interest
       
    except Exception as e:
        print(e)
        return {'returncode': 1, 'message': 'Service Unavailable right now.'}, 503
    

    
    
    