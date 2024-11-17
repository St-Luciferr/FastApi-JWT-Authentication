# FastAPI Project with JWT Authentication (RSA Signing)

This project implements JWT authentication using RSA key pair for signing and verifying tokens. It uses FastAPI for the backend and SQLAlchemy for database interaction.

## Prerequisites

Make sure you have the following installed:
- Python 3
- `pip` (Python package installer)

---
### Example `.env` file:
Copy this inside a `.env` file in your project directory.
```env
DATABASE_URL='postgresql://<user>:<password>@<host>:<port>/<dbname>'
RSA_PRIVATE_KEY_PATH='rsa_keys/private.pem'
RSA_PUBLIC_KEY_PATH='rsa_keys/public.pem'
```

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/St-Luciferr/FastApi-JWT-Authentication
cd "FastApi-JWT-Authentication"
```

### 2. Create Virtual Environment
It’s recommended to use a virtual environment to manage project dependencies.
```bash
python -m venv .venv
```
### 3. Activate Virtual Environment
* On Windows:
```bash
 .venv\Scripts\activate
```
* On Linux:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
---
## Setting Up RSA Keys for JWT
### 5. Generate RSA Key Pair
The project uses RSA keys to sign and verify JWT tokens.
#### Generate the Private and Public Keys
Run the following commands to generate a private key (private.pem) and a public key (public.pem):
```bash
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
```
```bash
openssl rsa -pubout -in private.pem -out public.pem
```

#### Store the Keys
Make sure to save private.pem and public.pem securely in your project directory inside folder `rsa_keys`. These files are required for signing and verifying JWT tokens.

## Running the Project

### 6. Run the FastAPI Development Server
With the virtual environment activated and dependencies installed, you can run the FastAPI application:

```bash
uvicorn main:app --reload
```