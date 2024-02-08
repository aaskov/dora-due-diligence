#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import openai


# =============================================================================
# GET ENVIRONMENT VARIABLES AND AVOID EXPOSING KEYS
# -----------------------------------------------------------------------------

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
search_key = os.environ.get("AZURE_SEARCH_API_KEY")



# =============================================================================
# FUNCTION
# -----------------------------------------------------------------------------

def SendAndReturnAnswer(which_paragraph, contract):
    """Send and return the answer from Azure OpenAI service using a specific
    prompt engineered request regarding DORA.

    Parameters
    ----------
    which_paragraph : string
        What is the DORA paragraph that has to be searched for? Eg. '2(b)'
    contract : strig
        The text from the contract that is going to get analyzed.

    Returns
    -------
    content : string
        The returned (first) answer from Azure OpenAI.

    """

    # This is the Azure OpenAI service deploy name
    deployment = "demo-dora-due-diligence4"

    client = openai.AzureOpenAI(
        base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
        api_key=api_key,
        api_version="2023-08-01-preview",
    )

    # This is the indexing search deployment name
    search_deployment = "indexdoraarticle30"

    # Prompt engineering
    message = ""
    message += "You are a contract manager and lawyer who specializes in DORA compliance. DORA specifies that the contractual arrangements on the use of ICT services shall include a list of elements."
    message += "Your task is to look through the contract and assess whether the contract contains clause which fulfills the requirements set by a specific pararaph in the DORA act text."
    message += "The specific DORA paragraph is {0}.".format(which_paragraph)
    message += "When you answer, it is important that you are certain that the contract contains a clause which covers the paragraph, so just say it, if you can't find it."
    message += "You should structure your answer like this:"
    message += "A FULLY, PARTIALLY or NOT FOUND indication of whether a clause can be found which covers the DORA paragraph inside a set of <FOUND> </FOUND> markers."
    message += "Parrot the exact text of the clause (or clauses) from the contract, with no interpretation, just the text, which covers the DORA paragraph inside a set of <CLAUSE> </CLAUSE> markers. Reply with NOT FOUND if it is not found."
    message += "Give an explanation of 1-3 lines as to why the clause in the contract covers or doesn't cover the DORA paragraph requirement and base your explanation on the DORA element text, inside a set of <EXPLANATION> </EXPLANATION> markers."
    message += "Please review the contract and then give your answer. Here is the contract:"
    message += " " + contract

    # Initiate a communication
    print("Asking Azure OpenAI about paragraph {0}".format(which_paragraph))
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": message
            },
        ],
            extra_body={
                "dataSources": [
                    {
                        "type": "AzureCognitiveSearch",
                        "parameters": {
                            "endpoint": search_endpoint,
                            "key": search_key,
                            "indexName": search_deployment
                        }
                    }
                ]
            }
    )

    # Intepret the responce in a JSON format
    output = json.loads(completion.model_dump_json())

    # Extract the content part (assuming only a single answer)
    content = output["choices"][0]["message"]["content"]

    return(content)

