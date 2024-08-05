SHELL=/bin/bash

VERSION := $$(grep 'version:' galaxy.yml | cut -d ' ' -f 2)

COLLECTION_ROOT="/home/vagrant/ansible_collections/checkmk/general"
CONTAINER_BUILD_ROOT="$(COLLECTION_ROOT)/tests/container"
CONTAINER_NAME="ansible-checkmk-test"

#https://stackoverflow.com/questions/3931741/why-does-make-think-the-target-is-up-to-date
.PHONY: clean

help:
	@echo "setup           			- Run all setup target at once."
	@echo ""
	@echo "python	    			- Prepare the system for development with Python."
	@echo ""
	@echo "kvm			       		- Install and enable KVM."
	@echo ""
	@echo "vagrant   				- Install and enable Vagrant."
	@echo ""
	@echo "venv		       			- Install Python Virtual Environment. You need to activate it yourself though!"
	@echo ""
	@echo "vm           			- Create a virtual development environment."
	@echo "vms						- Create a virtual environment with all boxes (exept for the development ones and ansidows)."
	@echo "vms-debian 	   			- Create a virtual environment with all Debian family OSes."
	@echo "vms-redhat 	   			- Create a virtual environment with all RedHat family OSes."
	@echo "vms-suse 	   			- Create a virtual environment with all Suse family OSes."
	@echo ""
	@echo "container       			- Create a customized container image for testing."
	@echo ""
	@echo "tests	       			- Run all available tests."
	@echo "tests-sanity    			- Run sanity tests."
	@echo "tests-integration    	- Run all integration tests."
	@echo "tests-integration-custom	- Run all integration tests using a custom built image."
	@echo ""
	@echo "clean           			- Clean up several things"
	@echo "clean-vm        			- Clean up virtual development environment."
	@echo ""
	@echo "version         			- Update collection version"
	@echo ""
	@echo "Publishing:"
	@echo ""
	@echo "  release       			- Build, upload, publish, announce and tag a release"
	@echo "  announce      			- Announce the release"
	@echo "  publish       			- Make files available, update git and announce"
	@echo ""

release: version
	# gh workflow run release.yaml --ref main  # https://cli.github.com/manual/gh_workflow_run

announce:
	# See cma scripts announce

version:
	@newversion=$$(dialog --stdout --inputbox "New Version:" 0 0 "$(VERSION)") ; \
	if [ -n "$$newversion" ] ; then ./scripts/release.sh -s "$(VERSION)" -t $$newversion ; fi

setup: setup-python kvm vagrant

python:
	@sudo apt-get -y update --quiet
	@sudo apt-get -y install -y \
		python3-pip \
		python3-venv \
		ca-certificates \
		curl \
		gnupg \
		lsb-release
	@python3 -m pip install pip --upgrade
	@python3 -m pip install -r requirements.txt

kvm:
	@sudo apt update -y
	@sudo apt install -y \
		virt-manager \
		qemu-kvm \
		libvirt-clients \
		libvirt-daemon-system \
		bridge-utils \
		libvirt-daemon\
		libvirt-dev \
		libxslt-dev \
		libxml2-dev \
		zlib1g-dev
	@sudo systemctl enable --now libvirtd

vagrant:
	@sudo apt update -y
	@sudo apt install -y \
		apt-transport-https \
		ca-certificates \
		wget \
		software-properties-common
	@wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
	@echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $$(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
	@sudo apt update -y
	@sudo apt -y install vagrant
	@sudo usermod -aG libvirt $(USER)
	@vagrant plugin install vagrant-libvirt

venv:
	@python3 -m venv venv
	@(. venv/bin/activate && python3 -m pip install pip --upgrade && python3 -m pip install -r requirements.txt)
	@echo
	@echo "Run the following command to actually activate the venv!"
	@echo ". venv/bin/activate"
	@echo

clean:
	@rm -rf .tox/
	@rm -rf ./venv/
	@rm -rf ./tests/output/*
	@vagrant destroy --force

vm:
	@vagrant up collection

vms:
	@vagrant up debsible ansibuntu anstream ansuse ansoracle # ansles ## currently no SLES box for libvirt!

vms-debian:
	@vagrant up debsible ansibuntu

vms-redhat:
	@vagrant up anstream ansoracle

vms-suse:
	@vagrant up ansuse # ansles ## currently no SLES box for libvirt!

vms-windows:
	@vagrant up ansidows

container:
	vagrant ssh collection -c "\
	docker build -t $(CONTAINER_NAME) $(CONTAINER_BUILD_ROOT) --build-arg DL_PW=$$(cat .secret) && \
	docker save $(CONTAINER_NAME):latest > $(COLLECTION_ROOT)/$(CONTAINER_NAME)-latest-image.tar.gz"

tests: tests-linting tests-sanity tests-integration

tests-linting: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	ansible-galaxy collection install ./ && \
	yamllint -c .yamllint ./roles/ && \
	yamllint -c .yamllint ./playbooks/ && \
	ansible-lint -c .ansible-lint ./roles/ && \
	ansible-lint -c .ansible-lint ./playbooks/"

tests-sanity: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	ansible-test sanity --docker"

tests-integration: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	ansible-test integration --docker"

tests-integration-custom: vm container
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	docker load -i ansible-checkmk-test-latest-image.tar.gz && \
	ansible-test integration --docker-privileged --python 3.10 --docker ansible-checkmk-test && \
	ansible-test integration --docker-privileged --python 3.11 --docker ansible-checkmk-test && \
	ansible-test integration --docker-privileged --python 3.12 --docker ansible-checkmk-test"
