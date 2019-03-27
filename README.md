# Data Science Portal

A portal to RStudio and Jupyter with ability to host Shiny and Dash apps. 

## Background

This uses [shinyproxy](https://www.shinyproxy.io/) under the hood to manage login and etc.  Thi assumes you'll be running on a linux system. 

## Getting started

1. Make sure `docker` and `docker-compose` are installed. 
2. Clone this repo
3. Build docker images for example apps

``` sh
docker build -t example_shiny ./shiny
docker build -t example_dash ./dash
docker build -t rstudio ./rstudio
docker build -t jupyter ./jupyter
```

4. Create a docker user/group for managing mounted home dirs in rstudio and jupyter. [more info](https://blog.stefanproell.at/2018/08/08/jupyter-docker-stacks-with-a-custom-user/)

``` sh
groupadd -g 1011 docker_worker
useradd -s /bin/false -u 1010 -g 1020 docker_worker
```

Give the users home directories and pass ownership to the `docker_worker`

```
# these are my cats - they are data scientists too...
sudo mkdir /home/users/mau
sudo mkdir /home/users/mau
sudo chown -R docker_worker:docker_worker /home/users
```

5. Run `docker-compose up` to start the data science portal

``` sh
docker compose up
```

