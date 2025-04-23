# 🧠 PDM40

**PDM40** is a FastAPI-based service that uses OpenAI's GPT models to generate standardized material descriptions with a **maximum of 40 characters**, ideal for SAP or other ERP systems, following Brazilian technical norms.

---

## 🚀 Features

- ✅ Automatically generates concise, standardized PDMs
- 🧠 Strict formatting rules: max 40 characters, uppercase, no special characters
- 🛡️ Rate limiting with `slowapi`
- 🔒 CORS enabled and secure configuration

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pdm40-api.git
cd pdm40-api
```

### 2. Create and activate a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Create a .env file in the project root with your OpenAI key:

```bash
OPEN_AI_KEY=sk-...
```

### 5. Run the application

```bash
fastapi run app/main.py --port 16413
```

---

## 📦 Endpoints

### `POST /pdm`

Generates a PDM (Material Description Pattern) with a strict 40-character limit.

```json
POST /pdm
Content-Type: application/json

{
  "description": "ROLAMENTO FRM REF729068 MARCA FRM REFERENCIA 729068 MATERIAL ACO APLICACOES AUTOMOTIVA INDUSTRIAL"
}
```

Response:

```json
{
  "pdm": "ROLAMENTO RIG ESF 729068 ACO"
}
```

---

## ⚙️ Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [SlowAPI](https://pypi.org/project/slowapi/)

---

## 🔒 PDM Rules

- Max 40 characters
- Must be UPPERCASE
- Only allow letters, numbers, and spaces
- No accents, punctuation, or special characters
- Response will contain only the final PDM string, with no explanation or formatting

---

### Like this project? Give it a star ⭐
