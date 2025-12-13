# Yashus Agent Platform

**AI-Powered Digital Marketing Automation Platform**

An enterprise-grade agentic AI boilerplate for building autonomous marketing agents with microservices architecture, featuring the Sales Hunter agent for automated lead generation.

## 🚀 Features

- **Microservices Architecture**: Scalable FastAPI backend with Angular 17 frontend
- **Agentic AI Framework**: Extensible base agent system for building autonomous AI agents
- **Sales Hunter Agent**: Automated lead generation from Google Maps and web sources
- **Docker Support**: Full containerization with Docker Compose
- **CI/CD Pipeline**: Automated testing and deployment to Azure
- **Type Safety**: Full TypeScript and Python type hints
- **Testing**: Comprehensive unit and integration tests
- **Modern Stack**: Latest versions of Angular, Python, FastAPI

> **⚠️ Development Note**: Current implementation uses in-memory storage for tasks (data lost on restart). For production, implement database-backed storage using PostgreSQL or MongoDB. See code comments for guidance.

## 📁 Project Structure

```
yashus/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── agents/            # AI Agent implementations
│   │   │   ├── base_agent.py  # Base agent class
│   │   │   └── sales_hunter_agent.py  # Sales Hunter agent
│   │   ├── api/               # API endpoints
│   │   │   └── endpoints/
│   │   │       ├── agents.py  # Agent management endpoints
│   │   │       └── tasks.py   # Task execution endpoints
│   │   ├── core/              # Core utilities
│   │   │   └── config.py      # Configuration management
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── main.py            # Application entry point
│   ├── tests/                 # Backend tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # Angular 17 Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # UI Components
│   │   │   │   ├── dashboard/
│   │   │   │   ├── agent-list/
│   │   │   │   ├── task-create/
│   │   │   │   └── task-results/
│   │   │   └── services/      # Angular services
│   │   │       └── api.service.ts
│   │   └── environments/
│   ├── Dockerfile
│   └── package.json
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline
├── docker-compose.yml         # Docker orchestration
├── .env.example               # Environment variables template
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Redis** - Caching and message broker
- **Celery** - Task queue
- **OpenAI / LangChain** - AI capabilities
- **Selenium / Playwright** - Web scraping

### Frontend
- **Angular 17** - Modern web framework
- **TypeScript** - Type safety
- **SCSS** - Styling
- **RxJS** - Reactive programming

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Local development
- **GitHub Actions** - CI/CD
- **Azure Container Instances** - Cloud deployment

## 🚦 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

### 1. Clone the Repository

```bash
git clone https://github.com/dlai-sd/yashus.git
cd yashus
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

This will start:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:4200
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 4. Access the Application

- **Frontend Dashboard**: http://localhost:4200
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 💻 Local Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 🎯 Using the Sales Hunter Agent

> **⚠️ Note**: The current implementation uses mock data for demonstration purposes. To use real data:
> - Add your `GOOGLE_MAPS_API_KEY` to `.env` for Google Maps integration
> - Implement web scraping with proper APIs (see code comments for examples)

### Via UI

1. Navigate to http://localhost:4200
2. Click "Create Task"
3. Select "Sales Hunter Agent"
4. Enter:
   - **Search Phrase**: e.g., "restaurants", "dentists"
   - **Location**: e.g., "San Francisco, CA"
   - **Radius**: Search radius in meters (default: 5000)
   - **Max Results**: Maximum number of leads (default: 20)
5. Click "Launch Agent"
6. View results in "Results" tab

### Via API

```bash
# Create a task
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "sales_hunter",
    "config": {
      "search_phrase": "restaurants",
      "location": "San Francisco, CA",
      "radius": 5000,
      "max_results": 20
    }
  }'

# Check task status
curl "http://localhost:8000/api/v1/tasks/{task_id}"

# Get task results
curl "http://localhost:8000/api/v1/tasks/{task_id}/result"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/yashus` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | Application secret key | (required) |
| `OPENAI_API_KEY` | OpenAI API key for AI features | (optional) |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | (optional) |
| `DEBUG` | Debug mode | `False` |

## 🤖 Building New Agents

The platform provides a simple framework for building new agents:

```python
from app.agents.base_agent import BaseAgent, AgentResult, AgentStatus

class MyCustomAgent(BaseAgent):
    """Your custom agent"""
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate task parameters"""
        return "required_field" in task
    
    async def execute(self, task: Dict[str, Any]) -> AgentResult:
        """Execute the agent's task"""
        # Your agent logic here
        
        return AgentResult(
            agent_id=self.agent_id,
            agent_type="my_custom_agent",
            status=AgentStatus.COMPLETED,
            data={"results": "..."},
            started_at=started_at
        )
```

## 📦 Deployment

### Azure Deployment

1. Set up Azure credentials as GitHub secrets:
   - `AZURE_CREDENTIALS`
   - `AZURE_RESOURCE_GROUP`
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

2. Push to main branch:

```bash
git push origin main
```

The CI/CD pipeline will automatically:
- Run tests
- Build Docker images
- Push to Docker Hub
- Deploy to Azure Container Instances

### Manual Deployment

```bash
# Build images
docker-compose build

# Push to registry
docker tag yashus-backend:latest your-registry/yashus-backend:latest
docker push your-registry/yashus-backend:latest

docker tag yashus-frontend:latest your-registry/yashus-frontend:latest
docker push your-registry/yashus-frontend:latest
```

## 🔐 Security

- All API endpoints use CORS protection
- Environment variables for sensitive data
- SQL injection protection via SQLAlchemy
- XSS protection in Angular
- Regular dependency updates

## 📊 API Documentation

Full API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Angular team for Angular 17
- OpenAI for AI capabilities
- The open source community

## 📞 Support

For support, email support@yashus.in or create an issue in the repository.

## 🗺️ Roadmap

- [ ] Additional agent types (SEO, Social Media, Email)
- [ ] Advanced lead scoring with ML
- [ ] Real-time notifications
- [ ] Multi-tenant support
- [ ] Enhanced analytics dashboard
- [ ] Integration with CRM systems
- [ ] Mobile app
- [ ] Agent marketplace

---

**Built with ❤️ for Digital Marketing Automation**
