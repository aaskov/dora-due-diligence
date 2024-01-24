from distutils.log import debug 
from fileinput import filename 
from flask import *
from PyPDF2 import PdfReader
app = Flask(__name__) 

@app.route('/') 
def main(): 
	return render_template("index.html") 

@app.route('/success', methods = ['POST']) 
def success(): 
	if request.method == 'POST': 
		# Save file 
		print('Saving file locally')
		f = request.files['file'] 
		f.save(f.filename) 

		# Read file (assuming PDF)
		print('Reading text from file')
		reader = PdfReader(f.filename)
		text = ""
		for i in range(len(reader.pages)):
			text += reader.pages[i].extract_text()

		return render_template("acknowledgement.html", name = f.filename, text = text) 

if __name__ == '__main__': 
	app.run(debug=True)
