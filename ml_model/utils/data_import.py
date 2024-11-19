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


if __name__ == '__main__':
    
    cce_to_database()   
    bes_to_database()
    print('Data imported to database successfully!')
    