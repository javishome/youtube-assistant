FROM chinhlengoc123/music_base1:latest

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements_all.txt
RUN pip3 install --upgrade yt-dlp

EXPOSE 2024

CMD python3 main.py
