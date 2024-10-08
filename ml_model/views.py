import json
from django.shortcuts import render

# Create your views here.

# views.py
import pandas as pd
import joblib
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from .utils.data_loader import *

from .utils.data_process import *

from django.http import JsonResponse
from django.template.loader import render_to_string



# Load the model (assumes it's saved in the same directory)
model = joblib.load('ml_model/model.pkl')

# - Time(B>D)(CGP)
# - Vessel
# - Voyage
# - Wk/ ETB CGP


def home(request):
    return HttpResponse('Hello World')


# def predict(request):
#     week = request.GET.get('week')
#     vessel = request.GET.get('vessel')
#     voyage = request.GET.get('voyage')
#     time_cgp = request.GET.get('time_cgp')

#     # Log the received inputs
#     print(f"Received inputs: week={week}, vessel={vessel}, voyage={voyage}, time_cgp={time_cgp}")

#     # Convert inputs to the appropriate types
#     try:
#         week = float(week)
#         vessel = float(vessel)
#         voyage = float(voyage)
#         time_cgp = float(time_cgp)
#     except ValueError:
#         return JsonResponse({'error': 'Invalid input types'}, status=400)

#     # Create a DataFrame with feature names (as used in training)
#     input_data = pd.DataFrame({
#         'Wk/ ETB CGP': [week],
#         'Vessel': [vessel],
#         'Voyage': [voyage],
#         'Time(B>D)(CGP)': [time_cgp]
#     })

#     # Make predictions using the DataFrame
#     prediction = model.predict(input_data)
#     return JsonResponse({'prediction': prediction[0]})





def predict_etb(request):
    if request.method == 'POST':
        # Get form inputs
        week = request.POST.get('week')
        vessel = request.POST.get('vessel')
        voyage = request.POST.get('voyage')
        etb_cgp = request.POST.get('etb_cgp')
        etd_cgp = request.POST.get('etd_cgp')

        # Convert inputs to appropriate types
        try:
            week = int(week)
            etb_cgp_date = datetime.strptime(etb_cgp, '%Y-%m-%d')
            etd_cgp_date = datetime.strptime(etd_cgp, '%Y-%m-%d')

            # Calculate the difference in days between ETD(CGP) and ETB(CGP)
            day_difference = (etd_cgp_date - etb_cgp_date).days
            print(f'etb_cgp_date : {etb_cgp_date}')
            print(f'etd_cgp_date : {etd_cgp_date}')
            print(f'day_difference : {day_difference}')
        except ValueError:
            return render(request, 'ml_model/predict_form.html', {'error': 'Invalid input types'})

        # Create a DataFrame for the model prediction
      
        input_data = pd.DataFrame({
        'Wk/ ETB CGP': [week],
        'Vessel': [vessel],
        'Voyage': [voyage],
        'Time(B>D)(CGP)': [day_difference]
    })

        # Make the prediction (this assumes the model is already loaded)
        model_output = model.predict(input_data)

        # Convert model output to an integer (days to add to ETD(CGP))
        predicted_days = int(model_output[0])
        print(f'Predicted days : {predicted_days}')

        # Add the predicted days to ETD(CGP) to calculate ETB(CMB)
        etb_cmb_date = etd_cgp_date + timedelta(days=predicted_days)
        print(f'Predicted date : {etb_cmb_date}')

        # Render the result
        return render(request, 'ml_model/predict_form.html', {
            'etb_cmb': etb_cmb_date.strftime('%Y-%m-%d'),
            'week': week,
            'vessel': vessel,
            'voyage': voyage,
            'etb_cgp': etb_cgp,
            'etd_cgp': etd_cgp,
            })

    # If no POST request, render the empty form
    return render(request, 'ml_model/predict_form.html')






def cce_table(request):
    if request.method == 'POST':
        df = load_data()
        df = remove_duplicate_vessels(df)
        
        data = json.loads(request.body)
        print(data)
        vessel_names = data.get('vessel_names', [])
        samples = generate_samples(df, vessel_names)
        print(samples)
        
        # Return data as JSON for frontend to handle
        return JsonResponse({'samples': samples}, safe=False)
    
    # If GET request, just render the template without any data
    return render(request, 'ml_model/cce_table.html')







