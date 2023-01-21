FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["Home.py"]


# FROM mcr.microsoft.com/azure-functions/python:4-python3.8

# # Pulls in necessary .py files and requirements
# COPY . .

# WORKDIR /

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt requirements.txt
# RUN pip install -U pip
# RUN pip install -r requirements.txt

# # Port name which app runs on
# EXPOSE 8501

# # Running the streamlit and executing Home.py
# ENTRYPOINT ["streamlit", "run"]

# CMD [“Home.py”]