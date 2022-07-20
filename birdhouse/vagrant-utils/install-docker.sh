#!/usr/bin/env bash

set -e # Exit if any subcommand fails
set -x # Print commands for troubleshooting

if ! grep centos /etc/os-release && ! grep rocky /etc/os-release; then

    # Install Docker CE on Ubuntu per
    # https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/

    # From https://github.com/stefanlasiewski/vagrant-ubuntu-docker/blob/756db1689947b1ba6eb360354bc10150c510a52a/install-docker.sh

    # The Docker version may be specified as $1
    if [ $# -eq 1 ]; then
      docker_version=$1
    fi

    # 1. Update the apt package index:

    sudo apt-get --yes --quiet update

    # 2. Install packages to allow apt to use a repository over HTTPS:

    sudo apt-get --yes --quiet install \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common

    # 3. Add Docker’s official GPG key:

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88, by searching for the last 8 characters of the fingerprint.

    sudo apt-key fingerprint 0EBFCD88

    # 4. Use the following command to set up the stable repository. You always need the stable repository, even if you want to install builds from the edge or test repositories as well. To add the edge or test repository, add the word edge or test (or both) after the word stable in the commands below.
    #DOCKER_REPOS="stable edge"
    DOCKER_REPOS="stable"

    sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       $DOCKER_REPOS"

    # INSTALL DOCKER CE

    # 1. Update the apt package index.

    sudo apt-get --yes --quiet update

    # 2. Install the latest version of Docker CE, or go to the next step to install a specific version. Any existing installation of Docker is replaced.
    if [ "$docker_version" ]; then
      sudo apt-get install --yes --quiet docker-ce=$docker_version
    else
      sudo apt-get install --yes --quiet docker-ce
    fi

else

    sudo yum install -y yum-utils

    sudo yum-config-manager \
        --add-repo \
        https://download.docker.com/linux/centos/docker-ce.repo

    sudo yum install -y docker-ce docker-ce-cli containerd.io

    sudo systemctl enable docker
    sudo systemctl start docker

    # net-tools for 'route' command
    sudo yum install -y git net-tools

fi

# 4. Verify that Docker CE is installed correctly by running the hello-world image.

sudo docker run --rm hello-world


# Add current user to group docker to not have to always do 'sudo docker'
sudo usermod -a -G docker $USER
if [ -n "`df -h | grep ^vagrant`" ]; then
    # inside a vagrant box, add user 'vagrant' to group docker for the same reason
    # $USER was 'root' not 'vagrant' during provisionning step
    sudo usermod -a -G docker vagrant
fi

# Add /usr/local/bin to PATH of all users, even root user, so docker-compose
# can be found.
echo 'export PATH="$PATH:/usr/local/bin"' | sudo tee /etc/profile.d/usr_local_path.sh

# install docker-compose, from https://gist.github.com/wdullaer/f1af16bd7e970389bad3
LATEST_COMPOSE_VERSION="`git ls-remote https://github.com/docker/compose | grep refs/tags | grep -oP "v[0-9]+\.[0-9]\.[0-9]+$"|tail -1`"
# LATEST_COMPOSE_VERSION=$(curl --silent https://api.github.com/repos/docker/compose/releases/latest | jq .name -r)  # need jq :(
sudo curl -L "https://github.com/docker/compose/releases/download/$LATEST_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# docker-compose v2 removed the completion file, see https://github.com/docker/compose/issues/8550
#sudo curl -L "https://raw.githubusercontent.com/docker/compose/${LATEST_COMPOSE_VERSION}/contrib/completion/bash/docker-compose" -o /etc/bash_completion.d/docker-compose
docker-compose --version
