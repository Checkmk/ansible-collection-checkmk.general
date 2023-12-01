FROM quay.io/ansible/base-test-container:6.0.0

COPY requirements /usr/share/container-setup/default/requirements/
COPY freeze /usr/share/container-setup/default/freeze/

RUN pwsh /usr/share/container-setup/default/requirements/sanity.pslint.ps1 -IsContainer && \
    rm -rf /tmp/.dotnet /tmp/Microsoft.PackageManagement

COPY files/pre-build /usr/share/container-setup/pre-build/
COPY files/requirements.py /usr/share/container-setup/
RUN /usr/share/container-setup/python -B /usr/share/container-setup/requirements.py default

COPY files/prime.py files/ansible-test-*.txt /usr/share/container-setup/
RUN /usr/share/container-setup/python -B /usr/share/container-setup/prime.py default
