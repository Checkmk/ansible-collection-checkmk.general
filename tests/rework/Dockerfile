FROM ubuntu:jammy
LABEL maintainer="Robin Gierse"

ENV pip_packages "ansible"

ARG distro="jammy"
ARG DEBIAN_FRONTEND=noninteractives

ENV stable "2.2.0p14"
ENV old "2.1.0p36"
ENV ancient "2.0.0p39"

# Install dependencies.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
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
       rsyslog systemd sudo iproute2 \
       wget \
    && \
    apt-get clean && \
    rm -Rf /var/lib/apt/lists/* && \
    rm -Rf /usr/share/doc
RUN sed -i 's/^\($ModLoad imklog\)/#\1/' /etc/rsyslog.conf

# Fix potential UTF-8 errors with ansible-test.
RUN locale-gen en_US.UTF-8

# Install Ansible via Pip.
RUN pip3 install $pip_packages

COPY files/initctl_faker .
RUN chmod +x initctl_faker && rm -fr /sbin/initctl && ln -s /initctl_faker /sbin/initctl

# Install Ansible inventory file.
RUN mkdir -p /etc/ansible
RUN echo "[local]\nlocalhost ansible_connection=local" > /etc/ansible/hosts

# Remove unnecessary getty and udev targets that result in high CPU usage when using
# multiple containers with Molecule (https://github.com/ansible/molecule/issues/1104)
RUN rm -f /lib/systemd/system/systemd*udev* \
  && rm -f /lib/systemd/system/getty.target

# Install Checkmk
RUN apt-get update &&\
    # wget https://download.checkmk.com/checkmk/${ancient}/check-mk-raw-${ancient}_0.${distro}_amd64.deb && \
    # wget https://download.checkmk.com/checkmk/${old}/check-mk-raw-${old}_0.${distro}_amd64.deb && \
    wget https://download.checkmk.com/checkmk/${stable}/check-mk-raw-${stable}_0.${distro}_amd64.deb && \
    # apt-get install -y ./check-mk-raw-${ancient}_0.${distro}_amd64.deb && \
    # apt-get install -y ./check-mk-raw-${old}_0.${distro}_amd64.deb && \
    apt-get install -y ./check-mk-raw-${stable}_0.${distro}_amd64.deb

VOLUME ["/sys/fs/cgroup", "/tmp", "/run"]
CMD ["/lib/systemd/systemd"]
