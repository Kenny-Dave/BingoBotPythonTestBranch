ROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN sudo apt-get install -y fonts-lato
RUN PATH=$PATH:~/usr/share/fonts/


CMD ["python3", "Bot.py"]