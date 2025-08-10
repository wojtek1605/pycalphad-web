from flask import Flask, request, send_file, render_template
import matplotlib.pyplot as plt
import io
from pycalphad import Database, binplot
import pycalphad.variables as v

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate')
def calculate():
    system = request.args.get('system', 'ag_al')

    # Map system param to database file and phases
    if system == 'ag_al':
        db_file = 'ag_al.TDB'
        phases = ['LIQUID', 'FCC_A1']
        comps = ['AG', 'AL', 'VA']
    elif system == 'fe_mn':
        db_file = 'fe_mn.TDB'
        phases = ['LIQUID', 'BCC_A2']
        comps = ['FE', 'MN', 'VA']
    else:
        return "Unknown system", 400

    db = Database(db_file)
    fig, ax = plt.subplots(figsize=(9,6))
    binplot(db, comps, phases, {v.X(comps[1]): (0, 1, 0.02), v.T: (300, 1500, 10), v.P:101325, v.N:1}, plot_kwargs={'ax': ax})

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)