#BUILD: docker build -t say66-samdd:0.0.2  .      
#RUN: docker run -u root -it --entrypoint /bin/bash  saybanana-samdd:latest
# docker run -u prod -it --entrypoint /bin/bash  saybanana-samdd:latest
#RUN: docker run say66-samdd:0.0.2 

FROM python:3.10-slim
WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY system/.bashrc /root/.bashrc 
COPY packages/ packages/
COPY cache/samdd/ /root/.cache/samdd/
COPY src/ src/
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Create a non-root user 'prod'
RUN adduser --disabled-password --gecos "" prod

# Create cache directory for 'prod' user and adjust permissions
RUN mkdir -p /home/prod/.cache/samdd \
    && chown -R prod:prod /home/prod/.cache
COPY --chown=prod:prod cache/samdd/ /home/prod/.cache/samdd/

# Copy the .bashrc file for the 'prod' user and adjust permissions
COPY system/.bashrc /home/prod/.bashrc
RUN chown prod:prod /home/prod/.bashrc

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

USER prod


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

