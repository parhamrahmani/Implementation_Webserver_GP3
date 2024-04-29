
# Setting up the Web App for the IT security session

## Installing prerequisites
Assuming you have a Debian-based system, you can install the required packages by running the following command:

1. installing pip3 and venv
```bash
sudo apt update && sudo apt install python3-pip python3-venv
```
2. Install flask and cors
```bash
pip3 install flask flask-cors
```
3. Install Pymysql
```bash
pip3 install pymysql
```
4. Install bcrypt for encryption of the passwords in the database
```bash
pip3 install bcrypt
```
5. Install nginx
```bash
sudo apt install nginx
```


## Database Configuration

### Install and Configure MySQL

1. Install MySQL server:

```bash
sudo apt update && sudo apt install mysql-server
```
2. Configure MySQL:

```bash
sudo mysql_secure_installation
```
3. Log in to MySQL:

```bash
sudo mysql
```
4. Create a new database:
   replace `mydb` with the name of your database and `admin` with the name of your user and `password` with the password of your user.
```sql
CREATE DATABASE mydb2;
USE mydb;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
CREATE TABLE credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
INSERT INTO credentials (user, password) VALUES ('testuser', 'testpassword');

GRANT ALL PRIVILEGES ON mydb.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
5. Exit MySQL:

```sql
exit;
```

6. set the password as an environment variable, so in the app.py file, you can access it.
```bash
export MYDB_PASS=password
```
## Configuring the Nginx server

1. Create a new configuration file for the web app:
```bash
sudo nano /etc/nginx/sites-available/webapp
```

2. Add the following configuration to the file:
```nginx
server {
    listen 80;
    server_name _;  # wildcard

    location / {
        proxy_pass http://127.0.0.1:5000;  # Point to where Flask is running
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
3. Create a symbolic link to the sites-enabled directory:
```bash
sudo ln -s /etc/nginx/sites-available/myflaskapp /etc/nginx/sites-enabled
```
4. Restart the Nginx server:
```bash
sudo systemctl restart nginx
```
5. Check the status of the Nginx server:
```bash
sudo systemctl status nginx
```

## Setting up the Web App

1. Clone the repository from GitHub
2. Navigate to the directory where the repository was cloned and app.py is located
3. Run the following command to start the web app:
```bash
python3 app.py
```
4. Then you should see the following output:
```
❯ python3 app.py
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
5. Open a web browser and navigate to `http://127.0.0.1:5000` to view the web app.

You should see this like the screenshots below:

![Login Page](Documentation/Screenshot%20from%202024-04-29%2022-21-07.png)
![Register Page](Documentation/Screenshot%20from%202024-04-29%2022-21-55.png)
