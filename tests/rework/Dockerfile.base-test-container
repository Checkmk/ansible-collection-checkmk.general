FROM quay.io/bedrock/ubuntu:focal-20230801

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    g++ \
    gcc \
    git \
    gnupg2 \
    libbz2-dev \
    libffi-dev \
    libreadline-dev \
    libsqlite3-dev \
    libxml2-dev \
    libxslt1-dev \
    libyaml-dev \
    locales \
    make \
    openssh-client \
    openssh-server \
    openssl \
    python3.8-dev \
    python3.8-distutils \
    python3.8-venv \
    python3.9-dev \
    python3.9-distutils \
    python3.9-venv \
    shellcheck \
    sudo \
    systemd-sysv \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY files/deadsnakes.gpg /etc/apt/keyrings/deadsnakes.gpg
COPY files/deadsnakes.list /etc/apt/sources.list.d/deadsnakes.list

# Install Python versions available from the deadsnakes PPA.
# This is done separately to avoid conflicts with official Ubuntu packages.
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3.7-dev \
    python3.7-distutils \
    python3.7-venv \
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
    rm -rf /var/lib/apt/lists/*

RUN rm /etc/apt/apt.conf.d/docker-clean && \
    ln -s python3 /usr/bin/python && \
    locale-gen en_US.UTF-8

# Install PowerShell using a binary archive.
# This allows pinning to a specific version, and also brings support for multiple architectures.
RUN version="7.3.8" && \
    major_version="$(echo ${version} | cut -f 1 -d .)" && \
    install_dir="/opt/microsoft/powershell/${major_version}" && \
    tmp_file="/tmp/powershell.tgz" && \
    arch="$(uname -i)" && \
    arch=$(if [ "${arch}" = "x86_64" ]; then echo "x64"; \
         elif [ "${arch}" = "aarch64" ]; then echo "arm64"; \
         else echo "unknown arch: ${arch}" && exit 1; fi) && \
    url="https://github.com/PowerShell/PowerShell/releases/download/v${version}/powershell-${version}-linux-${arch}.tar.gz" && \
    echo "URL: ${url}" && \
    curl -sL "${url}" > "${tmp_file}" && \
    mkdir -p "${install_dir}" && \
    tar zxf "${tmp_file}" --no-same-owner --no-same-permissions -C "${install_dir}" && \
    rm "${tmp_file}" && \
    find "${install_dir}" -type f -exec chmod -x "{}" ";" && \
    chmod +x "${install_dir}/pwsh" && \
    ln -s "${install_dir}/pwsh" /usr/bin/pwsh && \
    pwsh --version

ENV container=docker
CMD ["/sbin/init"]

# Install pip last to speed up local container rebuilds.
COPY files/*.py /usr/share/container-setup/
RUN ln -s /usr/bin/python3.12 /usr/share/container-setup/python
RUN /usr/share/container-setup/python -B /usr/share/container-setup/setup.py

# Make sure the pip entry points in /usr/bin are correct.
RUN rm -f /usr/bin/pip3 && cp -av /usr/local/bin/pip3 /usr/bin/pip3 && /usr/bin/pip3 -V && \
    rm -f /usr/bin/pip  && cp -av /usr/local/bin/pip  /usr/bin/pip  && /usr/bin/pip  -V
