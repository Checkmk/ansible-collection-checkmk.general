# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  # We are using boxes from here: https://app.vagrantup.com/generic

  # Main Box
  config.vm.define "collection", primary: true do |srv|
    srv.vm.box = "ubuntu/jammy64"
    srv.vm.network "private_network", ip: "192.168.56.42"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'collection'
      v.memory = 6144
      v.cpus = 4
    end
    $script = <<-SCRIPT
    apt-get -y update --quiet
    apt-get -y install python3-pip ca-certificates curl gnupg lsb-release
    wget "https://download.checkmk.com/checkmk/2.1.0p31/check-mk-raw-2.1.0p31_0.jammy_amd64.deb" -O /tmp/checkmk-oldstable.deb
    wget "https://download.checkmk.com/checkmk/2.2.0p7/check-mk-raw-2.2.0p7_0.jammy_amd64.deb" -O /tmp/checkmk-stable.deb
    apt-get install -y /tmp/checkmk-oldstable.deb
    omd create --admin-password 'd7589df1' stable
    apt-get install -y /tmp/checkmk-stable.deb
    omd create --admin-password 'd7589df1' beta
    omd status -b stable || omd start stable
    omd status -b beta || omd start beta
    python3 -m pip install pip --upgrade
    python3 -m pip install -r /vagrant/requirements.txt
    sudo -u vagrant ansible-galaxy collection install -f -r /vagrant/requirements.yml
    mkdir -p /home/vagrant/ansible_collections/checkmk/general
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    usermod -aG docker vagrant
    grep "alias ic=" /home/vagrant/.bashrc || echo "alias ic='ansible-galaxy collection build --force ~/ansible_collections/checkmk/general && ansible-galaxy collection install -f ./checkmk-general-*.tar.gz && rm ./checkmk-general-*.tar.gz'" >> /home/vagrant/.bashrc
    grep "alias ap=" /home/vagrant/.bashrc || echo "alias ap='ansible-playbook -i vagrant, '" >> /home/vagrant/.bashrc
    SCRIPT
    srv.vm.provision "shell", inline: $script
    srv.vm.synced_folder "./", "/home/vagrant/ansible_collections/checkmk/general/"
  end
  
  # Main Box Old
  config.vm.define "molecule", autostart: false , primary: false do |srv|
    srv.vm.box = "ubuntu/focal64"
    srv.vm.network "private_network", ip: "192.168.56.42"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'molecule'
      v.memory = 6144
      v.cpus = 4
    end
    $script = <<-SCRIPT
    apt-get -y update --quiet
    apt-get -y install python3-pip ca-certificates curl gnupg lsb-release
    wget "https://download.checkmk.com/checkmk/2.1.0p31/check-mk-raw-2.1.0p31_0.focal_amd64.deb" -O /tmp/checkmk-oldstable.deb
    wget "https://download.checkmk.com/checkmk/2.2.0p7/check-mk-raw-2.2.0p7_0.focal_amd64.deb" -O /tmp/checkmk-stable.deb
    apt-get install -y /tmp/checkmk-oldstable.deb
    omd create --admin-password 'd7589df1' stable
    apt-get install -y /tmp/checkmk-stable.deb
    omd create --admin-password 'd7589df1' beta
    omd status -b stable || omd start stable
    omd status -b beta || omd start beta
    python3 -m pip install pip --upgrade
    python3 -m pip install -r /vagrant/requirements.txt
    python3 -m pip install molecule molecule-plugins[docker]
    sudo -u vagrant ansible-galaxy collection install -f -r /vagrant/requirements.yml
    mkdir -p /home/vagrant/ansible_collections/checkmk/general
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    usermod -aG docker vagrant
    grep "alias ic=" /home/vagrant/.bashrc || echo "alias ic='ansible-galaxy collection build --force ~/ansible_collections/checkmk/general && ansible-galaxy collection install -f ./checkmk-general-*.tar.gz && rm ./checkmk-general-*.tar.gz'" >> /home/vagrant/.bashrc
    grep "alias ap=" /home/vagrant/.bashrc || echo "alias ap='ansible-playbook -i vagrant, '" >> /home/vagrant/.bashrc
    SCRIPT
    srv.vm.provision "shell", inline: $script
    srv.vm.synced_folder "./", "/home/vagrant/ansible_collections/checkmk/general/"
  end

  # Ubuntu
  config.vm.define "ansibuntu", autostart: false , primary: false do |srv|
    srv.vm.box = "ubuntu/jammy64"
    srv.vm.network "private_network", ip: "192.168.56.61"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'ansibuntu'
      v.memory = 2048
      v.cpus = 2
    end
    srv.vm.provision "shell",
          inline: "apt-get -y update --quiet && apt-get -y install vim htop curl wget git"
  end

  # Debian
  config.vm.define "debsible", autostart: false , primary: false do |srv|
    srv.vm.box = "debian/bookworm64"
    srv.vm.network "private_network", ip: "192.168.56.62"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'debsible'
      v.memory = 2048
      v.cpus = 2
    end
    srv.vm.provision "shell",
      inline: "apt-get -y update --quiet && apt-get -y install vim htop curl wget git"
  end

  # CentOS Stream
  config.vm.define "anstream", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/centos9s"
    srv.vm.network "private_network", ip: "192.168.56.63"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'anstream'
      v.memory = 2048
      v.cpus = 2
    end
    srv.vm.provision "shell",
      inline: "dnf --quiet check-update ; dnf -y install vim curl wget git"
  end

  # openSUSE
  config.vm.define "ansuse", autostart: false , primary: false do |srv|
    srv.vm.box = "opensuse/Tumbleweed.x86_64"
    srv.vm.network "private_network", ip: "192.168.56.64"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'ansuse'
      v.memory = 2048
      v.cpus = 2
    end
    srv.vm.provision "shell",
      inline: "zypper --quiet up -y"
  end

  # SLES15
  config.vm.define "ansles", autostart: false , primary: false do |srv|
    srv.vm.box = "saltstack/cicd-sles15"
    srv.vm.network "private_network", ip: "192.168.56.65"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'ansles'
      v.memory = 2048
      v.cpus = 2
    end
    srv.vm.provision "shell",
      inline: "zypper --quiet up -y"
  end


  # Oracle Linux
  config.vm.define "ansoracle", autostart: false , primary: false do |srv|
    srv.vm.box = "generic/oracle8"
    srv.vm.network "private_network", ip: "192.168.56.66"
    srv.ssh.insert_key = false
    srv.vm.provider "virtualbox" do |v|
      v.name = 'ansoracle'
      v.memory = 2048
      v.cpus = 2
    end
    srv.vm.provision "shell",
      inline: "dnf --quiet check-update ; dnf -y install vim curl wget git"
  end

end
