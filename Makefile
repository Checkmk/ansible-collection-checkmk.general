SHELL=/bin/bash

VERSION := $$(grep 'version:' galaxy.yml | cut -d ' ' -f 2)

help:
	@echo "setup           - Run all setup target at once."
	@echo ""
	@echo "setup-python    - Prepare the system for development with Python."
	@echo ""
	@echo "setup-vm        - Prepare the system for running the necessary VMs."
	@echo ""
	@echo "vm              - Create a virtual development environment."
	@echo "molecule        - Create a virtual environment for molecule tests."
	@echo ""
	@echo "clean           - Clean up several things"
	@echo "clean-vm        - Clean up virtual development environment."
	@echo ""
	@echo "version         - Update collection version"
	@echo ""
	@echo "Publishing:"
	@echo ""
	@echo "  release       - Build, upload, publish, announce and tag a release"
	@echo "  announce      - Announce the release"
	@echo "  publish       - Make files available, update git and announce"
	@echo ""

release: 

publish:

announce:

setup: setup-python setup-vm

setup-python:
	sudo apt-get -y update --quiet && sudo apt-get -y install python3-pip ca-certificates curl gnupg lsb-release
	python3 -m pip install pip --upgrade
	python3 -m pip install -r requirements.txt

setup-vm:
	@echo
	@echo "This command will alter your system."
	@echo "Do you want to proceed? If not, press CTRL + C!"
	@read
	sudo apt install -y vagrant libvirt-dev
	vagrant plugin install vagrant-libvirt

clean: clean-vm

version:
	@newversion=$$(dialog --stdout --inputbox "New Version:" 0 0 "$(VERSION)") ; \
	if [ -n "$$newversion" ] ; then ./scripts/release.sh -s "$(VERSION)" -t $$newversion ; fi

clean-vm:
	vagrant destroy --force

molecule:
	vagrant up molecule

vm:
	vagrant up collection
