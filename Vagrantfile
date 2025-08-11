# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'
ENV['VAGRANT_NO_PARALLEL'] = 'yes'

Vagrant.configure("2") do |config|

  # We are using boxes from here: https://app.vagrantup.com/generic

  # Main Box
  config.vm.define "collection", primary: true do |srv|
    srv.vm.box = "generic/debian12"
    srv.vm.network :private_network,
        :ip                         => "192.168.124.42",
        :libvirt__netmask           => "255.255.255.0",
        :libvirt__network_name      => "ansible_collection",
        :libvirt__network_address   => "192.168.124.0"
    srv.ssh.insert_key = false
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used for development of the Checkmk Ansible Collection.'
      libvirt.memory = 8096
      libvirt.cpus = 4
      libvirt.title = 'collection'
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    $script = <<-SCRIPT
    apt-get -y update --quiet
    apt-get -y purge postfix --quiet  # Necessary, as it breaks the upgrade process
    apt-get -y dist-upgrade --quiet
    apt-get -y install ca-certificates curl direnv gnupg lsb-release qemu-guest-agent podman htop
    sudo -u vagrant bash -c "curl -LsSf https://astral.sh/uv/install.sh | sh"
    sudo -u vagrant bash -c "cd /home/vagrant/ansible_collections/checkmk/general/ && /home/vagrant/.local/bin/uv sync"
    sudo -u vagrant bash -c "cd /home/vagrant/ansible_collections/checkmk/general/ && /home/vagrant/.local/bin/uv run ansible-galaxy collection install -f -r /home/vagrant/ansible_collections/checkmk/general/requirements.yml"
    grep "alias ic=" /home/vagrant/.bashrc || echo "alias ic='LC_ALL=C.UTF-8 uv run ansible-galaxy collection build --force ~/ansible_collections/checkmk/general && LC_ALL=C.UTF-8 uv run ansible-galaxy collection install -f ./checkmk-general-*.tar.gz && rm ./checkmk-general-*.tar.gz'" >> /home/vagrant/.bashrc
    grep "alias ap=" /home/vagrant/.bashrc || echo "alias ap='LC_ALL=C.UTF-8 uv run ansible-playbook -i vagrant, '" >> /home/vagrant/.bashrc
    grep "export LC_ALL=C.UTF-8" /home/vagrant/.bashrc || echo "LC_ALL=C.UTF-8" >> /home/vagrant/.bashrc
    hostnamectl set-hostname collection
    SCRIPT
    srv.vm.provision "shell", inline: $script
    srv.vm.provision :reload
    srv.vm.synced_folder "./", "/home/vagrant/ansible_collections/checkmk/general/", type: "virtiofs"
  end

  # Ubuntu
  config.vm.define "ansibuntu", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/ubuntu2204"
    srv.vm.network :private_network,
    :ip                         => "192.168.124.61",
    :libvirt__netmask           => "255.255.255.0",
    :libvirt__network_name      => "ansible_collection",
    :libvirt__network_address   => "192.168.124.0"
    srv.ssh.insert_key = false
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used to test roles against.'
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.title = "ansibuntu"
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    srv.vm.provision "shell",
          inline: "apt-get -y update --quiet && apt-get -y install vim htop curl wget git"
  end

  # Debian
  config.vm.define "debsible", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/debian12"
    srv.vm.network :private_network,
    :ip                         => "192.168.124.62",
    :libvirt__netmask           => "255.255.255.0",
    :libvirt__network_name      => "ansible_collection",
    :libvirt__network_address   => "192.168.124.0"
    srv.ssh.insert_key = false
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used to test roles against.'
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.title = "debsible"
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    srv.vm.provision "shell",
      inline: "apt-get -y update --quiet && apt-get -y install vim htop curl wget git"
  end

  # CentOS Stream
  config.vm.define "anstream", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/centos9s"
    srv.vm.network :private_network,
    :ip                         => "192.168.124.63",
    :libvirt__netmask           => "255.255.255.0",
    :libvirt__network_name      => "ansible_collection",
    :libvirt__network_address   => "192.168.124.0"
    srv.ssh.insert_key = false
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used to test roles against.'
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.title = "anstream"
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    srv.vm.provision "shell",
      inline: "dnf --quiet check-update ; dnf -y install vim curl wget git"
  end

  # openSUSE
  config.vm.define "ansuse", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/opensuse15"
    srv.vm.network :private_network,
    :ip                         => "192.168.124.64",
    :libvirt__netmask           => "255.255.255.0",
    :libvirt__network_name      => "ansible_collection",
    :libvirt__network_address   => "192.168.124.0"
    srv.ssh.insert_key = false
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used to test roles against.'
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.title = "ansuse"
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    srv.vm.provision "shell",
      inline: "zypper --quiet up -y"
  end

  # Oracle Linux
  config.vm.define "ansoracle", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/oracle8"
    srv.vm.network :private_network,
    :ip                         => "192.168.124.66",
    :libvirt__netmask           => "255.255.255.0",
    :libvirt__network_name      => "ansible_collection",
    :libvirt__network_address   => "192.168.124.0"
    srv.ssh.insert_key = false
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used to test roles against.'
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.title = "ansoracle"
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    srv.vm.provision "shell",
      inline: "dnf --quiet check-update ; dnf -y install vim curl wget git"
  end

  # Windows
  config.vm.define "ansidows", autostart: false , primary: false do |srv|
    srv.vm.box = "peru/windows-server-2022-standard-x64-eval"
    srv.vm.network :private_network,
    :ip                         => "192.168.124.67",
    :libvirt__netmask           => "255.255.255.0",
    :libvirt__network_name      => "ansible_collection",
    :libvirt__network_address   => "192.168.124.0"
    srv.winrm.max_tries = 100
    srv.winrm.retry_delay = 2
    srv.vm.boot_timeout = 180
    srv.vm.hostname = "ansidows"
    srv.vm.provider "libvirt" do |libvirt|
      libvirt.default_prefix = "ansible_"
      libvirt.description = 'This box is used to test roles against.'
      libvirt.memory = 4096
      libvirt.cpus = 2
      libvirt.title = "ansidows"
      libvirt.keymap = "de"
      libvirt.memorybacking :access, :mode => 'shared'
      libvirt.memorybacking :source, :type => 'memfd'
    end
    $script = <<-SCRIPT
    Set-NetFirewallRule -name 'FPS-ICMP4-ERQ-In*' -Enabled true
    Get-NetFirewallrule -DisplayName *snmp* | Enable-NetFirewallRule
    Install-WindowsFeature SNMP-Service,SNMP-WMI-Provider -IncludeManagementTools
    Invoke-WebRequest -Uri 'https://www.spice-space.org/download/windows/spice-guest-tools/spice-guest-tools-latest.exe' -OutFile "C:\\tmp\\spice-guest-tools.exe"
    Write-Output "You need to run the spice agent setup manually!"
    Write-Output "Find it at 'C:\\tmp\\spice-guest-tools.exe'"
    SCRIPT
    srv.vm.provision "shell", inline: $script
  end

end
