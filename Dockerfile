FROM mcr.microsoft.com/azure-functions/python:4-python3.8

# Pulls in necessary .py files and requirements
COPY * /

WORKDIR /

RUN pip install -r requirements.txt

# Port name which app runs on
EXPOSE 8501

# Running the streamlit and executing Home.py
ENTRYPOINT ["streamlit", "run"]

CMD ["Home.py"]