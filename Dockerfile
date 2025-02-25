FROM python:3.13

WORKDIR /app

RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm

RUN git clone https://github.com/ggerganov/whisper.cpp
RUN cd whisper.cpp && make && cp main /usr/local/bin/whisper

COPY . .

CMD ["python", "src/main.py"]
