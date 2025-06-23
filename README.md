# Gen AI Project - Code Generation with IBM Granite

A Flask web application that uses the IBM Granite 3.3-2B Instruct model for code generation, debugging, and analysis.

## Features

- **Code Generation**: Generate code based on natural language prompts
- **Code Debugging**: Analyze code for bugs and provide debugging suggestions
- **Code Explanation**: Get detailed explanations of code functionality
- **Code Optimization**: Optimize code for better performance and readability
- **Multi-language Support**: Support for Python, JavaScript, Java, and more

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd gen-ai-project
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# API Keys and Configuration
GRANITE_API_KEY=your_granite_api_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here_change_this_in_production

# Model Configuration
MODEL_NAME=ibm-granite/granite-3.3-2b-instruct
MAX_LENGTH=2048
TEMPERATURE=0.7
```

### 5. Get API Keys

#### IBM Granite API Key
- Visit the IBM Granite model page on Hugging Face
- You may need to request access to the model
- Get your API key from your IBM account

#### Hugging Face Token (Optional)
- Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
- Create a new token with read permissions
- This is required if you're using private models

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /` - Main application page
- `POST /api/generate` - Generate code from prompt
- `POST /api/debug` - Debug and analyze code
- `POST /api/explain` - Explain code functionality
- `POST /api/optimize` - Optimize code for performance
- `GET /api/health` - Health check endpoint

## Example API Usage

### Generate Code
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to calculate fibonacci numbers",
    "language": "python",
    "max_length": 1024,
    "temperature": 0.7
  }'
```

### Debug Code
```bash
curl -X POST http://localhost:5000/api/debug \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
    "language": "python"
  }'
```

## Configuration

The application uses a configuration system that supports different environments:

- **Development**: Default configuration with debug enabled
- **Production**: Production settings with security checks
- **Testing**: Configuration for running tests

You can set the environment using the `FLASK_ENV` environment variable.

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique secret keys in production
- Keep your API keys secure and rotate them regularly
- The `.gitignore` file is configured to exclude sensitive files

## Troubleshooting

### Model Loading Issues
- Ensure you have sufficient RAM (at least 8GB recommended)
- Check that your GPU drivers are up to date if using CUDA
- Verify your API keys are correct

### Memory Issues
- Reduce `MAX_LENGTH` in your environment variables
- Use a smaller model variant if available
- Consider using model quantization

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here] 