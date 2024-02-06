from flask import Flask, redirect, render_template,request, session, jsonify
import secrets
from datetime import datetime
from fd import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.static_url_path = '/static'  # The URL path to serve static files
app.static_folder = "templates\static"
app.secret_key = secrets.token_hex(16)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/fixed_deposits')
def fixed_deposits():
    multiple_call = request.args.get('multiple')
    if multiple_call == None:
        redirect_call = session.pop('redirect_call', False)
        output_json = session.pop('output_json', [])
        if redirect_call==False:
            return render_template('fixed_deposits.html')
        elif redirect_call==True:
            if len(output_json)== 11:
                end_dates = output_json[0]["line_labels"]; principal_amounts = output_json[1]["principal_amounts"]; values = output_json[2]["values"]; principal = output_json[3]["principal"]; slice_interest = output_json[4]["interest"]; slices = output_json[5]["slices"]; current_evalution = output_json[6]["current_evalution"]; amount = output_json[7]["amount"]; current_evalution_interest_dates = output_json[8]["current_evalution_interest_dates"]; total_interest_dates = output_json[9]["total_interest_dates"]; total_interest = output_json[10]["total_interest"]
                return render_template('fixed_deposits.html',line_labels=end_dates, principal_amounts=principal_amounts, values=values, principal=principal, interest=slice_interest, slices=slices, amount=amount, current_evalution=current_evalution, current_evalution_interest_dates=current_evalution_interest_dates, total_interest_dates=total_interest_dates, total_interest=total_interest)
            elif len(output_json)> 11:
                
                end_dates = output_json[0]["line_labels"]; principal_amounts = output_json[1]["principal_amounts"]; values = output_json[2]["values"]; principal = output_json[3]["principal"]; slice_interest = output_json[4]["interest"]; slices = output_json[5]["slices"]; current_evalution = output_json[6]["current_evalution"];amount = output_json[7]["amount"];  current_evalution_interest_dates = output_json[8]["current_evalution_interest_dates"]; total_interest_dates = output_json[9]["total_interest_dates"]; slice_interest_dates = output_json[10]["slice_interest_dates"]; total_interest = output_json[11]["total_interest"]  
                return render_template('fixed_deposits.html',line_labels=end_dates, principal_amounts=principal_amounts, values=values, principal=principal, interest=slice_interest, slices=slices, amount=amount, current_evalution=current_evalution, current_evalution_interest_dates=current_evalution_interest_dates, total_interest_dates=total_interest_dates, slice_interest_dates=slice_interest_dates, total_interest=total_interest)
        else:
            return {'returncode': 1,'message': 'The Service is unavailable.'}, 503
    elif multiple_call=='yes':
        return render_template('multiple_fd.html')
    else:
        return render_template('error_404.html')


@app.route('/calculate_fd',  methods=['POST'])
def calculate_fd():
    form = request.form
    try:
        line_labels, principal_amounts, slice_interest ,principal, values, slices, current_evaluation_interest, total_interest = fd_calculate(form)
        amount = float(principal) + total_interest.item()

        # For Biforgation
        slice_start = (form.get('slice_start')); slice_end = (form.get('slice_end')); start = (form.get('start')); maturity = (form.get('maturity'))
        if(slice_start=='' or slice_end==''):
            current_evalution_interest_dates = start + " - " + datetime.strftime(datetime.now(), "%Y-%m-%d") 
            total_interest_dates = start + " - " + maturity 
            output = [{"line_labels":line_labels}, {"principal_amounts":principal_amounts}, {"values":values}, {"principal":float(principal)}, {"interest": (slice_interest.item()+ float(principal))}, {"slices":slices}, {"current_evalution":(current_evaluation_interest.item() + float(principal))}, {"amount":amount}, {"current_evalution_interest_dates":current_evalution_interest_dates}, {"total_interest_dates":total_interest_dates},{"total_interest":(total_interest + float(principal))}]
        else:             
            current_evalution_interest_dates = start + " - " + datetime.strftime(datetime.now(), "%Y-%m-%d") 
            slice_interest_dates = slice_start + " - " + slice_end 
            total_interest_dates = start + " - " + maturity 
            output = [{"line_labels":line_labels}, {"principal_amounts":principal_amounts}, {"values":values}, {"principal":float(principal)}, {"interest": (slice_interest.item() + float(principal))}, {"slices":slices}, {"current_evalution":(current_evaluation_interest.item() + float(principal))}, {"amount":amount}, {"current_evalution_interest_dates":current_evalution_interest_dates}, {"total_interest_dates":total_interest_dates}, {"slice_interest_dates":slice_interest_dates}, {"total_interest":(total_interest + float(principal))}]
        session['redirect_call'] = True
        session['output_json'] = output
        return redirect('/fixed_deposits')
    except Exception as err:
        return {'returncode': 1,'message': 'Looks like you have reached your monthly limit or rather the service itself is unavailable.'}, 403

@app.route('/calculate_fds',  methods=['POST'])
def calculate_fds():
    try:
        data = request.get_json()
        # Process the data as needed
        return jsonify({'status': 'success', 'message': 'Data received and processed successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route("/test")
def test():
    return "Test Approved from Finoplex"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    
    