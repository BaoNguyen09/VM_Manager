# CloudProvisioner

> **A lightweight backend platform for automating cloud VM instance creation, tracking, and management via a RESTful API.**

---

## 🚀 Overview
Watch a quick demo here 👉: [my awsome video](https://drive.google.com/file/d/1Mxo1PYuymocejEURuKGrrmyoRBb7E2jB/view?usp=sharing)

CloudProvisioner is a simple server-side tool that allows users (or automated systems) to:
- Launch new cloud VM instances on demand
- Monitor instance creation status
- Store and track metadata in a cloud-hosted SQL database
- Retrieve server information through a lightweight REST API

It is similar in spirit to AWS EC2 instance management, but simplified for learning and educational purposes.

This project was completed for **CSC 346: Cloud Computing** at the University of Arizona (Spring 2025).

---

## 🏗️ System Architecture

- **Apache2 Server + CGI Scripts**  
  - Handles incoming requests
  - Talks to cloud provider API to create VMs
  - Connects to SQL database to store server metadata

- **Cloud-hosted SQL Database**  
  - Stores VM instance metadata (`id`, `owner`, `description`, `instance_id`, `ready` status)

- **Background Monitoring Script**  
  - Polls cloud provider API
  - Updates database when VM instance becomes "ready"

- **Cloud Provider**  
  - Actual compute infrastructure for VMs: DigitalOcean

---

## 🗂️ Features

| Feature | Description |
|---------|-------------|
| `create_server` script | Accepts user input to create new VM instances |
| `monitor_new_node` script | Monitors VM creation and updates status |
| `GET /api/servers` | Returns all tracked server instances |
| `GET /api/servers/<id>` | Returns specific server instance metadata |
| Secure VM access | SSH key-based access for managing instances |
| Public IP Exposure | Once ready, servers are accessible via their public IP |

---

## ⚙️ API Endpoints

### 1. List all servers
```
GET /api/servers
```
Returns JSON array of server objects with:
- `id`
- `owner`
- `description`
- `public_ip` (blank if not ready)

### 2. View a single server
```
GET /api/servers/<id>
```
Returns JSON object for a specific server.

---

## 🔐 Security

- **SSH public key authentication** is used to configure access to instances.
- **No password-based logins** are allowed to VM instances (mitigates brute-force attacks).
- **Firewall rules** restrict ports to necessary services only (e.g., 80 for web, 22 for SSH).

---

## 🛠️ Technology Stack

- **Python 3** for CGI scripts
- **Apache2** HTTP server
- **MySQL** cloud database (I use Railway)
- **Cloud API SDKs** (I use Digital Ocean)
- **Bash** scripting (for background monitoring)
- **Linux/Ubuntu** (typical VM OS)

---

## 📋 Setup Instructions (for grading)

1. Clone project files into your CGI directory (`/usr/lib/cgi-bin/` if you use Ubuntu 22.04 (LTS) x64 version)
2. Set up environment variables or a config file for database credentials (never hardcode credentials into scripts).
3. Ensure Python3, MySQLdb, and necessary cloud CLI tools (e.g., `doctl`, `aws`, `gcloud`) are installed.
4. Deploy cloud SQL database according to provided schema (`servers.txt`).
5. Adjust CGI file permissions as needed (`chmod 755`).

---

## 📚 Key Concepts Practiced

- Cloud resource provisioning
- Backend REST API development
- Database integration with cloud services
- SSH key authentication for secure server access
- Basic cloud infrastructure automation
- System design thinking

---

## ✍️ Author

Bao Nguyen  
University of Arizona  
Spring 2025 — CSC 346: Cloud Computing

---

## 🧠 Future Improvements (optional ideas)

- Support for terminating instances (DELETE endpoint)
- Add authentication
