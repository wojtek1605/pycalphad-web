#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 21:18:05 2025

@author: wojtek
"""

from flask import Flask, request, send_file, jsonify
import matplotlib.pyplot as plt
import io
from pycalphad import Database, binplot
import pycalphad.variables as v

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "PyCalphad API is running. Send a GET request to /calculate"
    })

@app.route('/calculate', methods=['GET'])
def calculate():
    

    db_agal = Database('ag_al.TDB')
    phases = ['LIQUID','FCC_A1']
    fig = plt.figure(figsize=(9,6))
    axes = fig.gca()
    binplot(db_agal, ['AG', 'AL', 'VA'] , phases, {v.X('AL'):(0,1,0.02), v.T: (300, 1500, 10), v.P:101325, v.N: 1}, plot_kwargs={'ax': axes})

   
    
    
    
    
    
    # Get user parameters from query string
    #element = request.args.get('element', 'Fe')
    #temperature = float(request.args.get('T', 1000))

    # ----------------------------
    # PLACEHOLDER for pycalphad code
    # Example: do real calculations here
    # result = run_pycalphad(element, temperature)
    # For now, let's just make a dummy plot
    # ----------------------------
    #temps = [temperature - 200, temperature, temperature + 200]
    #values = [t**0.5 for t in temps]  # Fake data

    #plt.figure()
    #plt.plot(temps, values, marker='o')
    #plt.title(f"PyCalphad Results for {element} at {temperature}K")
    #plt.xlabel("Temperature (K)")
    #lt.ylabel("Property Value")

    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
