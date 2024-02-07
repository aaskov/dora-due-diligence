from distutils.log import debug 
from fileinput import filename 
from flask import *
from PyPDF2 import PdfReader
import os
import openai
import json

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = "demo-dora-due-diligence4"

client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)


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

		# =======
		# Azure OpenAI service
		# -------
		completion = client.chat.completions.create(
	    model=deployment,
	    messages=[
	        {
	            "role": "user",
	            "content": "Does any part of the followin content fullfill the requirements mentioned in paragraph 2(a). You are only allowed to answer with yes or no: "+text,
	        },
	    ],
		    extra_body={
		        "dataSources": [
		            {
		                "type": "AzureCognitiveSearch",
		                "parameters": {
		                    "endpoint": os.environ.get("AZURE_SEARCH_ENDPOINT"),
		                    "key": os.environ.get("AZURE_SEARCH_API_KEY"),
		                    "indexName": "indexdoraarticle30"
		                }
		            }
		        ]
		    }
		)

		output = json.loads(completion.model_dump_json())

		ss302a = output["choices"][0]["message"]["content"]


		return render_template("acknowledgement.html", name = f.filename, text = text, ss302a=ss302a) 

if __name__ == '__main__': 
	app.run(debug=True)
