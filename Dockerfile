#Docker para rodar a aplicação, ainda trabalhando

# https://hub.docker.com/_/python
FROM python

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Bundle app source
COPY . .


# Criar dockerfile com overlay no file para desenvolvimento e depois o dockerfile de produção que é a copia daquela pasta e com os envs
