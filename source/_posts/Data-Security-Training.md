---
title: Data & Cyber Security Training Notes
date: 2024-09-15 19:55:57

categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Cyber Security
- Data Security
description: "Notes and revisits of data & cyber security training session."
key_concepts:
  - Data Security
takeaways:
  - SQL injection is prevented by using parameterized queries instead of string concatenation
  - XSS attacks are mitigated through proper output encoding and Content Security Policy headers
  - OS command injection requires allowlist validation on any user input passed to system commands
  - Weak session tokens from predictable generation algorithms enable session hijacking attacks
---
Notes and revisits of data & cyber security training session.
{% asset_img cover.jpg Data and Cyber Security Training cover: SQL injection and security threats %}
<!-- more -->

## SQL Injection
### Example of attack
`SELECT * FROM Users WHERE Username='admin' AND Password = abc'OR 1=1;--`
Here, "abc'OR1=1;--" is the constructed malicious input, and `--` marks the end of line.

**Solution**: Use **parameterized** query.


1. **Wrong Code**: Straight forward concatenantion (trust user's input as part of the SQL command) like `VALUES(request_user_name","+request_user_age+"")`
2. **Correct Code**: Parameterized query. `insert_user = db.prepare "INSERT INTO users(name, age) VALUES(?,?)"`
`insert_user.execute(request_user_name, request_user_age)`

### Other ways of injection attack
**Union attack**: Use `UNION` to extend the results returned by the original query. It requires both queries to contail the **same** amount of columns.

### Conclusion
1. All popular dev frameworks have **secure construction** of db queries.
2. Use **allowist** validation on all user input (e.g. ban the `'`)
3. Apply **least privilege** principle on all backend db users.
4. Consider GET and POST parameters, Cookies and other HTTP headers.


## Cross-Site Scripting (XSS)

The user recognized a valid and known host name is the URL, clicks on the link and surfs to the URL. The website does not validate or encode the params before rendering / reflecting it back to the user. Then, the browser may execute the injected Javascript and redirects the user to a phising site, tricking them into submitting their passwords.

**Prevention**:
1. Never trsut the user input. All user input rendered on the application output should be validated or encoded.
2. If you do not validate the user input, unescaped input would be dispalyed in an immediate response to the user. This would allow attacker to perform actions within the application on behalf of other users.
3. Frameworks offer specific API calls to protect the application from XSS by HTML encoding untrusted user input. 
4. Cookies should be securely configured.
5. Set the `HttpOnly` flag to prevent scripts from accessing them. 
\* Note that you should not mark strings as "safe", e.g. `{{recipe_searchedIssafe}}`; Otherwise, the engine would escape the user input so that they would not got executed / interpreted as html / js.

## OS Command Injection

Such vulnerability can happen when user controlled input, through parameters, cookies, http headers, etc are passed to the system shell without any prior validation.

**Example**: If the application simply appends the GET params to the command string, the malicious command would got executed. Note that in this case, the command would run with the privilege of the **running application**.
Note that many of the characters needs to be "url encoded" in order to be transferred and parsed correctly.

**Solution**:
1. User framework specific API calls instead of OS commands. If not possible, validate all user controlled output against a **white-list** before passing to the shell. 
2. Apply **least privilege** to the application.
3. **Never** set `shell=True`. This would bypass the validation and have it executed in the shell directly.
4. Can make use of "check_output" to validate if the user provided part is a shell parameter. If not, then you should fail it.

---

**Remote File Inclusion**: Open any file / Iclude in the page makes the application vulnearable to remote file inclusion injection.

An adversary could upload a malicious script to be executed on the client-side server. 
You can specify it as "text/plain" also set security policy to solve the issue.

---

**File Traverse**:
Using the URL GET parameter to open local files makes the application vulnerable to **Path Traversal** attacks.


An adversary could modify the iamge parameter path to include any server file in the application page (e.g., `?image=/etc/passwd`) 

**Solution**: Remove file response. Also not open server files from URL GET params.

## Weak Session Token Generation
If the generation is too weak, an attacker may easily associate to another active user's session with constructed ID.
Use **built-in** session management functionalities instead of inventing your own.

- Store the Session ID in a cookie and then protect session cookies. This can be done by setting an **expiry timestamp**, path, "secure" and "HttpOnly" flag and **invalidate** on logout.
- Session ID properties must be secure. Make them **unpredictable**, **time limited** and **single session**.
- Use a secure communication channel.

---

## Missing Function Level Access Control

**Definition**: user can perform functions that they are not authorized for, or when resources can be accessed by **unauthorized** users.

When access checks have not been implemented, or when a protection mechanism exists but is not properly configured.

**Solution**:
1. Protect all business functions using a **role based** authorization mechanism. Implement it on the server side.
2. Authorization should be applied using **centrailized routines**, provided by the framework or external modules.