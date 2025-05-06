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

build:
	@echo "Building Collection from current working directory. This can take a while."
	@uv run ansible-galaxy collection build --force ./

install:
	@uv run ansible-galaxy collection install -f ./checkmk-general-$(VERSION).tar.gz

release: version
	# gh workflow run release.yaml --ref main  # https://cli.github.com/manual/gh_workflow_run

announce:
	# See cma scripts announce

version:
	@newversion=$$(dialog --stdout --inputbox "New Version:" 0 0 "$(VERSION)") ; \
	if [ -n "$$newversion" ] ; then ./scripts/release.sh -s "$(VERSION)" -t $$newversion ; fi

setup: setup-python kvm vagrant

python:
	@curl -LsSf https://astral.sh/uv/install.sh | sh

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
		software-properties-common \
		virtiofsd
	@wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
	@echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $$(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
	@sudo apt update -y
	@sudo apt -y install vagrant
	@sudo usermod -aG libvirt $(USER)
	@vagrant plugin install vagrant-libvirt vagrant-reload

venv:
	@uv venv
	@uv sync

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

container: vm
	vagrant ssh collection -c "\
	podman build -t $(CONTAINER_NAME) $(CONTAINER_BUILD_ROOT) --build-arg DL_PW=$$(cat .secret) && \
	podman save $(CONTAINER_NAME):latest > $(COLLECTION_ROOT)/$(CONTAINER_NAME)-latest-image.tar.gz"

tests: tests-linting tests-sanity tests-integration

tests-linting: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	LC_ALL=C.UTF-8 uv run ansible-galaxy collection install ./ && \
	uv run yamllint -c .yamllint ./roles/ && \
	uv run yamllint -c .yamllint ./playbooks/ && \
	LC_ALL=C.UTF-8 uv run ansible-lint -c .ansible-lint ./roles/ && \
	LC_ALL=C.UTF-8 uv run ansible-lint -c .ansible-lint ./playbooks/"

tests-sanity: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	LC_ALL=C.UTF-8 uv run ansible-test sanity --docker"

tests-units: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	LC_ALL=C.UTF-8 uv run ansible-test units --docker"

tests-integration: vm
	@vagrant ssh collection -c "\
	cd $(COLLECTION_ROOT) && \
	LC_ALL=C.UTF-8 uv run ansible-test integration --docker"
