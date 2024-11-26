import os
import django
import sys

PROJECT_ROOT = r"C:\django\hr_lines"

# Add the Django project directory to sys.path
sys.path.append(PROJECT_ROOT)

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_lines.settings')
django.setup()

# # Initialize Django


from ml_model.utils.data_loader import load_data
from ml_model.utils.data_process import *
from ml_model.models import BES, Schedule






def cce_to_database():
    df = load_data()
    # print('Before removing duplicates:', df['Vessel'].unique())
    # df = remove_duplicate_vessels(df)
    # print('After removing duplicates:', df['Vessel'].unique())
    for _, row in df.iterrows():
        x = row.to_dict()
        Schedule.objects.create(

                week_etb_cgp=x['Wk/ ETB CGP'],
                service=x['Service'],
                vessel=x['Vessel'],
                voyage_s=x['Voyage-S'],
                eta_cgp=x['ETA CGP'],
                etb_cgp=x['ETB CGP'],
                etd_cgp=x['ETD CGP'],
                voyage_n=x['Voyage-N'],
                eta_cmb=x['ETA CMB'],
                etb_cmb=x['ETB CMB'],
                etd_cmb=x['ETD CMB'],
                eta_cgp_2=x['ETA CGP-2'],
                etb_cgp_2=x['ETB CGP-2'],
                etd_cgp_2=x['ETD CGP-2']


        )
    print('Data imported to database successfully!')


def bes_to_database():
    df = load_data(path='C:\\Users\\omeoo\\Downloads\\bes-new.xlsx')
    for _, row in df.iterrows():
        x = row.to_dict()
        BES.objects.create(

                week_etb_cgp=x['Week'],
                service=x['Service'],
                vessel=x['Vessel'],
                voyage_s=x['Voyage-S'],
                eta_cgp=x['ETA CGP'],
                etb_cgp=x['ETB CGP'],
                etd_cgp=x['ETD CGP'],
                voyage_n=x['Voyage-N'],
                eta_sin=x['ETA SIN'],
                etb_sin=x['ETB SIN'],
                etd_sin=x['ETD SIN'],
                eta_pkg=x['ETA PKG'],
                etb_pkg=x['ETB PKG'],
                etd_pkg=x['ETD PKG'],
                eta_cgp_2=x['ETA CGP-2'],
                etb_cgp_2=x['ETB CGP-2'],
                etd_cgp_2=x['ETD CGP-2']


        )
    print('Data imported to database successfully!')


def bes_to_database_complete():
    df = load_data(path='C:\\Users\\omeoo\\Downloads\\bes-new-complete.xlsx')
    for _, row in df.iterrows():
        x = row.to_dict()
        BES_Complete.objects.create(

                operator=x['operator'],
                service=x['service'],
                vessel=x['vessel'],
                voyage_s=x['voyage_s'],
                eta_cgp=x['eta_cgp'],
                ata_cgp=x['ata_cgp'],

                etb_cgp=x['etb_cgp'],
                atb_cgp=x['atb_cgp'],
                etd_cgp=x['etd_cgp'],
                atd_cgp= x['atd_cgp'],
                voyage_n=x['voyage_n'],
                eta_sin=x['eta_sin'],
                ata_sin= x['ata_sin'],
                etb_sin=x['etb_sin'],
                atb_sin= x['atb_sin'],
                etd_sin=x['etd_sin'],
                atd_sin=x['atd_sin'],
                eta_pkg=x['eta_pkg'],
                ata_pkg=x['ata_pkg'],
                etb_pkg=x['etb_pkg'],
                atb_pkg=x['atb_pkg'],
                etd_pkg=x['etd_pkg'],
                atd_pkg=x['atd_pkg'],
                eta_cgp_2=x['eta_cgp_2'],
                ata_cgp_2=x['ata_cgp_2'],
                etb_cgp_2=x['etb_cgp_2'],
                atb_cgp_2=x['atb_cgp_2'],
                etd_cgp_2=x['etd_cgp_2'],
                atd_cgp_2=x['atd_cgp_2']


        )
    print('Data imported to database successfully!')




def cce_to_database_complete():
    df = load_data(path='C:\\Users\\omeoo\\Downloads\\cce_complete.xlsx')
    for _, row in df.iterrows():
        x = row.to_dict()
        CCE_Complete.objects.create(

                operator=x['operator'],
                service=x['service'],
                vessel=x['vessel'],
                voyage_s=x['voyage_s'],
                eta_cgp=x['eta_cgp'],
                ata_cgp=x['ata_cgp'],

                etb_cgp=x['etb_cgp'],
                atb_cgp=x['atb_cgp'],
                etd_cgp=x['etd_cgp'],
                atd_cgp= x['atd_cgp'],
                voyage_n=x['voyage_n'],
                eta_cmb=x['eta_cmb'],
                ata_cmb= x['ata_cmb'],
                etb_cmb=x['etb_cmb'],
                atb_cmb= x['atb_cmb'],
                etd_cmb=x['etd_cmb'],
                atd_cmb=x['atd_cmb'],
                
                eta_cgp_2=x['eta_cgp_2'],
                ata_cgp_2=x['ata_cgp_2'],
                etb_cgp_2=x['etb_cgp_2'],
                atb_cgp_2=x['atb_cgp_2'],
                etd_cgp_2=x['etd_cgp_2'],
                atd_cgp_2=x['atd_cgp_2']


        )
    print('Data imported to database successfully!')


if __name__ == '__main__':
    
    cce_to_database()   
    bes_to_database()
    print('Data imported to database successfully!')
    