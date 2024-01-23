FROM python:3.9

# locales = ['en_US.UTF-8','fr_FR.UTF-8','de_DE.UTF-8','es_ES.UTF-8','it_IT.UTF-8','pt_PT.UTF-8','tr_TR.UTF-8','zh_CN.UTF-8','ru_RU.UTF-8','ja_JP.UTF-8','ko_KR.UTF-8']
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN sed -i -e '/en_US.UTF-8/s/^# //g' -e '/fr_FR.UTF-8/s/^# //g' -e '/de_DE.UTF-8/s/^# //g' -e '/es_ES.UTF-8/s/^# //g' -e '/it_IT.UTF-8/s/^# //g' -e '/pt_PT.UTF-8/s/^# //g' -e '/tr_TR.UTF-8/s/^# //g' -e '/zh_CN.UTF-8/s/^# //g' -e '/ru_RU.UTF-8/s/^# //g' -e '/ja_JP.UTF-8/s/^# //g' -e '/ko_KR.UTF-8/s/^# //g' /etc/locale.gen
RUN locale-gen

ADD *.py .
RUN pip install nicegui pandas nicegui[highcharts]
CMD [ "python", "./main.py" ]

EXPOSE 80 8080 443