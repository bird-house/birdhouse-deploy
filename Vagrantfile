require 'yaml'
config_file=File.expand_path(File.join(File.dirname(__FILE__), 'vagrant_variables.yml'))
settings=YAML.load_file(config_file)

Vagrant.configure("2") do |config|
  config.vagrant.plugins = ["vagrant-disksize", "vagrant-vbguest"]
  config.vm.box = settings.fetch('box', "ubuntu/bionic64")
  config.vm.define settings['hostname']
  config.vm.hostname = settings['hostname']
  # thin provisioning, won't take 100G upfront
  config.disksize.size = settings.fetch('disksize', '100GB')

  # bug https://github.com/hashicorp/vagrant/issues/3341 still happening as of
  # 2019-07-03 with VirtualBox 6.0.8
  if Vagrant.has_plugin?("vagrant-vbguest") then
    # vagrant plugin list
    # vagrant vbguest --status
    # vagrant vbguest --do install  # manual re-install if OS update wiped it
    # Sometime manual re-install do not work, best to take a VM snapshot before OS update for rollback.
    config.vbguest.auto_update = false
  end

  # https://blog.centos.org/2018/01/updated-centos-vagrant-images-available-v1801-01/
  # Fix /vagrant shared folders (together with vagrant-vbguest) for Centos 7.
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  # bridge networking to get real DNS name on local network, PAVICS does not
  # seems to work with numerical IP address for PAVICS_FQDN
  if settings.has_key?('hostip')
    if settings.has_key?('network_bridge')
      config.vm.network "public_network", ip: settings['hostip'], bridge: settings['network_bridge']
    else
      config.vm.network "public_network", ip: settings['hostip']
    end
  else
    if settings.has_key?('network_bridge')
      config.vm.network "public_network", bridge: settings['network_bridge']
    else
      config.vm.network "public_network"
    end
  end

  config.vm.provision :shell, path: "birdhouse/vagrant-utils/provision.sh", env: {"VM_HOSTNAME" => settings['hostname'],
                                                                                  "VM_DOMAIN" => settings['domain'],
                                                                                  "LETSENCRYPT_EMAIL" => settings['letsencrypt_email'],
                                                                                  "KITENAME" => settings.fetch('kitename',''),
                                                                                  "KITESECRET" => settings.fetch('kitesecret',''),
                                                                                  "KITESUBDOMAIN" => settings.fetch('kitesubdomain',''),

                                                                                  }

  if settings.has_key?('ssh_deploy_key')
      config.vm.provision :file, source: settings['ssh_deploy_key'], destination: ".ssh/id_rsa_git_ssh_read_only"
  end

  if settings.has_key?('datasets_dirs')
    settings['datasets_dirs'].each do |mountpoint|
      srcdir = mountpoint['srcdir']
      destdir = mountpoint['destdir']
      config.vm.synced_folder srcdir, destdir, mount_options: ["ro"]
    end
  end

  if settings.has_key?('default_gateway')
      # default router
      config.vm.provision "shell",
        run: "always",
        inline: "route add default gw " + settings['default_gateway']
  end

  config.vm.provider "virtualbox" do |v|
      v.memory = settings.fetch('memory', 10240)
      v.cpus = settings.fetch('cpus', 2)
  end

end

# -*- mode: ruby -*-
# vi: set ft=ruby tabstop=8 expandtab shiftwidth=2 softtabstop=2 :
