FROM python:latest

COPY bots/config.py /bots/
COPY bots/favretweet.py /bots/
COPY bots/autoreply.py /bots/
COPY bots/followFollowers.py /bots/
COPY bots/followFollowers_data.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
# CMD ["python3", "favretweet.py"]