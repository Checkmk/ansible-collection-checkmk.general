FROM ubuntu:jammy
LABEL maintainer="Robin Gierse"

ARG distro="jammy"
ARG DEBIAN_FRONTEND=noninteractives

ENV stable "2.2.0p17"
ENV old "2.1.0p37"
ENV ancient "2.0.0p39"

# Install dependencies.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       apache2 \
       apt-utils \
       build-essential \
       locales \
       libffi-dev \
       libssl-dev \
       libyaml-dev \
       man \
       python3-dev \
       python3-setuptools \
       python3-pip \
       python3-yaml \
       software-properties-common \
       rsyslog sudo iproute2 \
       wget \
    && \
    apt-get clean && \
    rm -Rf /var/lib/apt/lists/* && \
    rm -Rf /usr/share/doc

# Download files first to have them cached.
RUN wget https://download.checkmk.com/checkmk/${ancient}/check-mk-raw-${ancient}_0.${distro}_amd64.deb && \
    wget https://download.checkmk.com/checkmk/${old}/check-mk-raw-${old}_0.${distro}_amd64.deb && \
    wget https://download.checkmk.com/checkmk/${stable}/check-mk-raw-${stable}_0.${distro}_amd64.deb && \
    wget https://download.checkmk.com/checkmk/${stable}/check-mk-cloud-${stable}_0.${distro}_amd64.deb

RUN sed -i 's/^\($ModLoad imklog\)/#\1/' /etc/rsyslog.conf

# Fix potential UTF-8 errors with ansible-test.
RUN locale-gen en_US.UTF-8

# Install Ansible via Pip.
# COPY ../../requirements.txt /
# RUN pip3 install -r /requirements.txt
RUN pip3 install ansible

# Install Ansible inventory file.
RUN mkdir -p /etc/ansible
RUN echo "[local]\nlocalhost ansible_connection=local" > /etc/ansible/hosts

# Remove unnecessary units
RUN rm -f /lib/systemd/system/multi-user.target.wants/* \
  /etc/systemd/system/*.wants/* \
  /lib/systemd/system/local-fs.target.wants/* \
  /lib/systemd/system/sockets.target.wants/*udev* \
  /lib/systemd/system/sockets.target.wants/*initctl* \
  /lib/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup* \
  /lib/systemd/system/systemd-update-utmp* \
  /lib/systemd/system/getty.target

# Install systemctl faker and enable apache2 service at boot
COPY files/systemctl3.py /usr/bin/systemctl
RUN systemctl enable apache2

# Install Checkmk
RUN apt-get update && \
    # mv /usr/bin/systemctl /usr/bin/systemctl.bak && \
    # echo "exit 0" > /usr/bin/systemctl && \
    # chmod +x /usr/bin/systemctl && \
    apt-get install -y \
      ./check-mk-raw-${ancient}_0.${distro}_amd64.deb \
      ./check-mk-raw-${old}_0.${distro}_amd64.deb \
      ./check-mk-raw-${stable}_0.${distro}_amd64.deb \
      ./check-mk-cloud-${stable}_0.${distro}_amd64.deb
    # && mv /usr/bin/systemctl.bak /usr/bin/systemctl && \
    # chmod +x /usr/bin/systemctl

CMD ["/usr/bin/systemctl"]
