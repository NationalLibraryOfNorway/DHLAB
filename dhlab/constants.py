import os
from dotenv import load_dotenv

load_dotenv("dhlab.env")  # take environment variables

"""Constant variables used across modules, change in dhlab.env or through environment variable"""

BASE_URL = os.getenv("NB_DHLAB_BASE_URL")  #: REST-API URL adress to fulltext query functions
NGRAM_API =  os.getenv("NB_DHLAB_NGRAM_API") #: URL adress for API calls to ngram-databases
GALAXY_API = os.getenv("NB_DHLAB_GALAXY_API")  #: URL adress for word galaxy API queries
