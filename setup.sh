docker build -t example_shiny ./shiny
docker build -t example_dash ./dash
docker build -t rstudio ./rstudio
docker build -t jupyter ./jupyter

groupadd -g 1011 docker_worker
useradd -s /bin/false -u 1010 -g 1020 docker_worker

sudo mkdir /home/users/roz
sudo mkdir /home/users/mew

sudo chown -R docker_worker:docker_worker /home/users
