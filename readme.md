uses https://github.com/vmware/pyvmomi

this project checks vcenter for virtual machine info and writes to mysql

require these components:
 
#install mysql 

sudo apt policy mariadb-server mariadb-client

sudo apt install mariadb-server mariadb-client

apt policy mariadb-server mariadb-client

#install nginx web server 

sudo apt install nginx

#try to log in mysql

sudo mysql -u root

#install php for frontend

sudo apt install php-imagick php-phpseclib php-php-gettext php7.3-common php7.3-gd php7.3-imap php7.3-json php7.3-curl php7.3-zip php7.3-xml php7.3-mbstring php7.3-bz2 php7.3-intl php7.3-gmp

#configure mysql

sudo mysql_secure_installation

#install mysql module for python3  

pip3 install mysql-connector-python

Usage:

python3 getvmsbycluster.py -s ip_address -u vcenter_username -p password -nossl