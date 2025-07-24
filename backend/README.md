 
---

## 🛠️ Troubleshooting: MySQL 'Access denied for user' Error

If you see this error when running your app or tests:

```
pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
```

### 1. Check Your .env File
- Make sure your `.env` file is in the `backend/` directory.
- It should look like:
  ```
  MYSQL_HOST=localhost
  MYSQL_PORT=3306
  MYSQL_USER=root
  MYSQL_PASSWORD=your_real_password
  MYSQL_DB=supplywhiz
  ```
- No extra spaces or quotes. Example: `MYSQL_PASSWORD=password` (not `MYSQL_PASSWORD = "password"`)

### 2. Ensure .env is Loaded
- At the top of `backend/app.py`, add:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
- Install python-dotenv if needed:
  ```bash
  pip install python-dotenv
  ```

### 3. Print the Credentials Used by Your App
Add this to `backend/db.py` **after** the variable assignments:
```python
print("DEBUG: MYSQL_USER =", MYSQL_USER)
print("DEBUG: MYSQL_PASSWORD =", MYSQL_PASSWORD)
print("DEBUG: MYSQL_DB =", MYSQL_DB)
```
Run your app or test and check the output. If you see `None` or an unexpected value, your `.env` is not being loaded.

### 4. Check MySQL User Privileges
- Log in to MySQL and run:
  ```sql
  SHOW GRANTS FOR 'root'@'localhost';
  ```
- Make sure the user has privileges for the database and is allowed to connect from `localhost`.

### 5. Test Manual Connection
- Try connecting with the same credentials using the MySQL CLI:
  ```bash
  mysql -u root -p -h localhost -P 3306
  ```
- If you can’t connect, the password is wrong or the user is not allowed.

### 6. Restart Everything
- Sometimes, environment variables are cached. Restart your terminal, IDE, and MySQL server.

--- 