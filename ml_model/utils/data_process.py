import os
import sys

import django


PROJECT_ROOT = r"C:\django\hr_lines"

# Add the Django project directory to sys.path
sys.path.append(PROJECT_ROOT)

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_lines.settings')
django.setup()


from datetime import datetime, date
from math import e

import pandas as pd
from requests import get

from ml_model.models import *

# from .data_loader import load_data
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models.functions import Lower, Replace
from django.db.models import Value, F

from django.apps import apps



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


def month_dif(y, x):
    dif = relativedelta(y, x)
    # Calculate the total difference in months
    total_months = dif.years * 12 + dif.months
    # Add 1 if there are any remaining days
    if dif.days > 0:
        total_months += 1
    return total_months


def get_weeks(date):
    iso_calender = date.isocalendar()
    return iso_calender[1]


def get_rv(entry):
    rv = []
    if entry:
        diff = entry.ata_cgp_2 - entry.ata_cgp
        rv.append(diff.days)
        diff = entry.atb_cgp_2 - entry.atb_cgp
        rv.append(diff.days)
        diff = entry.atd_cgp_2 - entry.atd_cgp
        rv.append(diff.days)
    else :
        print('No data available')
    return rv

def get_sv(entry):
    sv = []
    if entry.service == 'CCE':
        diff = entry.ata_cmb - entry.ata_cgp  
        sv.append(diff.days)
        diff = entry.atb_cmb - entry.atb_cgp 
        sv.append(diff.days)
        diff = entry.atd_cmb - entry.atd_cgp 
        sv.append(diff.days)
    elif entry.service == 'BES':
        diff =  entry.ata_pkg - entry.ata_cgp
        sv.append(diff.days)
        diff = entry.atb_pkg - entry.atb_cgp
        sv.append(diff.days)
        diff = entry.atd_pkg - entry.atd_cgp
        sv.append(diff.days)
    return sv

def get_nv(entry):
    nv = []
    if entry.service == 'CCE':
        diff =  entry.ata_cgp_2 - entry.ata_cmb
        nv.append(diff.days)
        diff = entry.atb_cgp_2 - entry.atb_cmb
        nv.append(diff.days)
        diff = entry.atd_cgp_2 - entry.atd_cmb
        nv.append(diff.days)
    elif entry.service == 'BES':
        diff =  entry.ata_cgp_2 - entry.ata_pkg
        nv.append(diff.days)
        diff = entry.atb_cgp_2 - entry.atb_pkg
        nv.append(diff.days)
        diff = entry.atd_cgp_2 - entry.atd_pkg
        nv.append(diff.days)
    return nv


def get_berthing_delay(entry):
    pass


def get_vessel_code(entry):
    vessel = entry.vessel
    return vessel.split('"')[1]


def get_vessel_only(entry):
    vessel = entry.vessel
    return vessel.split('"')[0]

def get_voyage_s_with_code(entry):
    return get_vessel_code(entry) + get_voyage_s(entry)


def get_voyage_n_with_code(entry):
    return get_vessel_code(entry) + get_voyage_n(entry)


def get_terminal(entry):
    pass









def generate_schedule(service,months):

    print(type(months))

    if service == 'BES':
        bes_rv = BES_RV.objects.all().first()

        available_vessels = list(Vessel.objects.filter(service='BES').values_list('name', flat=True).distinct())

        for vessel in available_vessels:

            keep_going = BES.objects.exists()

            initial_info = None

            if BES.objects.exists():
                initial_info = (
                                BES.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )

                
            
            else:
                print('No data available')
            
            while keep_going:

                last_info = (
                                BES.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )
                
                
                duplicate_entry = BES.objects.filter(
                week_etb_cgp=get_weeks(last_info.eta_cgp_2) ,
                service=last_info.service,
                vessel=last_info.vessel,
                voyage_s=get_voyage_s(last_info),
            
                ).exists()

                if month_dif(last_info.eta_cgp,initial_info.eta_cgp) <months and not duplicate_entry:

                    print(f'date1:{last_info.eta_cgp} - date2:{initial_info.eta_cgp} - dif:{month_dif(last_info.eta_cgp,initial_info.eta_cgp)}')

                    

                    BES.objects.create(
                    week_etb_cgp=get_weeks(last_info.eta_cgp_2),
                    service=last_info.service,
                    vessel=last_info.vessel,
                    voyage_s=get_voyage_s(last_info),
                    eta_cgp=last_info.eta_cgp_2,
                    etb_cgp=last_info.etb_cgp_2,
                    etd_cgp=last_info.etd_cgp_2,
                    voyage_n=get_voyage_n(last_info),

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),

                    eta_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    etb_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    etd_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp)
                    )
                else:
                    keep_going = False
    else:
        
        cce_rv = CCE_RV.objects.all().first()

        available_vessels = list(Vessel.objects.filter(service='CCE').values_list('name', flat=True).distinct())

        for vessel in available_vessels:

            keep_going = Schedule.objects.exists()

            initial_info = None

            if Schedule.objects.exists():
                initial_info = (
                                Schedule.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )

                
            
            else:
                print('No data available')
            
            while keep_going:

                last_info = (
                                Schedule.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )
                print(vessel)
                print(last_info)
                
                duplicate_entry = Schedule.objects.filter(
                week_etb_cgp=get_weeks(last_info.eta_cgp_2) ,
                service=last_info.service,
                vessel=last_info.vessel,
                voyage_s=get_voyage_s(last_info),
            
                ).exists()
                print(initial_info.eta_cgp)

                if month_dif(last_info.eta_cgp,initial_info.eta_cgp) < months and not duplicate_entry:

                    print("debug")
                    Schedule.objects.create(
                    week_etb_cgp=get_weeks(last_info.eta_cgp_2),
                    service=last_info.service,
                    vessel=last_info.vessel,
                    voyage_s=get_voyage_s(last_info),
                    eta_cgp=last_info.eta_cgp_2,
                    etb_cgp=last_info.etb_cgp_2,
                    etd_cgp=last_info.etd_cgp_2,
                    voyage_n=get_voyage_n(last_info),
                    eta_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                    etb_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                    etd_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),

                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp)                   
                    )
                else:
                    keep_going = False


                 

            



def set_voyage_complete_before(model_name, month, year):
    # Define the cutoff date as the first day of the specified month and year
    cutoff_date = date(year, month, 1)
    
    # Get the model class based on the model name
    model = apps.get_model('ml_model', model_name)
    
    # Filter records where the etd_cgp date is before the cutoff date
    records_to_update = model.objects.filter(eta_cgp__lt=cutoff_date)
    
    # Update the voyage_complete field to True for the filtered records
    records_to_update.update(voyage_complete=True)

# Example usage



def del_bes_by_vessel_name(entry):
    vessel_name = entry.name
    BES.objects.annotate(
                            vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value('')))
                        ).filter(
                            vessel_no_space=vessel_name.replace(" ", "").lower(),
                            voyage_complete=False
                        ).delete()


def del_cce_by_vessel_name(entry):
    vessel_name = entry.name
    Schedule.objects.annotate(
                            vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value('')))
                        ).filter(
                            vessel_no_space=vessel_name.replace(" ", "").lower(),
                            voyage_complete=False
                        ).delete()


def del_bes(entry):
    vessel_name = entry.vessel
    BES.objects.annotate(
                            vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value('')))
                        ).filter(
                            vessel_no_space=vessel_name.replace(" ", "").lower(),
                            voyage_complete=False
                        ).delete()

def del_cce(entry):


    vessel_name = entry.vessel
    Schedule.objects.annotate(
                            vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value('')))
                        ).filter(
                            vessel_no_space=vessel_name.replace(" ", "").lower(),
                            voyage_complete=False
                        ).delete()


def generate_bes_partial(entry):

    bes_rv = BES_RV.objects.all().first()

    vessel = entry.vessel
    print('inside generate_bes_partial')
    last_info = BES.objects.order_by('-eta_cgp').first()
    initial_info = (
                                BES.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                    )

    months = month_dif(last_info.eta_cgp,initial_info.eta_cgp)
    print('months:',months)

    keep_going = True

    while keep_going:

                last_info = (
                                BES.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )
                
                print('im inside while loop')
                duplicate_entry = BES.objects.filter(

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin)

               
                

            
                ).exists()
                print('after duplicate check')

                if month_dif(last_info.eta_cgp,initial_info.eta_cgp) <months :

                    print(f'date1:{last_info.eta_cgp} - date2:{initial_info.eta_cgp} - dif:{month_dif(last_info.eta_cgp,initial_info.eta_cgp)}')

                    

                    BES.objects.create(
                    week_etb_cgp=get_weeks(last_info.eta_cgp_2),
                    service=last_info.service,
                    vessel=last_info.vessel,
                    voyage_s=get_voyage_s(last_info),
                    eta_cgp=last_info.eta_cgp_2,
                    etb_cgp=last_info.etb_cgp_2,
                    etd_cgp=last_info.etd_cgp_2,
                    voyage_n=get_voyage_n(last_info),

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),

                    eta_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    etb_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    etd_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp)
                    )
                else:
                    keep_going = False




#Need Testing
def generate_cce_partial(entry):
        
        cce_rv = CCE_RV.objects.all().first()
    
        vessel = entry.vessel
    
        last_info = Schedule.objects.order_by('-eta_cgp').first()
        initial_info = (
                                    Schedule.objects
                                    .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                    .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                    .order_by('-id')
                                    .first()
                        )
    
        months = month_dif(last_info.eta_cgp,initial_info.eta_cgp)
    
        keep_going = True
    
        while keep_going:
    
                    last_info = (
                                    Schedule.objects
                                    .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                    .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                    .order_by('-id')
                                    .first()
                                )
                    
                    
                    # duplicate_entry = Schedule.objects.filter(
                    # week_etb_cgp=get_weeks(last_info.eta_cgp_2) ,
                    # service=last_info.service,
                    # vessel=last_info.vessel,
                    # voyage_s=get_voyage_s(last_info),
                
                    # ).exists()
    
                    if month_dif(last_info.eta_cgp,initial_info.eta_cgp) <months :
    
                        print(f'date1:{last_info.eta_cgp} - date2:{initial_info.eta_cgp} - dif:{month_dif(last_info.eta_cgp,initial_info.eta_cgp)}')
    
                        
    
                        Schedule.objects.create(
                        week_etb_cgp=get_weeks(last_info.eta_cgp_2),
                        service=last_info.service,
                        vessel=last_info.vessel,
                        voyage_s=get_voyage_s(last_info),
                        eta_cgp=last_info.eta_cgp_2,
                        etb_cgp=last_info.etb_cgp_2,
                        etd_cgp=last_info.etd_cgp_2,
                        voyage_n=get_voyage_n(last_info),
    
                        eta_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                        etb_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                        etd_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                        eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                        etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                        etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp)                   
                        )
                    else:
                        keep_going = False








def bes_to_cce(entry):
    cce_rv = CCE_RV.objects.all().first()
    if entry :
        Schedule.objects.create(
            week_etb_cgp=entry.week_etb_cgp,
            service='CCE',
            vessel=entry.vessel,
            voyage_s=get_voyage_s(entry),
            eta_cgp=entry.eta_cgp,
            etb_cgp=entry.etb_cgp,
            etd_cgp=entry.etd_cgp,
            voyage_n=get_voyage_n(entry),
            eta_cmb=entry.etd_cgp + timedelta(days=cce_rv.cgp_to_cmb),
            etb_cmb=entry.etd_cgp + timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb),
            etd_cmb=entry.etd_cgp + timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
            eta_cgp_2=entry.etd_cgp + timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
            etb_cgp_2=entry.etd_cgp + timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
            etd_cgp_2=entry.etd_cgp + timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp)
        )

    else:
        print('No data available')
    



    





def cce_to_bes(entry):
    bes_rv = BES_RV.objects.all().first()
    if entry:
        BES.objects.create(
            week_etb_cgp=entry.week_etb_cgp,
            service='BES',
            vessel=entry.vessel,
            voyage_s=get_voyage_s(entry),
            eta_cgp=entry.eta_cgp,
            etb_cgp=entry.etb_cgp,
            etd_cgp=entry.etd_cgp,
            voyage_n=get_voyage_n(entry),
            eta_sin=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin),
            etb_sin=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
            etd_sin=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
            eta_pkg=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
            etb_pkg=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
            etd_pkg=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
            eta_cgp_2=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
            etb_cgp_2=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
            etd_cgp_2=entry.etd_cgp + timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp)
        )
    else:
        print('No data available')








def generate_schedule_complete(service,months):

    print(type(months))

    if service == 'BES':
        bes_rv = BES_RV.objects.all().first()

        available_vessels = list(Vessel.objects.filter(service='BES').values_list('name', flat=True).distinct())

        for vessel in available_vessels:

            keep_going = BES_Complete.objects.exists()

            initial_info = None

            if BES_Complete.objects.exists():
                initial_info = (
                                BES_Complete.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )

                
            
            else:
                print('No data available')
            
            while keep_going:

                last_info = (
                                BES_Complete.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )
                
                
                duplicate_entry = BES_Complete.objects.filter(
                week_cgp=get_weeks(last_info.eta_cgp_2) ,
                service=last_info.service,
                vessel=last_info.vessel,
                voyage_s=get_voyage_s(last_info),
            
                ).exists()

                if month_dif(last_info.eta_cgp,initial_info.eta_cgp) <months and not duplicate_entry:

                    print(f'date1:{last_info.eta_cgp} - date2:{initial_info.eta_cgp} - dif:{month_dif(last_info.eta_cgp,initial_info.eta_cgp)}')

                    
                    rv = get_rv(last_info)
                    sb_v = get_sv(last_info)
                    nb_v = get_nv(last_info)

                    

                    BES_Complete.objects.create(
                    operator = last_info.operator,
                    service = last_info.service,
                    rv1 = rv[0],
                    sb_v1 = sb_v[0],
                    nb_v1 = nb_v[0],
                    rv2 = rv[1],
                    sb_v2 = sb_v[1],
                    nb_v2 = nb_v[1],    
                    rv3 = rv[2],
                    sb_v3 = sb_v[2],
                    nb_v3 = nb_v[2],

                    week_cgp = get_weeks(last_info.eta_cgp_2),
                    only_vessel_name = get_vessel_only(last_info),
                    vessel_code = get_vessel_code(last_info),
                    vessel = last_info.vessel,
                    voyage_s = get_voyage_s(last_info), 
                    voyage_s_with_code = get_voyage_s_with_code(last_info),
                    #add terminal_cgp
                    eta_cgp = last_info.eta_cgp_2,
                    ata_cgp = last_info.eta_cgp_2,
                    etb_cgp = last_info.etb_cgp_2,
                    atb_cgp = last_info.etb_cgp_2,
                    etd_cgp = last_info.etd_cgp_2,
                    atd_cgp = last_info.etd_cgp_2,
                    #add berthing_delay_cgp

                    week_sin = get_weeks(last_info.eta_cgp_2 +timedelta(days=bes_rv.cgp_to_sin)),
                    voyage_n = get_voyage_n(last_info),
                    voyage_n_with_code = get_voyage_n_with_code(last_info),
                    #add terminal_sin

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    ata_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    atb_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
                    atd_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
                    #add berthing_delay_sin
                    week_pkg = get_weeks(last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg)),
                    #add terminal_pkg
                    eta_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    ata_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    etb_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    atb_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    etd_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    atd_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    #add berthing_delay_pkg
                    week_cgp_2 = get_weeks(last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp)),
                    #add terminal_cgp_2
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    ata_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    atb_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp),
                    atd_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp)
                    )
                    #add berth_delay_cgp_2
                else:
                    keep_going = False
    else:
        
        cce_rv = CCE_RV.objects.all().first()

        available_vessels = list(Vessel.objects.filter(service='CCE').values_list('name', flat=True).distinct())

        for vessel in available_vessels:

            keep_going = CCE_Complete.objects.exists()

            initial_info = None

            if CCE_Complete.objects.exists():
                initial_info = (
                                CCE_Complete.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )

                
            
            else:
                print('No data available')
            
            while keep_going:

                last_info = (
                                CCE_Complete.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )
                print(vessel)
                print(last_info)
                
                duplicate_entry = CCE_Complete.objects.filter(
                week_cgp=get_weeks(last_info.eta_cgp_2) ,
                service=last_info.service,
                vessel=last_info.vessel,
                voyage_s=get_voyage_s(last_info),
            
                ).exists()
                print(initial_info.eta_cgp)

                if month_dif(last_info.eta_cgp,initial_info.eta_cgp) < months and not duplicate_entry:

                    rv = get_rv(last_info)
                    sb_v = get_sv(last_info)
                    nb_v = get_nv(last_info)

                    print("debug")
                    CCE_Complete.objects.create(
                    operator = last_info.operator,
                    service = last_info.service,
                    rv1 = rv[0],
                    sb_v1 = sb_v[0],
                    nb_v1 = nb_v[0],
                    rv2 = rv[1],
                    sb_v2 = sb_v[1],
                    nb_v2 = nb_v[1],
                    rv3 = rv[2],
                    sb_v3 = sb_v[2],
                    nb_v3 = nb_v[2],
                    week_cgp=get_weeks(last_info.eta_cgp_2),
                    only_vessel_name=get_vessel_only(last_info),
                    vessel_code=get_vessel_code(last_info),
                    
                    vessel=last_info.vessel,
                    voyage_s=get_voyage_s(last_info),
                    voyage_s_with_code = get_voyage_s_with_code(last_info),
                    #add terminal_cgp
                    eta_cgp=last_info.eta_cgp_2,
                    ata_cgp=last_info.eta_cgp_2,
                    etb_cgp=last_info.etb_cgp_2,
                    atb_cgp=last_info.etb_cgp_2,
                    etd_cgp=last_info.etd_cgp_2,
                    atd_cgp=last_info.etd_cgp_2,
                    #add berthing_delay_cgp
                    week_cmb=get_weeks(last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb)),

                    voyage_n=get_voyage_n(last_info),
                    voyage_n_with_code = get_voyage_n_with_code(last_info), 
                    #add terminal_cmb
                    eta_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                    ata_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                    etb_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                    atb_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                    etd_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                    atd_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                    #add berthing_delay_cmb

                    week_cgp_2=get_weeks(last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp)),
                    #add terminal_cgp_2
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                    ata_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                    atb_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp),
                    atd_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp),
                    #add berth_delay_cgp_2                   
                    )
                else:
                    keep_going = False




def del_bes_complete(entry):
    vessel_name = entry.vessel
    BES_Complete.objects.annotate(
                            vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value('')))
                        ).filter(
                            vessel_no_space=vessel_name.replace(" ", "").lower(),
                            voyage_complete=False
                        ).delete()




def del_cce_complete(entry):


    vessel_name = entry.vessel
    CCE_Complete.objects.annotate(
                            vessel_no_space=Lower(Replace(F('vessel'), Value(' '), Value('')))
                        ).filter(
                            vessel_no_space=vessel_name.replace(" ", "").lower(),
                            voyage_complete=False
                        ).delete()



def bes_to_cce_complete(last_info):
    cce_rv = CCE_RV.objects.all().first()
    if last_info :
        rv = get_rv(last_info)
        sb_v = get_sv(last_info)
        nb_v = get_nv(last_info)
        CCE_Complete.objects.create(
                    operator = last_info.operator,
                    service = 'CCE',
                    rv1 = rv[0],
                    sb_v1 = sb_v[0],
                    nb_v1 = nb_v[0],
                    rv2 = rv[1],
                    sb_v2 = sb_v[1],
                    nb_v2 = nb_v[1],
                    rv3 = rv[2],
                    sb_v3 = sb_v[2],
                    nb_v3 = nb_v[2],
                    week_cgp=get_weeks(last_info.eta_cgp_2),
                    only_vessel_name=get_vessel_only(last_info),
                    vessel_code=get_vessel_code(last_info),
                    
                    vessel=last_info.vessel,
                    voyage_s=get_voyage_s(last_info),
                    voyage_s_with_code = get_voyage_s_with_code(last_info),
                    #add terminal_cgp
                    eta_cgp=last_info.eta_cgp_2,
                    ata_cgp=last_info.eta_cgp_2,
                    etb_cgp=last_info.etb_cgp_2,
                    atb_cgp=last_info.etb_cgp_2,
                    etd_cgp=last_info.etd_cgp_2,
                    atd_cgp=last_info.etd_cgp_2,
                    #add berthing_delay_cgp
                    week_cmb=get_weeks(last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb)),

                    voyage_n=get_voyage_n(last_info),
                    voyage_n_with_code = get_voyage_n_with_code(last_info), 
                    #add terminal_cmb
                    eta_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                    ata_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                    etb_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                    atb_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                    etd_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                    atd_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                    #add berthing_delay_cmb

                    week_cgp_2=get_weeks(last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp)),
                    #add terminal_cgp_2
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                    ata_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                    atb_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp),
                    atd_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp),
                    #add berth_delay_cgp_2                   
                    )

    else:
        print('No data available')


def cce_to_bes_complete(last_info):
    bes_rv = BES_RV.objects.all().first()
    if last_info :
        rv = get_rv(last_info)
        sb_v = get_sv(last_info)
        nb_v = get_nv(last_info)
        BES_Complete.objects.create(
                    operator = last_info.operator,
                    service = 'BES',
                    rv1 = rv[0],
                    sb_v1 = sb_v[0],
                    nb_v1 = nb_v[0],
                    rv2 = rv[1],
                    sb_v2 = sb_v[1],
                    nb_v2 = nb_v[1],    
                    rv3 = rv[2],
                    sb_v3 = sb_v[2],
                    nb_v3 = nb_v[2],

                    week_cgp = get_weeks(last_info.eta_cgp_2),
                    only_vessel_name = get_vessel_only(last_info),
                    vessel_code = get_vessel_code(last_info),
                    vessel = last_info.vessel,
                    voyage_s = get_voyage_s(last_info), 
                    voyage_s_with_code = get_voyage_s_with_code(last_info),
                    #add terminal_cgp
                    eta_cgp = last_info.eta_cgp_2,
                    ata_cgp = last_info.eta_cgp_2,
                    etb_cgp = last_info.etb_cgp_2,
                    atb_cgp = last_info.etb_cgp_2,
                    etd_cgp = last_info.etd_cgp_2,
                    atd_cgp = last_info.etd_cgp_2,
                    #add berthing_delay_cgp

                    week_sin = get_weeks(last_info.eta_cgp_2 +timedelta(days=bes_rv.cgp_to_sin)),
                    voyage_n = get_voyage_n(last_info),
                    voyage_n_with_code = get_voyage_n_with_code(last_info),
                    #add terminal_sin

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    ata_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    atb_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
                    atd_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
                    #add berthing_delay_sin
                    week_pkg = get_weeks(last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg)),
                    #add terminal_pkg
                    eta_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    ata_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    etb_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    atb_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    etd_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    atd_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    #add berthing_delay_pkg
                    week_cgp_2 = get_weeks(last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp)),
                    #add terminal_cgp_2
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    ata_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    atb_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp),
                    atd_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp)
                    )

    else:
        print('No data available')



def generate_bes_partial_complete(entry):

    bes_rv = BES_RV.objects.all().first()

    vessel = entry.vessel
    print('inside generate_bes_partial')
    last_info = BES_Complete.objects.order_by('-eta_cgp').first()
    initial_info = (
                                BES_Complete.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                    )

    months = month_dif(last_info.eta_cgp,initial_info.eta_cgp)
    print('months:',months)

    keep_going = True

    while keep_going:

                last_info = (
                                BES_Complete.objects
                                .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                .order_by('-id')
                                .first()
                            )
                
                print('im inside while loop')
                duplicate_entry = BES_Complete.objects.filter(

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin)

               
                

            
                ).exists()
                print('after duplicate check')

                if month_dif(last_info.eta_cgp,initial_info.eta_cgp) <months :

                    print(f'date1:{last_info.eta_cgp} - date2:{initial_info.eta_cgp} - dif:{month_dif(last_info.eta_cgp,initial_info.eta_cgp)}')

                    rv = get_rv(last_info)
                    sb_v = get_sv(last_info)
                    nb_v = get_nv(last_info)

                    
                    BES_Complete.objects.create(
                    operator = last_info.operator,
                    service = last_info.service,
                    rv1 = rv[0],
                    sb_v1 = sb_v[0],
                    nb_v1 = nb_v[0],
                    rv2 = rv[1],
                    sb_v2 = sb_v[1],
                    nb_v2 = nb_v[1],    
                    rv3 = rv[2],
                    sb_v3 = sb_v[2],
                    nb_v3 = nb_v[2],

                    week_cgp = get_weeks(last_info.eta_cgp_2),
                    only_vessel_name = get_vessel_only(last_info),
                    vessel_code = get_vessel_code(last_info),
                    vessel = last_info.vessel,
                    voyage_s = get_voyage_s(last_info), 
                    voyage_s_with_code = get_voyage_s_with_code(last_info),
                    #add terminal_cgp
                    eta_cgp = last_info.eta_cgp_2,
                    ata_cgp = last_info.eta_cgp_2,
                    etb_cgp = last_info.etb_cgp_2,
                    atb_cgp = last_info.etb_cgp_2,
                    etd_cgp = last_info.etd_cgp_2,
                    atd_cgp = last_info.etd_cgp_2,
                    #add berthing_delay_cgp

                    week_sin = get_weeks(last_info.eta_cgp_2 +timedelta(days=bes_rv.cgp_to_sin)),
                    voyage_n = get_voyage_n(last_info),
                    voyage_n_with_code = get_voyage_n_with_code(last_info),
                    #add terminal_sin

                    eta_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    ata_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin),
                    etb_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    atb_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin),
                    etd_sin=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
                    atd_sin = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin),
                    #add berthing_delay_sin
                    week_pkg = get_weeks(last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg)),
                    #add terminal_pkg
                    eta_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    ata_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg),
                    etb_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    atb_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg),
                    etd_pkg=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    atd_pkg = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg),
                    #add berthing_delay_pkg
                    week_cgp_2 = get_weeks(last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp)),
                    #add terminal_cgp_2
                    eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    ata_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp),
                    etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    atb_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp),
                    etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp),
                    atd_cgp_2 = last_info.etd_cgp_2 +timedelta(days=bes_rv.cgp_to_sin + bes_rv.eta_to_etb_sin + bes_rv.etb_to_etd_sin + bes_rv.sin_to_pkg + bes_rv.eta_to_etb_pkg + bes_rv.etb_to_etd_pkg + bes_rv.pkg_to_cgp + bes_rv.eta_to_etb_cgp + bes_rv.etb_to_etd_cgp)
                    )
                else:
                    keep_going = False




#Need Testing
def generate_cce_partial_complete(entry):
        
        cce_rv = CCE_RV.objects.all().first()
    
        vessel = entry.vessel
    
        last_info = CCE_Complete.objects.order_by('-eta_cgp').first()
        initial_info = (
                                    CCE_Complete.objects
                                    .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                    .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                    .order_by('-id')
                                    .first()
                        )
    
        months = month_dif(last_info.eta_cgp,initial_info.eta_cgp)
    
        keep_going = True
    
        while keep_going:
    
                    last_info = (
                                    CCE_Complete.objects
                                    .annotate(vessel_no_space=Lower(Replace('vessel', Value(' '), Value(''))))
                                    .filter(vessel_no_space=vessel.replace(" ", "").lower())
                                    .order_by('-id')
                                    .first()
                                )
                    
                    
                    # duplicate_entry = Schedule.objects.filter(
                    # week_etb_cgp=get_weeks(last_info.eta_cgp_2) ,
                    # service=last_info.service,
                    # vessel=last_info.vessel,
                    # voyage_s=get_voyage_s(last_info),
                
                    # ).exists()
    
                    if month_dif(last_info.eta_cgp,initial_info.eta_cgp) <months :
    
                        print(f'date1:{last_info.eta_cgp} - date2:{initial_info.eta_cgp} - dif:{month_dif(last_info.eta_cgp,initial_info.eta_cgp)}')
    
                        rv = get_rv(last_info)
                        sb_v = get_sv(last_info)
                        nb_v = get_nv(last_info)


    
                        CCE_Complete.objects.create(
                        operator = last_info.operator,
                        service = last_info.service,
                        rv1 = rv[0],
                        sb_v1 = sb_v[0],
                        nb_v1 = nb_v[0],
                        rv2 = rv[1],
                        sb_v2 = sb_v[1],
                        nb_v2 = nb_v[1],
                        rv3 = rv[2],
                        sb_v3 = sb_v[2],
                        nb_v3 = nb_v[2],
                        week_cgp=get_weeks(last_info.eta_cgp_2),
                        only_vessel_name=get_vessel_only(last_info),
                        vessel_code=get_vessel_code(last_info),
                        
                        vessel=last_info.vessel,
                        voyage_s=get_voyage_s(last_info),
                        voyage_s_with_code = get_voyage_s_with_code(last_info),
                        #add terminal_cgp
                        eta_cgp=last_info.eta_cgp_2,
                        ata_cgp=last_info.eta_cgp_2,
                        etb_cgp=last_info.etb_cgp_2,
                        atb_cgp=last_info.etb_cgp_2,
                        etd_cgp=last_info.etd_cgp_2,
                        atd_cgp=last_info.etd_cgp_2,
                        #add berthing_delay_cgp
                        week_cmb=get_weeks(last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb)),

                        voyage_n=get_voyage_n(last_info),
                        voyage_n_with_code = get_voyage_n_with_code(last_info), 
                        #add terminal_cmb
                        eta_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                        ata_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb),
                        etb_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                        atb_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb+ cce_rv.eta_to_etb_cmb),
                        etd_cmb=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                        atd_cmb = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb),
                        #add berthing_delay_cmb

                        week_cgp_2=get_weeks(last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp)),
                        #add terminal_cgp_2
                        eta_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                        ata_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp),
                        etb_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                        atb_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp),
                        etd_cgp_2=last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp),
                        atd_cgp_2 = last_info.etd_cgp_2 +timedelta(days=cce_rv.cgp_to_cmb + cce_rv.eta_to_etb_cmb + cce_rv.etb_to_etd_cmb + cce_rv.cmb_to_cgp + cce_rv.eta_to_etb_cgp + cce_rv.etb_to_etd_cgp),
                        #add berth_delay_cgp_2                   
                        )
                    else:
                        keep_going = False






            





if __name__ == '__main__':
    
    set_voyage_complete_before('Schedule', 9, 2025)  # Set voyage_complete to True for records in the Schedule model before June 2026           
    print('success')


                                
