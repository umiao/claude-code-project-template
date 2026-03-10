---
title: Need-To-Knows For Software Security Engineer
permalink: need-to-knows-for-software-security-engineer/
date: 2023-08-31 19:35:51
categories:
- [Job Search, Software Engineering]
tags:
- Cyber Security
- Software Engineering
- Certificate
---


This post covers common software / cyber-security threats and preventions. Including SQL Injection, Cross-Site Scripting (XSS), OS Command Injection, Weak Session Token Generation and Missing Function Level Access Control.
{% asset_img cover.jpg ML_note %}
<!-- more -->



# SQL Injection
{% asset_img SQL.jpg SQL_Injection_Concept_Demonstration %}

## Example of attack:

`SELECT * FROM Users WHERE Username = ‘admin’ AND Password = abc’ OR 1=1;—`
> Here, “abc’ OR 1=1;—” is the constructed malicious input. ‘—’ (double dashes) states end of line.

**Solution**: 
Use parameterized query:

**Wrong Code**:
Straight forward concatenation (trust user’s input as part of the SQL command).
`VALUES (request_user_name “,” + request_user_age + “”)`
	
**Correct Code**:
**Parametrized query**:
`insert_user = db.prepare “INSERT INTO users (name, age) VALUES (?, ?)”
insert_user.execute (request_user_name, request_user_age).`

---

**Other ways of injection attack**:
- **Union attack**: use `UNION` to extend the results returned by the original query.
	It requires both queries to contain the same amount of columns.	

**Conclusion**:
1. All popular dev frameworks have secure construction of db queries.
2. Use allowlist validation on all user input. (e.g., ban the `‘`)
3. Apply least privilege principle on all backend db users.
4. Consider `GET` and `POST` parameters, Cookies and other HTTP headers.

---

# Cross-Site Scripting (XSS)
**Example**: (https://bank.com/search.html?keyword=&#60;script>document.Location=“https://phising.com”&#60;/script>)
The user recognized a valid and known host name is the URL, clicks on the link. Surfs to the URL.

The website (http://bank.com) does not validate or encode the params before rendering / reflecting it back to the user.
Then, the browser may execute the injected JavaScript and redirects the user to a phishing site, tricking them into submitting their passed.

**Prevention**: you should never trust the user input. All user input that is rendered on the application output should be validated or encoded.
The essential is that, if you do not validate the user input, the unescaped input would be displayed in an immediate response to the user. This would allow attacker to perform actions within the application on behalf of other users. Frameworks offer specific API calls to protect the application from XSS by HTML encoding untrusted user input. Cookies should be securely configured. Set the `HttpOnly` flag to prevent scripts from accessing them.

Note that you should not mark strings as “safe”, e.g., `{{recipe_searched|safe}}`. Otherwise, the engine would escape the user input so that they would not got executed / interpreted as html / js. Eliminating such dangerous use cases can help prevent ***Cross-Site Scripting***, which should be already well prevented by the dev framework.

---

# OS Command Injection
Such vulnerability can happen when user controlled input, through parameters, cookies, http headers, etc are passed to the system shell without any prior validation.	

**Example**: url/delete?fileToDelete=aFile.txt;&#183;rm -rf /var/www&#183;
If the application simply appends the `GET` params to the command string, the malicious command would got executed.
Note that in this case, the command would run with the privilege of the running application.
Note that many of the characters needs to be “url encoded” in order to be transferred and parsed correctly.

**Solution**: Use framework specific API calls instead of OS commands, If not possible, validate all user controlled output against a white-list before passing to the shell. Note that you should apply least privilege to the application.
Also,!!! Never set `shell=True`. This would bypass the validation and have it executed in the shell directly.
You can make use of “check_output” to validate if the user provided part is a shell parameter. If not, then you should fail it.


**Remote File Inclusion**
Open any file / Include in the page makes the application vulnerable to remote file inclusion injection. An adversary could upload a malicious script to be executed on the client-side server.
You can specify it as “text/plain” also set security policy to solve the issue.

**File Traverse**
Using the URL GET parameter to open local files makes the application vulnerable to Path Traversal attacks.
An adversary could modify the image parameter path to include any server file in the application page (e.g. `?image=/etc/paswd`).

**Solution**: Remove file response. Also not open server files from URL Get Params.

---
	
# Weak Session Token Generation
If the generation is too weak, an attacker may easily associate to another active user’s session with constructed ID.

**Solution**:
1. Use built-in session management functionalities, instead of inventing your own.
2. Store the session ID in a cookie and then protect session cookies. This can be done by setting an expiry timestamp, path,
“secure” and “HttpOnly” flag and invalidate on logout.
3. Session ID properties must be secure. Make them unpredictable, time limited and single session.
Use a secure communication channel.

---

# Missing Function Level Access Control
**Definition**: user can perform functions that they are not authorized for, or when resources can be accessed by unauthorized users.
When access checks have not been implemented, or when a protection mechanism exists but is not properly configured.

**Solution**:
1. Protect all business functions using a role based authorization mechanism, implemented on the server side.
2. Authorization should be applied using centralized routines, provided by the framework or external modules.
3. Deny access by default. Use least privilege principle.
4. Implement function access control on the server, never the client.