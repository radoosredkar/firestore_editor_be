# set base image (host OS)
FROM python:3.8

# set the working directory in the container
RUN apt-get update && apt-get install -y vim & apt-get install -y default-libmysqlclient-dev
# prerequisites for mysql
RUN mkdir /usr/src/firestore_gui
RUN mkdir /var/log/firestore_gui
WORKDIR /usr/src/firestore_gui

RUN /usr/local/bin/python -m pip install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r /usr/src/firestore_gui/requirements.txt

EXPOSE 5000

RUN echo "pip install -r /usr/src/firestore_gui/requirements.txt" > /usr/bin/build
RUN echo "python /usr/src/firestore_gui/main.py" > /usr/bin/run

RUN chmod +x /usr/bin/build
RUN chmod +x /usr/bin/run

CMD [ "flask", "run", "--host=0.0.0.0" ] 
