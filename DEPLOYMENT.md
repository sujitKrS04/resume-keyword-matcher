# 🚀 Deployment Guide

Complete guide for deploying Resume Keyword Matcher to various platforms.

## Table of Contents

- [Streamlit Cloud (Recommended)](#streamlit-cloud)
- [Heroku](#heroku)
- [Railway](#railway)
- [Docker](#docker)
- [Environment Variables](#environment-variables)

---

## Streamlit Cloud (Recommended)

**Best for**: Quick deployment, free hosting, automatic GitHub sync

### Prerequisites

- GitHub account
- Groq API key (or Gemini API key)
- Optional: SMTP credentials for email features

### Steps

1. **Push to GitHub**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/resume-keyword-matcher.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Advanced settings"

3. **Configure Secrets** (Click "Advanced settings" → "Secrets")

   Add your API keys and SMTP credentials:

   ```toml
   # Primary AI Provider (Recommended)
   GROQ_API_KEY = "gsk_your_groq_api_key_here"

   # Optional: Fallback AI Provider
   GEMINI_API_KEY = "your_gemini_api_key_here"

   # Optional: Email Features
   SMTP_EMAIL = "your_email@gmail.com"
   SMTP_PASSWORD = "your_app_password_here"
   ```

   **Note**: For Gmail SMTP, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

4. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes
   - Your app will be live at `https://your-app-name.streamlit.app`

### Custom Domain (Optional)

1. Go to app settings
2. Click "Custom domain"
3. Follow instructions to configure DNS

---

## Heroku

**Best for**: Professional deployments, custom domains, scaling

### Prerequisites

- Heroku account
- Heroku CLI installed
- Git repository

### Steps

1. **Install Heroku CLI**

   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Windows (use installer from heroku.com)

   # Verify installation
   heroku --version
   ```

2. **Login to Heroku**

   ```bash
   heroku login
   ```

3. **Create Heroku App**

   ```bash
   heroku create resume-keyword-matcher
   # Or let Heroku generate a name
   heroku create
   ```

4. **Create Required Files**

   **Procfile** (create in root directory):

   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   **runtime.txt** (specify Python version):

   ```
   python-3.9.16
   ```

5. **Set Environment Variables**

   ```bash
   heroku config:set GEMINI_API_KEY=your_actual_api_key
   ```

6. **Deploy**

   ```bash
   git add .
   git commit -m "Configure for Heroku"
   git push heroku main
   ```

7. **Open Your App**
   ```bash
   heroku open
   ```

### Troubleshooting Heroku

```bash
# View logs
heroku logs --tail

# Restart app
heroku restart

# Check dyno status
heroku ps
```

---

## Docker

**Best for**: Containerized deployments, Kubernetes, consistent environments

### Create Dockerfile

**Dockerfile**:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml** (optional):

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./:/app
    restart: unless-stopped
```

**.dockerignore**:

```
venv/
__pycache__/
*.pyc
.env
.git/
.gitignore
README.md
.streamlit/secrets.toml
```

### Build and Run

```bash
# Build image
docker build -t resume-matcher .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_api_key \
  resume-matcher

# Or use docker-compose
docker-compose up -d

# View logs
docker logs -f resume-matcher

# Stop container
docker stop resume-matcher
```

### Push to Docker Hub

```bash
# Tag image
docker tag resume-matcher yourusername/resume-matcher:latest

# Login to Docker Hub
docker login

# Push image
docker push yourusername/resume-matcher:latest
```

---

## AWS EC2

**Best for**: Full control, scalability, AWS ecosystem integration

### Launch EC2 Instance

1. **Create Instance**

   - Go to AWS EC2 Console
   - Click "Launch Instance"
   - Choose Amazon Linux 2 or Ubuntu
   - Select t2.micro (free tier)
   - Configure security group:
     - SSH (22) from your IP
     - HTTP (80) from anywhere
     - Custom TCP (8501) from anywhere

2. **Connect to Instance**

   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install Dependencies**

   ```bash
   # Update system
   sudo yum update -y  # Amazon Linux
   # or
   sudo apt update && sudo apt upgrade -y  # Ubuntu

   # Install Python 3.9
   sudo yum install python39 -y  # Amazon Linux
   # or
   sudo apt install python3.9 python3-pip -y  # Ubuntu

   # Install git
   sudo yum install git -y  # Amazon Linux
   # or
   sudo apt install git -y  # Ubuntu
   ```

4. **Clone and Setup**

   ```bash
   # Clone repository
   git clone https://github.com/yourusername/resume-keyword-matcher.git
   cd resume-keyword-matcher

   # Create virtual environment
   python3.9 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Set environment variable
   export GEMINI_API_KEY=your_api_key
   ```

5. **Run with Systemd (Production)**

   Create `/etc/systemd/system/resume-matcher.service`:

   ```ini
   [Unit]
   Description=Resume Keyword Matcher
   After=network.target

   [Service]
   User=ec2-user
   WorkingDirectory=/home/ec2-user/resume-keyword-matcher
   Environment="GEMINI_API_KEY=your_api_key"
   ExecStart=/home/ec2-user/resume-keyword-matcher/venv/bin/streamlit run app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:

   ```bash
   sudo systemctl enable resume-matcher
   sudo systemctl start resume-matcher
   sudo systemctl status resume-matcher
   ```

6. **Setup Nginx (Optional)**

   ```bash
   sudo yum install nginx -y
   sudo systemctl start nginx
   ```

   Configure reverse proxy in `/etc/nginx/conf.d/resume-matcher.conf`:

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

---

## Google Cloud Run

**Best for**: Serverless, auto-scaling, pay-per-use

### Prerequisites

- Google Cloud account
- gcloud CLI installed

### Steps

1. **Install gcloud CLI**

   ```bash
   # Follow instructions at cloud.google.com/sdk/docs/install

   # Initialize
   gcloud init
   ```

2. **Create Dockerfile** (see Docker section above)

3. **Build and Push to Container Registry**

   ```bash
   # Set project
   gcloud config set project YOUR_PROJECT_ID

   # Build image
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/resume-matcher
   ```

4. **Deploy to Cloud Run**

   ```bash
   gcloud run deploy resume-matcher \
     --image gcr.io/YOUR_PROJECT_ID/resume-matcher \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your_api_key
   ```

5. **Access Your App**
   - URL will be provided after deployment
   - Format: `https://resume-matcher-xxxxx-uc.a.run.app`

---

## Environment Variables

### Secure Management

**Streamlit Cloud**: Use Secrets management in dashboard

**Heroku**:

```bash
heroku config:set GEMINI_API_KEY=xxx
```

**Docker**:

```bash
docker run -e GEMINI_API_KEY=xxx ...
# Or use .env file
docker run --env-file .env ...
```

**AWS**: Use AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name gemini-api-key \
  --secret-string your_key
```

---

## Performance Optimization

### Caching

Add to app.py:

```python
@st.cache_data(ttl=3600)
def analyze_resume_cached(resume_text, job_desc):
    return analyze_resume_with_gemini(resume_text, job_desc)
```

### Rate Limiting

Implement request limits to avoid API quota issues.

### CDN

Use Cloudflare or similar CDN for static assets.

---

## Monitoring

### Streamlit Cloud

- Built-in metrics in dashboard
- View logs in real-time

### Heroku

```bash
heroku logs --tail
heroku metrics
```

### Docker

```bash
docker stats
docker logs -f container-name
```

### AWS CloudWatch

- Enable CloudWatch logs
- Set up alarms for errors

---

## SSL/HTTPS

### Streamlit Cloud

- Automatic HTTPS

### Heroku

- Automatic SSL for herokuapp.com domains
- For custom domains: Use Heroku SSL

### AWS

- Use AWS Certificate Manager
- Configure ALB with HTTPS listener

### Let's Encrypt (Self-hosted)

```bash
sudo certbot --nginx -d yourdomain.com
```

---

## Backup & Recovery

### Database Backups

(If you add database in future)

```bash
# PostgreSQL
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql
```

### Application Backups

- Keep code in version control (Git)
- Tag releases: `git tag v1.0.0`
- Use GitHub releases

---

## Scaling

### Vertical Scaling

- Increase dyno/instance size
- Add more RAM/CPU

### Horizontal Scaling

```bash
# Heroku
heroku ps:scale web=3

# Kubernetes
kubectl scale deployment resume-matcher --replicas=3
```

---

## Troubleshooting Deployment

### Common Issues

**Port binding error**:

```python
# Use environment variable for port
port = int(os.environ.get("PORT", 8501))
```

**Module not found**:

```bash
# Ensure requirements.txt is complete
pip freeze > requirements.txt
```

**API key not found**:

- Check environment variable name
- Verify secrets configuration
- Check .env file location

**Build timeout**:

- Optimize Dockerfile layers
- Use smaller base image
- Remove unnecessary files with .dockerignore

---

## Cost Optimization

### Streamlit Cloud

- **Free tier**: 1 private app, unlimited public apps
- **Team plan**: $250/month for private apps

### Heroku

- **Free tier**: Limited hours, sleeps after 30 min
- **Hobby**: $7/month, always on
- **Production**: $25+/month

### AWS EC2

- **t2.micro**: Free tier eligible (750 hours/month)
- **t2.small**: ~$17/month
- Use Reserved Instances for savings

### Google Cloud Run

- **Free tier**: 2 million requests/month
- Pay per use: ~$0.00002400 per request

---

## Security Checklist

- [ ] Use HTTPS
- [ ] Store API keys in environment variables
- [ ] Enable CORS protection
- [ ] Add rate limiting
- [ ] Keep dependencies updated
- [ ] Use secrets management service
- [ ] Enable audit logging
- [ ] Configure security headers
- [ ] Regular security scans
- [ ] Implement authentication (if needed)

---

## Support

For deployment issues:

- Check platform-specific documentation
- Review application logs
- Test locally first
- Open GitHub issue if needed

---

**Good luck with your deployment! 🚀**
