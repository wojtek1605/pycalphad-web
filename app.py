#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 19:13:39 2025

@author: wojtek
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import matplotlib.pyplot as plt
from pycalphad import Database, variables as v
from scheil import simulate_scheil_solidification

# Uncomment when you need pycalphad:
# from pycalphad import Database, binplot
# import pycalphad.variables as v

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # allow cross-origin requests if needed

# ---------------------------
# PLACEHOLDERS: put your pycalphad logic here
# ---------------------------
def generate_phase_diagram(db_file, components, phases, T_min, T_max, X_min, X_max):
    """
    Return a matplotlib.figure.Figure object representing the phase diagram.
    Replace this body with your pycalphad/binplot call and plotting code.
    Example (commented):
        db = Database(db_file)
        fig, ax = plt.subplots(figsize=(9,6))
        binplot(db, components, phases,
                { v.X(components[1]): (X_min, X_max, 0.02), v.T: (T_min, T_max, 10), v.P:101325, v.N:1 },
                plot_kwargs={'ax': ax})
        return fig
    """
    fig, ax = plt.subplots(figsize=(8,6))
    # Dummy placeholder plot (replace with real calculation)
    ax.plot([X_min, X_max], [T_min, T_max], marker='o')
    ax.set_xlabel('Composition (X)')
    ax.set_ylabel('Temperature (K)')
    ax.set_title('Phase diagram (placeholder)')
    return fig

def generate_solidification_path(db_file, components, phases, T_start, X_value):
    """
    Return a matplotlib.figure.Figure object representing a solidification path.
    Replace this with your actual solidification path calculation.
    """
    dbf = db_file
    comps = components
    phases = sorted(dbf.phases.keys())
    liquid_phase_name = 'LIQUID'
    composition = float(X_value)
    initial_composition = {v.X('AL'):composition}
    start_temperature = int(T_start)
    sol_res = simulate_scheil_solidification(dbf,comps,phases,initial_composition, start_temperature, step_temperature=1)   
    fig, ax = plt.subplots(figsize=(8, 6))
    for phase_name, amounts in sol_res.cum_phase_amounts.items():
        ax.plot(sol_res.temperatures, amounts, label=phase_name)
    ax.plot(sol_res.temperatures, sol_res.fraction_liquid, label='LIQUID', linewidth=2)
    
    ax.set_ylabel('Phase Fraction')
    ax.set_xlabel('Temperature (K)')
    ax.set_title(f'Scheil Simulation: {composition:.2f} X_AL')
    ax.legend(loc='best')

    return fig
# ---------------------------
# end placeholders
# ---------------------------

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/calculator')
def calculator():
    return app.send_static_file('1.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Expects JSON like:
    Phase diagram:
      { "type":"phase-diagram", "system":"ag_al", "T_min":300, "T_max":1500, "X_min":0.0, "X_max":1.0 }
    Solidification:
      { "type":"solidification", "system":"ag_al", "T_start":1500, "X_value":0.5 }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error":"Missing JSON body"}), 400

    calc_type = data.get('type')
    system = data.get('system', 'ag_al')

    # map system -> db_file, components, phases (extend as needed)
    if system == 'ag_al':
        db_file = 'ag_al.TDB'
        components = ['AG', 'AL', 'VA']
        phases = ['LIQUID', 'FCC_A1']
    elif system == 'au_mg':
        db_file = 'au_mg.TDB'
        components = ['AU', 'MG', 'VA']
        phases = ['LIQUID', 'FCC_A1']
    else:
        # default/fallback; you can add more mappings
        db_file = data.get('db_file', 'ag_al.TDB')
        components = data.get('components', ['AG','AL','VA'])
        phases = data.get('phases', ['LIQUID','FCC_A1'])

    try:
        if calc_type == 'phase-diagram':
            T_min = float(data.get('T_min', 300))
            T_max = float(data.get('T_max', 1500))
            X_min = float(data.get('X_min', 0.0))
            X_max = float(data.get('X_max', 1.0))
            fig = generate_phase_diagram(db_file, components, phases, T_min, T_max, X_min, X_max)

        elif calc_type == 'solidification':
            T_start = float(data.get('T_start', 1500))
            X_value = float(data.get('X_value', 0.5))
            fig = generate_solidification_path(db_file, components, phases, T_start, X_value)

        else:
            return jsonify({"error":"Unknown calculation type (use 'phase-diagram' or 'solidification')"}), 400

        # stream figure back as PNG
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')

    except Exception as e:
        # print traceback on server logs and return error message
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
