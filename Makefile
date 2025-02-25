install:
    pip install -r requirements.txt
    python -m spacy download pt_core_news_sm
    git clone https://github.com/ggerganov/whisper.cpp
    cd whisper.cpp
    make
    cp main ../bin/whisper
    cd ../
    rm -rf whisper.cpp

run:
    python src/main.py

test:
    pytest --cov=src tests/ --cov-report=term-missing

docker-build:
    docker build -t video-processor .

docker-run:
    docker run -v $(pwd)/raw:/app/raw -v $(pwd)/output:/app/output video-processor
