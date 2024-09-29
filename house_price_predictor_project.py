import pandas as pd
from flask import Flask, render_template, request
import pickle
app = Flask(__name__)

# Read the CSV file, skipping the extra index column if it exists
data = pd.read_csv('Cleaned_data.csv', index_col=0)
pipe=pickle.load(open("RidgeModel.pkl","rb"))

# Debug print to ensure data is read correctly
print(data.head())

@app.route('/')
def index():
    # Ensure 'location' column is present in the data
    if 'location' in data.columns:
        locations = sorted(data['location'].unique())
        # Debug print to ensure locations are generated correctly
        print(locations)
        return render_template('index.html', locations=locations)
    else:
        return "Error: 'location' column not found in CSV file"

@app.route('/predict',methods=['POST'])
def predict():
  try:
     location=request.form.get('location')
     bhk=request.form.get('bhk')
     bath=request.form.get('bath')
     sqft=request.form.get('total_sqft')
     print(location,bhk,bath,sqft)
     input=pd.DataFrame([[location,sqft,bath,bhk]],columns=['location','total_sqft','bath','bhk'])
    #prediction=pipe.predict(input)[0]
     prediction = pipe.predict(input)[0]
     return f"Predicted house price: {prediction}"

  except ValueError as ve:
    error_message = f"ValueError: {str(ve)}"
    print(error_message)
    return render_template('error.html', error_message=error_message)

  except Exception as e:
    error_message = f"An error occurred: {str(e)}"
    print(error_message)
    return render_template('error.html', error_message=error_message)

  


    return str(prediction)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
