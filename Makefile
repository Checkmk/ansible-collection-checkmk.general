SHELL=/bin/bash

VERSION := $$(grep 'version:' galaxy.yml | cut -d ' ' -f 2)

COLLECTION_ROOT="/home/vagrant/ansible_collections/checkmk/general"
CONTAINER_BUILD_ROOT="$(COLLECTION_ROOT)/tests/container"
CONTAINER_NAME="ansible-checkmk-test"

help:
	@echo "setup           				- Run all setup target at once."
	@echo ""
	@echo "setup-python    				- Prepare the system for development with Python."
	@echo ""
	@echo "setup-kvm       				- Install and enable KVM and prepare Vagrant."
	@echo ""
	@echo "kvm             				- Only copy the correct Vagrantfile for use with KVM."
	@echo ""
	@echo "setup-vbox 	     			- Copy the correct Vagrantfile for use with VirtualBox."
	@echo ""
	@echo "vbox 	           			- Copy the correct Vagrantfile for use with VirtualBox."
	@echo ""
	@echo "vm              - Create a virtual development environment."
	@echo "molecule        - Create a virtual environment for molecule tests."
	@echo "vms        	   - Create a virtual environment with all boxes (exept for the development ones and ansidows)."
	@echo "vms-debian 	   - Create a virtual environment with all Debian family OSes."
	@echo "vms-redhat 	   - Create a virtual environment with all RedHat family OSes."
	@echo "vms-suse 	   - Create a virtual environment with all Suse family OSes."
	@echo ""
	@echo "container       				- Create a customized container image for testing."
	@echo ""
	@echo "tests	       				- Run all available tests."
	@echo "tests-sanity    				- Run sanity tests."
	@echo "tests-integration    		- Run all integration tests."
	@echo "tests-integration-custom		- Run all integration tests using a custom built image."
	@echo ""
	@echo "clean           				- Clean up several things"
	@echo "clean-vm        				- Clean up virtual development environment."
	@echo ""
	@echo "version         				- Update collection version"
	@echo ""
	@echo "Publishing:"
	@echo ""
	@echo "  release       				- Build, upload, publish, announce and tag a release"
	@echo "  announce      				- Announce the release"
	@echo "  publish       				- Make files available, update git and announce"
	@echo ""

release: version
	# gh workflow run release.yaml --ref main  # https://cli.github.com/manual/gh_workflow_run

announce:
	# See cma scripts announce

version:
	@newversion=$$(dialog --stdout --inputbox "New Version:" 0 0 "$(VERSION)") ; \
	if [ -n "$$newversion" ] ; then ./scripts/release.sh -s "$(VERSION)" -t $$newversion ; fi

setup: setup-python setup-kvm

setup-python:
	@sudo apt-get -y update --quiet
	@sudo apt-get -y install -y \
		python3-pip \
		ca-certificates \
		curl \
		gnupg \
		lsb-release
	@python3 -m pip install pip --upgrade
	@python3 -m pip install -r requirements.txt

kvm:
	if [ -f Vagrantfile ] ; then cp Vagrantfile Vagrantfile.bak ; fi
	cp Vagrantfile.kvm Vagrantfile
	if [ -f playbooks/hosts ] ; then cp playbooks/hosts playbooks/hosts.bak ; fi
	cp playbooks/hosts.kvm playbooks/hosts

setup-kvm: kvm
	@sudo apt update -y
	@sudo apt install -y \
		virt-manager \
		qemu-kvm \
		libvirt-clients \
		libvirt-daemon-system \
		bridge-utils \--build-arg DL_PW=$$(cat .secret)
		libvirt-daemon\
		libvirt-dev \
		libxslt-dev \
		libxml2-dev \
		zlib1g-dev
	@sudo systemctl enable --now libvirtd
	@vagrant plugin install vagrant-libvirt

vbox:
	if [ -f Vagrantfile ] ; then cp Vagrantfile Vagrantfile.bak ; fi
	cp Vagrantfile.vbox Vagrantfile
	if [ -f playbooks/hosts ] ; then cp playbooks/hosts playbooks/hosts.bak ; fi
	cp playbooks/hosts.vbox playbooks/hosts

setup-vbox: vbox

clean: clean-vm

clean-vm:
	@vagrant destroy --force

molecule:
	@vagrant up molecule

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

container: molecule
	vagrant ssh molecule -c "\
	docker build -t $(CONTAINER_NAME) $(CONTAINER_BUILD_ROOT) --build-arg DL_PW=$$(cat .secret) && \
	docker save $(CONTAINER_NAME):latest > $(COLLECTION_ROOT)/$(CONTAINER_NAME)-latest-image.tar.gz"

tests: tests-sanity tests-integration

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
