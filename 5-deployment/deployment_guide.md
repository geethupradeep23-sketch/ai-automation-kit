# Deployment & Implementation Guide

## Prerequisites
- Python 3.8+
- API keys for all integrations (see .env.example)
- Server/hosting (AWS, DigitalOcean, Heroku, etc.)
- Database (PostgreSQL or MongoDB)

## Step 1: Environment Setup

```bash
# Clone repository
git clone https://github.com/geethupradeep23-sketch/ai-automation-kit.git
cd ai-automation-kit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## Step 2: Database Setup

```bash
# Create database
psql -c "CREATE DATABASE automation_kit;"

# Or use MongoDB
mongosh
> use automation_kit
```

## Step 3: Configuration

### Social Media Accounts
Create `config/social-media.json`:
```json
{
  "instagram": {
    "username": "your_username",
    "password": "your_password"
  },
  "twitter": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET"
  }
}
```

### Automation Platform
Create `config/automation.json`:
```json
{
  "make": {
    "api_key": "YOUR_MAKE_API_KEY",
    "organization_id": "YOUR_ORG_ID"
  },
  "zapier": {
    "api_key": "YOUR_ZAPIER_API_KEY"
  }
}
```

## Step 4: Run Locally

```bash
# Start scheduler
python -m 1-social-media.scheduler

# Start monitoring
python -m 1-social-media.monitor

# Start workflow engine
python -m 3-operations.workflow_engine
```

## Step 5: Deploy to Production

### Option A: Heroku
```bash
# Create Procfile
echo "worker: python -m 1-social-media.scheduler" > Procfile

# Deploy
git push heroku main
```

### Option B: AWS EC2
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Follow setup steps above
# Use systemd to manage services

sudo systemctl start automation-kit
sudo systemctl enable automation-kit
```

### Option C: Docker
```bash
# Build image
docker build -t ai-automation-kit .

# Run container
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  ai-automation-kit
```

## Step 6: Monitoring & Maintenance

- Set up error alerts
- Monitor API usage
- Review logs daily
- Test workflows weekly
- Update dependencies monthly

## Troubleshooting

### API Authentication Failed
- Verify API keys in .env
- Check rate limits
- Ensure credentials haven't expired

### Database Connection Error
- Verify database is running
- Check connection string
- Verify firewall rules

### Posts Not Scheduling
- Check scheduler service is running
- Verify social media credentials
- Review error logs
