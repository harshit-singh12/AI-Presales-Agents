#!/usr/bin/env python
import sys
import warnings
import os
import certifi

from crew import Companyresearcher
os.environ["SSL_CERT_FILE"] = certifi.where()
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

class main_crew():
    def startCrew(userinput: str):
        """
        Run the crew.
        """
        result = ''
        inputs = {
            'company_name': userinput.strip()
        }
        
        try:
            result = Companyresearcher().crew().kickoff(inputs=inputs)
        except Exception as e:
            result = (f"An error occurred while running the crew: {e}")
        return result

#run()
