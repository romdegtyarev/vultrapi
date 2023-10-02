FROM ubuntu

ENV USER_ID            1000
ENV GROUP_ID           985
ENV USER_GROUP_NAME    vultr

RUN apt-get update && apt-get install -y \
    python \
    python3 \
    python3-venv \
    python-pip \
    poppler-utils \
    python-poppler \
    libpoppler-cpp-dev \
    vim \
    sudo

RUN ln -fs /ust/share/zoneinfo/Asia/Novosibirsk /etc/localtime

RUN groupadd -g $GROUP_ID $USER_GROUP_NAME
RUN useradd -u $USER_ID -g $GROUP_ID -m $USER_GROUP_NAME

RUN mkdir -p /home/vultr/pyvenv
RUN python3 -m venv /home/vultr/pyvenv
RUN /home/vultr/pyvenv/bin/python3 -m pip install --upgrade pip
RUN /home/fivultra/pyvenv/bin/pip3 install schedule
RUN /home/vultr/pyvenv/bin/pip3 install beautifulsoup4
RUN /home/vultr/pyvenv/bin/pip3 install pdf2image
RUN /home/vultr/pyvenv/bin/pip3 install requests

RUN mkdir -p /home/vultr/vultr
RUN chown -R $USER_GROUP_NAME:$USER_GROUP_NAME /home/vultr/vultr
RUN chmod -R 777 /home/vultr/vultr

