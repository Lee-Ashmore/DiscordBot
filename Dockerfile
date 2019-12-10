FROM python:3.8.0-buster
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/discord
RUN cd tmp/discord
CMD ["python", "./tmp/discord/bot.py"]