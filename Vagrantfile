# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'
ENV['VAGRANT_NO_PARALLEL'] = 'yes'

Vagrant.configure("2") do |config|

  # We are using boxes from here: https://app.vagrantup.com/generic

  # Main Box
  config.vm.define "collection", primary: true do |srv|
    srv.vm.box = "generic/ubuntu2204"
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
    add-apt-repository -y ppa:deadsnakes
    apt-get -y install python3-pip ca-certificates curl gnupg lsb-release qemu-guest-agent python3.8 python3.9 python3.10 python3.11 python3.12
    sudo -u vagrant python3 -m pip install pip --upgrade
    sudo -u vagrant python3 -m pip install -r /home/vagrant/ansible_collections/checkmk/general/requirements.txt
    sudo -u vagrant python3 -m pip install -r /home/vagrant/ansible_collections/checkmk/general/qa-requirements.txt
    sudo -u vagrant ansible-galaxy collection install -f -r /home/vagrant/ansible_collections/checkmk/general/requirements.yml
    mkdir -p /home/vagrant/ansible_collections/checkmk/general
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    usermod -aG docker vagrant
    grep "alias ic=" /home/vagrant/.bashrc || echo "alias ic='ansible-galaxy collection build --force ~/ansible_collections/checkmk/general && ansible-galaxy collection install -f ./checkmk-general-*.tar.gz && rm ./checkmk-general-*.tar.gz'" >> /home/vagrant/.bashrc
    grep "alias ap=" /home/vagrant/.bashrc || echo "alias ap='ansible-playbook -i vagrant, '" >> /home/vagrant/.bashrc
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

  # # SLES15 (No Box for libvirt found!!)
  # config.vm.define "ansles", autostart: false , primary: false do |srv|
  #   srv.vm.box = "saltstack/cicd-sles15"
  #   srv.vm.network :private_network,
  #   :ip                         => "192.168.124.64",
  #   :libvirt__netmask           => "255.255.255.0",
  #   :libvirt__network_name      => "ansible_collection",
  #   :libvirt__network_address   => "192.168.124.0"
  #   srv.ssh.insert_key = false
  #   srv.vm.provider "libvirt" do |libvirt|
  #     libvirt.default_prefix = "ansible_"
  #     libvirt.description = 'This box is used to test roles against.'
  #     libvirt.memory = 2048
  #     libvirt.cpus = 2
  #     libvirt.title = "ansles"
  #     libvirt.memorybacking :access, :mode => 'shared'
  #     libvirt.memorybacking :source, :type => 'memfd'
  #   end
  #   srv.vm.provision "shell",
  #     inline: "zypper --quiet up -y"
  # end

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
    srv.vm.box = "peru/windows-server-2019-standard-x64-eval"
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
