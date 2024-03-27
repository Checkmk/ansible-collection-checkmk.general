FROM ubuntu:jammy
LABEL maintainer="Robin Gierse"

ARG distro="jammy"
ARG DEBIAN_FRONTEND=noninteractive

ENV stable "2.2.0p17"
ENV old "2.1.0p37"
ENV ancient "2.0.0p39"

ARG DL_USER="d-gh-ansible-dl"
ARG DL_PW

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
       wget

# Remove unnecessary units
RUN rm -f /lib/systemd/system/multi-user.target.wants/* \
  /etc/systemd/system/*.wants/* \
  /lib/systemd/system/local-fs.target.wants/* \
  /lib/systemd/system/sockets.target.wants/*udev* \
  /lib/systemd/system/sockets.target.wants/*initctl* \
  /lib/systemd/system/sysinit.target.wants/systemd-tmpfiles-setup* \
  /lib/systemd/system/systemd-update-utmp*

# Download files first to have them cached.
## Free downloads
RUN \
    wget https://download.checkmk.com/checkmk/${ancient}/check-mk-raw-${ancient}_0.${distro}_amd64.deb ; \
    wget https://download.checkmk.com/checkmk/${old}/check-mk-raw-${old}_0.${distro}_amd64.deb ; \
    wget https://download.checkmk.com/checkmk/${stable}/check-mk-raw-${stable}_0.${distro}_amd64.deb ; \
    wget https://download.checkmk.com/checkmk/${stable}/check-mk-cloud-${stable}_0.${distro}_amd64.deb
## Restricted downloads
RUN \
    wget --user=${DL_USER} --password=${DL_PW} https://download.checkmk.com/checkmk/${stable}/check-mk-enterprise-${stable}_0.${distro}_amd64.deb ; \
    wget --user=${DL_USER} --password=${DL_PW} https://download.checkmk.com/checkmk/${stable}/check-mk-managed-${stable}_0.${distro}_amd64.deb ; \
    wget --user=${DL_USER} --password=${DL_PW} https://download.checkmk.com/checkmk/${old}/check-mk-enterprise-${old}_0.${distro}_amd64.deb ; \
    wget --user=${DL_USER} --password=${DL_PW} https://download.checkmk.com/checkmk/${old}/check-mk-managed-${old}_0.${distro}_amd64.deb ; \
    wget --user=${DL_USER} --password=${DL_PW} https://download.checkmk.com/checkmk/${ancient}/check-mk-enterprise-${ancient}_0.${distro}_amd64.deb ; \
    wget --user=${DL_USER} --password=${DL_PW} https://download.checkmk.com/checkmk/${ancient}/check-mk-managed-${ancient}_0.${distro}_amd64.deb

# Fix potential UTF-8 errors with ansible-test.
RUN locale-gen en_US.UTF-8

# Install Ansible via Pip.
# COPY ../../requirements.txt /
# RUN pip3 install -r /requirements.txt
RUN pip3 install ansible

# Install Ansible inventory file.
RUN mkdir -p /etc/ansible
RUN echo "[local]\nlocalhost ansible_connection=local" > /etc/ansible/hosts

# Install systemctl faker and enable apache2 service at boot
COPY files/systemctl3.py /usr/bin/systemctl
RUN systemctl enable apache2

# Install Checkmk
RUN apt-get update && \
    apt-get install -y \
      ./check-mk-raw-${ancient}_0.${distro}_amd64.deb \
      ./check-mk-raw-${old}_0.${distro}_amd64.deb \
      ./check-mk-raw-${stable}_0.${distro}_amd64.deb \
      ./check-mk-cloud-${stable}_0.${distro}_amd64.deb \
      ./check-mk-enterprise-${ancient}_0.${distro}_amd64.deb \
      ./check-mk-managed-${ancient}_0.${distro}_amd64.deb \
      ./check-mk-enterprise-${old}_0.${distro}_amd64.deb \
      ./check-mk-managed-${old}_0.${distro}_amd64.deb \
      ./check-mk-enterprise-${stable}_0.${distro}_amd64.deb \
      ./check-mk-managed-${stable}_0.${distro}_amd64.deb

# Install Python Versions from Deadsnakes
COPY files/deadsnakes.gpg /etc/apt/keyrings/deadsnakes.gpg
COPY files/deadsnakes.list /etc/apt/sources.list.d/deadsnakes.list
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.8-dev \
    python3.8-distutils \
    python3.8-venv \
    python3.9-dev \
    python3.9-distutils \
    python3.9-venv \
    python3.10-dev \
    python3.10-distutils \
    python3.10-venv \
    python3.11-dev \
    python3.11-distutils \
    python3.11-venv \
    python3.12-dev \
    python3.12-distutils \
    python3.12-venv \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc

# Pre-create Sites
RUN \
  omd -V ${stable}.cre create -A --no-tmpfs --admin-password "mysecret" "stable_cre" ; \
  omd -V ${stable}.cee create -A --no-tmpfs --admin-password "mysecret" "stable_cee" ; \
  omd -V ${stable}.cme create -A --no-tmpfs --admin-password "mysecret" "stable_cme" ; \
  omd -V ${stable}.cce create -A --no-tmpfs --admin-password "mysecret" "stable_cce" ; \
  omd -V ${old}.cre create -A --no-tmpfs --admin-password "mysecret" "old_cre" ; \
  omd -V ${old}.cee create -A --no-tmpfs --admin-password "mysecret" "old_cee" ; \
  omd -V ${old}.cme create -A --no-tmpfs --admin-password "mysecret" "old_cme" ; \
  omd -V ${ancient}.cre create -A --no-tmpfs --admin-password "mysecret" "ancient_cre" ; \
  omd -V ${ancient}.cee create -A --no-tmpfs --admin-password "mysecret" "ancient_cee" ; \
  omd -V ${ancient}.cme create -A --no-tmpfs --admin-password "mysecret" "ancient_cme"

CMD ["/usr/bin/systemctl"]
