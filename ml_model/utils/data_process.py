from datetime import datetime, date

import pandas as pd

from ml_model.models import Schedule

from .data_loader import load_data
from datetime import timedelta

from ml_model.models import Predicted_Schedule

pd.options.mode.chained_assignment = None  # default='warn'





def remove_duplicate_vessels(df):
    """Pre-processing to remove duplicate vessel name"""
    for i in range(len(df['Vessel'])):
        if df['Vessel'][i] == 'SAHARE  "MSAH"' or df['Vessel'][i] == 'HR SAHARE "MSAH"' or df['Vessel'][i] == 'HR SAHARE  "MSAH"' or df['Vessel'][i] == ' HR SAHARE  "MSAH"':
            df['Vessel'][i] = 'HR SAHARE "MSAH"'
        elif df['Vessel'][i] == 'SARERA  "MSAR"' or df['Vessel'][i] == 'HR SARERA "MSAR"' or df['Vessel'][i] == 'HR SARERA  "MSAR"'  :
            df['Vessel'][i] ='HR SARERA "MSAR"'
        elif df['Vessel'][i] == 'HR FARHA "MHRF"' or df['Vessel'][i] == 'HR FARHA  "MHRF"' :
            df['Vessel'][i] ='HR FARHA "MHRF"'
        else:
            df['Vessel'][i] = df['Vessel'][i]
    

    return df



def remove_backslashes(vessel_list):
    return [vessel.replace('\\', '') for vessel in vessel_list]


def get_last_info(df, vessel_name) :
    return df[df['Vessel'] == vessel_name].iloc[-1]


def format_timestamp(timestamp):
    # Ensure the input is a pandas Timestamp
    if not isinstance(timestamp, (date,datetime)):
        raise ValueError("Input must be a pandas Timestamp")
    
    # Format the timestamp
    return timestamp.strftime('%a-%d/%m')



    


def get_voyage_s(last_info):
    


    previous_voyage = last_info.voyage_s

    integer_part_str = ''.join([char for char in previous_voyage if char.isdigit()])
    integer_part_int = int(integer_part_str)

    next_voyage = integer_part_int + 1
    number_of_zeros = 4 - len(str(next_voyage))
    return '0' * number_of_zeros + str(next_voyage) + 'S'




def get_voyage_n(last_info):
    


    previous_voyage = last_info.voyage_n

    integer_part_str = ''.join([char for char in previous_voyage if char.isdigit()])
    integer_part_int = int(integer_part_str)

    next_voyage = integer_part_int + 1
    number_of_zeros = 4 - len(str(next_voyage))
    return '0' * number_of_zeros + str(next_voyage) + 'N'




def get_eta_cmb(last_info):

    n = 5 # use probabilistic/ml model later
    last_date = last_info.etd_cgp_2
    return last_date + timedelta(days=n)



def get_etb_cmb(last_info):

    n = 1 # use probabilistic/ml model later
    last_date = get_eta_cmb(last_info)
        
        
        
    return last_date + timedelta(days=n)
    




def get_etd_cmb(last_info):

    n = 1 # use probabilistic/ml model later
    last_date = get_etb_cmb(last_info)
    return last_date + timedelta(days=n)
    


def get_eta_cgp(last_info):

    n = 5 # use probabilistic/ml model later
    last_date = get_etd_cmb(last_info)
    return last_date + timedelta(days=n)


def get_etb_cgp(last_info):

    n = 1 # use probabilistic/ml model later
    last_date = get_eta_cgp(last_info)
    return last_date + timedelta(days=n)
    


def get_etd_cgp(last_info):

    n = 3 # use probabilistic/ml model later
    last_date = get_etb_cgp(last_info)
    return last_date + timedelta(days=n)
    




def generate_samples(available_vessels):
        
    # samples = []

    for vessel in available_vessels :
        last_info = Schedule.objects.filter(vessel=vessel).order_by('-id').first()
        
        
        new_record = {  'ID' : last_info.id ,
                        'Wk/ ETB CGP' : int(last_info.week_etb_cgp) + 1,
                        'Service': last_info.service,
                        'Vessel' : last_info.vessel,
                        'Voyage-S':	get_voyage_s(last_info),
                        'ETA CGP':	format_timestamp(last_info.eta_cgp_2),
                        'ETB CGP':	format_timestamp(last_info.etb_cgp_2),
                        'ETD CGP':	format_timestamp(last_info.etd_cgp_2),
                        'Voyage-N':	get_voyage_n(last_info),
                        'ETA CMB' :	format_timestamp(get_eta_cmb(last_info)),
                        'ETB CMB' :	format_timestamp(get_etb_cmb(last_info)),
                        'ETD CMB' :	format_timestamp(get_etd_cmb(last_info)),
                        'ETA CGP-2' : format_timestamp(get_eta_cgp(last_info)),
                        'ETB CGP-2' : format_timestamp(get_etb_cgp(last_info)),	
                        'ETD CGP-2': format_timestamp(get_etd_cgp(last_info))}
        
        # samples.append(new_record)

        # Check if a duplicate entry exists in the database
        duplicate_entry = Predicted_Schedule.objects.filter(
            week_etb_cgp=int(last_info.week_etb_cgp) + 1,
            service=last_info.service,
            vessel=last_info.vessel,
            voyage_s=get_voyage_s(last_info),
            
        ).exists()

        if not duplicate_entry:
            Predicted_Schedule.objects.create(
            week_etb_cgp=int(last_info.week_etb_cgp) + 1,
            service=last_info.service,
            vessel=last_info.vessel,
            voyage_s=get_voyage_s(last_info),
            eta_cgp=last_info.eta_cgp_2,
            etb_cgp=last_info.etb_cgp_2,
            etd_cgp=last_info.etd_cgp_2,
            voyage_n=get_voyage_n(last_info),
            eta_cmb=get_eta_cmb(last_info),
            etb_cmb=get_etb_cmb(last_info),
            etd_cmb=get_etd_cmb(last_info),
            eta_cgp_2=get_eta_cgp(last_info),
            etb_cgp_2=get_etb_cgp(last_info),
            etd_cgp_2=get_etd_cgp(last_info)
            )


        


    
    
    # return samples


# def main() :
#     df = load_data()
#     df = remove_duplicate_vessels(df)
#     available_vessels = ['HR SAHARE "MSAH"']
#     samples = generate_samples(df,available_vessels)
#     print(samples)



# if __name__ == '__main__':
#     main()


                                
