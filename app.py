from src.exception import ModelException
from src.logger import logging
from src.constant.application import APP_HOST, APP_PORT
from src.pipline.predict_pipeline import CustomData, PredictionPipeline
from flask import Flask,request,render_template


from flask import Flask,request,render_template

application = Flask(__name__)

app = application

## routes for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method== 'GET':
        return render_template('home.html')
    else:
        data = CustomData(fixed_acidity=request.form.get('fixed_acidity'),
                volatile_acidity=request.form.get('volatile_acidity'),
                citric_acid=request.form.get('citric_acid'),
                residual_sugar=request.form.get('residual_sugar'),
                chlorides=request.form.get('chlorides'),
                free_sulfur_dioxide=request.form.get('free_sulfur_dioxide'),
                total_sulfur_dioxide=request.form.get('total_sulfur_dioxide'),
                density=request.form.get('density'),
                pH=request.form.get('pH'),
                sulphates=request.form.get('sulphates'),
                alcohol=request.form.get('alcohol'))
        
        data_df = data.get_data_as_data_frame()
        predict_pipeline = PredictionPipeline()
        results = predict_pipeline.predict(data_df)
        
        return render_template('home.html', results=results+3)
    
    
if __name__=="__main__":
    app.run(host=APP_HOST,debug=True,port=APP_PORT)