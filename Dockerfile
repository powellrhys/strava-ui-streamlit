FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements.txt

ENV client_id=""
ENV client_secret=""

EXPOSE 8501
EXPOSE 8502

ENTRYPOINT ["streamlit","run"]
CMD ["Home.py"]
