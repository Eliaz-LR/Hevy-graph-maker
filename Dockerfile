FROM python:3.9
ADD *.py .
RUN pip install nicegui pandas nicegui[highcharts]
CMD [ "python", "./main.py" ]

EXPOSE 80 8080 443