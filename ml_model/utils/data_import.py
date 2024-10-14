import os
import django

# Set the settings module (replace 'your_project_name.settings' with your actual settings module path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_lines.settings')

# Initialize Django
django.setup()


from .data_loader import load_data
from ..models import Schedule






def import_to_database():
    df = load_data()
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


if __name__ == '__main__':
    import_to_database()