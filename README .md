# MAC Forgery Lab – Length Extension Attack Demonstration & Mitigation

This project demonstrates the security weakness in using naive hash-based MACs (e.g., MAC = hash(secret || message)) and how a length extension attack can be used to forge valid MACs without knowing the secret key. It also shows how to secure the system using HMAC.

## What Is This All About?

A MAC (Message Authentication Code) is used to ensure that a message has not been tampered with and comes from a trusted sender. It's like a digital signature. However, if the MAC is implemented like this:

    MAC = hash(secret || message)

...then it becomes vulnerable to a **Length Extension Attack**. This is a cryptographic flaw where an attacker, who sees a message and its MAC, can add more data to the message and generate a valid MAC for the new message — without knowing the secret.

In this project, you simulate that attack, then fix it using a proper cryptographic method called **HMAC**.

## Features

- Generate MACs using both insecure (raw hash) and secure (HMAC) methods
- Simulate a length extension attack using the hashpumpy library
- Verify success of forgery in insecure mode
- Show that the same attack fails against HMAC
- Simple web interface using Flask

## Project Structure

```
mac_forgery_lab/
├── app.py        # Flask app   # logic for insecure mode & secure mode
├── templates/
│   └── index.html      # Frontend HTML page
└── README.md           # Project documentation
```

## How It Works

### 2. Demonstration of the Attack

a. **Intercept a valid (message, MAC) pair**  
   - Use the "Generate MAC" button to create a MAC for a chosen message.  
   - Copy the generated MAC.

b. **Perform a length extension attack**  
   - In insecure mode, input the original message, intercepted MAC, and new data to append (e.g., `&admin=true`).  
   - Click "Forge / Verify MAC".

c. **Generate a valid MAC for the extended message**  
   - The app uses the `hashpumpy` library to:
     - Guess key lengths
     - Automatically apply MD5-compatible padding
     - Construct the forged message and valid MAC
     - Compare the forged MAC with the expected server-side MAC

d. **Demonstrate that the server accepts the forged message and MAC**  
   - If successful, the server shows “MAC verified successfully” even though the attacker never knew the secret.

### 3. Mitigation and Defense

a. **Modify the system to use HMAC properly**  
   - Switch the mode to "secure".  
   - MACs are now computed using the `hmac.new()` function.

b. **Demonstrate that the attack fails**  
   - Repeat the attack steps in secure mode.  
   - The server correctly rejects the forged message since HMAC does not allow continuation of the hash state.

## Installation

### Using a Virtual Environment (Recommended)

#### 1. Create the environment

```bash
python -m venv venv
```

#### 2. Activate the environment

- **On Windows:**
```bash
venv\Scripts\activate
```

- **On macOS/Linux:**
```bash
source venv/bin/activate
```

#### 3. Install requirements

```bash
pip install flask hashpumpy hashlib
```

### Run the Lab

```bash
python app.py
```

Open your browser and go to:  
http://localhost:5000

## Explanation of Code and Sequence

### app.py

- Executes the attack using `hashpumpy`
- Simulates message forgery and validation
- Provides both insecure and secure modes
- Insecure: Uses MD5(secret || message)
- Secure: Uses HMAC(secret, message)

### index.html

- Provides a single interface for both modes
- Allows input of original message, MAC, and new data
- Displays output from the server response

## About hashpumpy

**hashpumpy** is a Python binding for the C++ tool `HashPump`, developed by Bryce Cogswell and originally published by the security community to demonstrate how length extension attacks can be automated. It’s widely used in cryptography labs and CTF challenges. The tool handles MD5, SHA1, and SHA256 padding and recomputes forged messages and MACs effectively with only partial knowledge of the original input.

## Team Members

- Mayssoune Hussein Elmasry - 2205251
- Maryam Waheed Zamel - 2205154
- Amina Ahmed Ferra - 2205225

## References

- HMAC RFC 2104 – https://datatracker.ietf.org/doc/html/rfc2104
