From tiangolo/uwsgi-nginx-flask:flask-python3.5
MAINTAINER nathan <huangxin911@gmail.com>

##########################################
# General
##########################################
# RUN apt-get update
# RUN apt-get install -y build-essential python-dev git
# RUN pip install --upgrade pip setuptools

##########################################
# Project packages
##########################################
# Install Python Packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

##########################################
# API files
##########################################
# get python api file
COPY ./app /app/

# set the default directory where CMD will execute
WORKDIR /app

# Expose ports
EXPOSE 80

#Define the default command
ENTRYPOINT ["python"]
CMD ["main.py"]

