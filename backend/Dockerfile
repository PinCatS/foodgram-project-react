FROM python:3.10.7
RUN apt update && apt install \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    gettext

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . ./

WORKDIR /app/foodgram

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 
