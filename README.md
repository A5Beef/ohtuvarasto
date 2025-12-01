# ohtuvarasto

[![CI](https://github.com/A5Beef/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/A5Beef/ohtuvarasto/actions)

[![codecov](https://codecov.io/github/A5Beef/ohtuvarasto/graph/badge.svg?token=QXKF2QJ9B3)](https://codecov.io/github/A5Beef/ohtuvarasto)

## Web User Interface

A Flask-based web user interface is available for managing warehouses.

### Running the Web Application

1. Install Flask:
   ```bash
   pip install flask
   ```

2. Start the application:
   ```bash
   cd src
   python3 app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`

### Configuration

The application supports the following environment variables:

- `FLASK_SECRET_KEY`: Secret key for session management (required for production)
- `FLASK_DEBUG`: Set to `true` to enable debug mode (default: `false`)

Example for development with debug mode:
```bash
export FLASK_DEBUG=true
python3 app.py
```

### Features

- **Create warehouses**: Define capacity and initial balance
- **Edit warehouses**: Modify warehouse name and capacity
- **Delete warehouses**: Remove warehouses from the system
- **Add content**: Increase warehouse inventory
- **Remove content**: Decrease warehouse inventory
- **View statistics**: See capacity, current balance, and available space with visual progress bars

