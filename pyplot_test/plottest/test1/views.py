from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
import os
from pycalphad import Database, binplot
import pycalphad.variables as v
import matplotlib

matplotlib.use('agg')

def home(request):
    dbf = Database('ag_al.TDB')
    comps = ['AL','AG','VA']
    phases = dbf.phases.keys()
   # fig = plt.figure(figsize=(9,6))
    fig=plt.figure()
    axes = fig.gca()
    binplot(dbf, ['AG', 'AL', 'VA'] , phases, {v.X('AL'):(0,1,0.02), v.T: (300, 1500, 10), v.P:101325, v.N: 1}, plot_kwargs={'ax': axes})
  #  plt.savefig('foo.png')
   # plt.show()
    
    plt.switch_backend('Agg') 
  #  plt.plot(range(10))
  #  fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request,'home.html',{'data':uri})

# Create your views here.
