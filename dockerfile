#BUILD: docker build -t say66-samdd:0.0.2  .      
#RUN: docker run -u root -it --entrypoint /bin/bash  say66-samdd:0.0.2 
#RUN: docker run say66-samdd:0.0.2 

FROM python:3.10-slim
WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY system/.bashrc /root/.bashrc 
COPY packages/samdd-method/ samdd-method/ 
COPY packages/SBFirebase-Interface/ SBFirebase-Interface/
COPY cache/samdd/ /root/.cache/samdd/
COPY samdd-saybanana.py . \
     requirements.txt . \
     logs/ .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Create a non-root user 'prod'
RUN adduser --disabled-password --gecos "" prod

# Create cache directory for 'prod' user and adjust permissions
RUN mkdir -p /home/prod/.cache/samdd \
    && chown -R prod:prod /home/prod/.cache

# Copy cache files to the 'prod' user's cache directory
COPY --chown=prod:prod cache/samdd/ /home/prod/.cache/samdd/

# Switch to the new user for all subsequent commands
USER prod

CMD ["python", "./samdd-saybanana.py"]

