#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from flask import *
from fileinput import filename 
from distutils.log import debug 
from pdf import ReadAndCleanPdfFile
from chat import SendAndReturnAnswer


# ==============================================================================
# FLASK APP CONFIGURATION
# ------------------------------------------------------------------------------

app = Flask(__name__) 


# Define the '/' endpoint
@app.route('/') 
def main(): 
    return render_template("index.html") 


# Define the '/success' endpoint (when documents have been processed)
@app.route('/success', methods = ['POST']) 
def success(): 
    if request.method == 'POST': 
        
        # Save the file locally (in order to read it)
        print('Saving file locally')
        f = request.files['file'] 
        f.save(f.filename) 

        # Read file (assuming PDF)
        contract = ReadAndCleanPdfFile(f.filename)
        
        # Ask Azure OpenAI
        answer2b = SendAndReturnAnswer("2(b)", contract)
        answer2c = SendAndReturnAnswer("2(c)", contract)
        answer2d = SendAndReturnAnswer("2(d)", contract)
        
        # Extract specific tags
        found2b = re.findall(r'<FOUND>(.*?)</FOUND>', answer2b)
        found2c = re.findall(r'<FOUND>(.*?)</FOUND>', answer2c)
        found2d = re.findall(r'<FOUND>(.*?)</FOUND>', answer2d)
        clause2b = re.findall(r'<CLAUSE>(.*?)</CLAUSE>', answer2b)
        clause2c = re.findall(r'<CLAUSE>(.*?)</CLAUSE>', answer2c)
        clause2d = re.findall(r'<CLAUSE>(.*?)</CLAUSE>', answer2d)
        explanation2b = re.findall(r'<EXPLANATION>(.*?)</EXPLANATION>', answer2b)
        explanation2c = re.findall(r'<EXPLANATION>(.*?)</EXPLANATION>', answer2c)
        explanation2d = re.findall(r'<EXPLANATION>(.*?)</EXPLANATION>', answer2d)
        
        # Handle empty scenarios
        if not found2b: found2b = 'Not found'
        if not found2c: found2c = 'Not found'
        if not found2d: found2d = 'Not found'
        if not clause2b: clause2b = 'No clause'
        if not clause2c: clause2c = 'No clause'
        if not clause2d: clause2d = 'No clause'
        if not explanation2b: explanation2b = 'No explanation'
        if not explanation2c: explanation2c = 'No explanation'
        if not explanation2d: explanation2d = 'No explanation'
        

        return render_template("acknowledgement.html", filename=f.filename, found2b=found2b, clause2b=clause2b, explanation2b=explanation2b, found2c=found2c, clause2c=clause2c, explanation2c=explanation2c, found2d=found2d, clause2d=clause2d, explanation2d=explanation2d)


# ==============================================================================
# RUN
# ------------------------------------------------------------------------------
if __name__ == '__main__': 
    app.run(debug=True)
