# Candidates API

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pyenv (recommended for Python version management)

### Project Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r req.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Starting the Server
1. **Activate virtual environment** (if not already active):
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the API**:
   - Server will start at: `http://127.0.0.1:8000/`
   - API endpoints will be available at: `http://127.0.0.1:8000/api/candidates/`


## Base URL
```
/api/candidates/
```

## Endpoints

### GET /api/candidates/
Returns a list of all candidates.

**Optional Query Parameters:**
- `query` - Search term for case-insensitive name search

**Response:**
Results are sorted by relevance, name length, and alphabetically.

**Example:**
```bash
GET /api/candidates/
GET /api/candidates/?query=john
```

### GET /api/candidates/{id}/
Returns details of a specific candidate.

**Parameters:**
- `id` (required) - The unique identifier of the candidate

**Example:**
```bash
GET /api/candidates/123/
```

### POST /api/candidates/
Creates a new candidate.

**Request Body:**
- Content-Type: `application/json`
- Expects JSON body with candidate data

**Request Body Example:**
```json
{
    "name": "John Doe",
    "age": 28,
    "gender": "Male",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890"
}
```

**Example:**
```bash
curl -X POST /api/candidates/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 28,
    "gender": "Male",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890"
  }'
```

### PUT /api/candidates/{id}/
Fully updates a candidate record.

**Parameters:**
- `id` (required) - The unique identifier of the candidate

**Request Body:**
- Content-Type: `application/json`
- Expects complete candidate data

**Request Body Example:**
```json
{
    "name": "Jane Smith",
    "age": 32,
    "gender": "Female",
    "email": "jane.smith@example.com",
    "phone_number": "+1987654321"
}
```

**Example:**
```bash
curl -X PUT /api/candidates/123/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "age": 32,
    "gender": "Female",
    "email": "jane.smith@example.com",
    "phone_number": "+1987654321"
  }'
```

### PATCH /api/candidates/{id}/
Partially updates a candidate record.

**Parameters:**
- `id` (required) - The unique identifier of the candidate

**Request Body:**
- Content-Type: `application/json`
- Expects partial candidate data

**Request Body Example:**
```json
{
    "email": "updated.email@example.com",
    "phone_number": "+1555123456"
}
```

**Example:**
```bash
curl -X PATCH /api/candidates/123/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated.email@example.com",
    "phone_number": "+1555123456"
  }'
```

### DELETE /api/candidates/{id}/
Deletes a candidate by ID.

**Parameters:**
- `id` (required) - The unique identifier of the candidate

**Example:**
```bash
DELETE /api/candidates/123/
```