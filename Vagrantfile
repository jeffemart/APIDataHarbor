Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"  # Escolha a imagem da VM que deseja usar

  (1..4).each do |i|
    config.vm.define "db#{i}" do |node|
      node.vm.network "private_network", type: "dhcp"
      node.vm.provider "virtualbox" do |vb|
        vb.memory = 1024  # Defina a quantidade de memória desejada
        vb.cpus = 1       # Defina a quantidade de CPUs desejada
      end
    end
  end
end