# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure("2") do |config|

    # Ubuntu
    config.vm.define "ansibuntu", primary: true do |srv|
        srv.vm.box = "ubuntu/focal64"
        srv.vm.network "private_network", ip: "192.168.56.61"
        srv.ssh.insert_key = false
        srv.vm.provider "virtualbox" do |v|
            v.name = 'ansibuntu'
            v.memory = 1024
            v.cpus = 2
        end
        srv.vm.provision "shell",
            inline: "apt-get -y update --quiet && apt-get -y install vim htop curl wget git"
    end

    # Debian
    config.vm.define "debsible", primary: true do |srv|
        srv.vm.box = "debian/bullseye64"
        srv.vm.network "private_network", ip: "192.168.56.62"
        srv.ssh.insert_key = false
        srv.vm.provider "virtualbox" do |v|
            v.name = 'debsible'
            v.memory = 1024
            v.cpus = 2
        end
        srv.vm.provision "shell",
            inline: "apt-get -y update --quiet && apt-get -y install vim htop curl wget git"
    end

    # CentOS Stream
    config.vm.define "anstream", primary: true do |srv|
        srv.vm.box = "centos/stream8"
        srv.vm.network "private_network", ip: "192.168.56.63"
        srv.ssh.insert_key = false
        srv.vm.provider "virtualbox" do |v|
            v.name = 'anstream'
            v.memory = 1024
            v.cpus = 2
        end
        srv.vm.provision "shell",
            inline: "dnf --quiet check-update ; dnf -y install vim curl wget git"
    end

    # openSUSE Tumbleweed
    config.vm.define "ansuse", primary: true do |srv|
        srv.vm.box = "opensuse/Tumbleweed.x86_64"
        srv.vm.network "private_network", ip: "192.168.56.64"
        srv.ssh.insert_key = false
        srv.vm.provider "virtualbox" do |v|
            v.name = 'ansuse'
            v.memory = 1024
            v.cpus = 2
        end
        srv.vm.provision "shell",
            inline: "zypper --quiet patch-check"
    end
end
