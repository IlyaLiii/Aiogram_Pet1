FROM python:3.11-slim AS bot

WORKDIR /opt/bot_roulette

COPY requirements.txt requirements.txt

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN  chmod +x ./entrypoint.bash

RUN ls ../

RUN ls ~

ENTRYPOINT ["bash", "./entrypoint.bash"]