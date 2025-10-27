# Detailed Deployment Guide

## Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] `.env.example` updated with all variables
- [ ] Static files in `static/` directory
- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] API keys ready (Anthropic/OpenAI/OpenRouter)

## Platform-Specific Guides

### 1. Render (Recommended for Beginners)

**Pros:**
- Free tier available
- Easy setup
- Auto-deploy from GitHub
- Built-in SSL

**Steps:**

1. **Sign up** at https://render.com

2. **New Web Service** → Connect GitHub repository

3. **Configuration:**
```
   Name: ee-research-scout
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
```

4. **Environment Variables** (click "Add Environment Variable"):
   - `LLM_PROVIDER` = `anthropic`
   - `ANTHROPIC_API_KEY` = `your_actual_key`
   - `ANTHROPIC_MODEL` = `claude-sonnet-4-5-20250929`
   - `PORT` = `8000`
   - `HOST` = `0.0.0.0`

5. **Create Web Service** - deployment starts automatically

6. **Access your app** at: `https://ee-research-scout.onrender.com`

**Free Tier Limitations:**
- Sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month free

**Upgrade to Paid ($7/month):**
- Always-on service
- Better performance
- More CPU/memory

---

### 2. Railway (Best for Simplicity)

**Pros:**
- $5 free credits monthly
- Very simple setup
- Good performance
- Modern dashboard

**Steps:**

1. **Sign up** at https://railway.app

2. **New Project** → **Deploy from GitHub repo**

3. **Select repository** and branch

4. **Add Variables** (click Variables tab):
```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_key_here
   ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
   PORT=8000
```

5. **Generate Domain** - Railway auto-generates a URL

6. **Deploy** - automatic deployment starts

**Pricing:**
- $5 free credits/month
- Pay-as-you-go after free credits
- ~$0.000463/GB-hr for RAM

---

### 3. Fly.io (Most Cost-Effective)

**Pros:**
- 3 free VMs (256MB each)
- Global edge deployment
- Low latency worldwide

**Steps:**

1. **Install Fly CLI:**
```bash
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   
   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

2. **Login:**
```bash
   fly auth login
```

3. **Initialize:**
```bash
   cd ee-research-scout-agent
   fly launch
```
   
   Answer prompts:
   - App name: `ee-research-scout`
   - Region: Choose closest to you
   - Database: No
   - Deploy now: No

4. **Set secrets:**
```bash
   fly secrets set LLM_PROVIDER=anthropic
   fly secrets set ANTHROPIC_API_KEY=your_key_here
   fly secrets set ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
```

5. **Deploy:**
```bash
   fly deploy
```

6. **Access:**
```bash
   fly open
```

**Free Tier:**
- 3 shared-cpu VMs
- 256MB RAM each
- 3GB persistent storage

---

### 4. Heroku

**Note:** Heroku removed free tier. Minimum $5/month.

**Steps:**

1. **Install Heroku CLI:**
```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Ubuntu
   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
   
   # Windows
   # Download installer from heroku.com
```

2. **Login:**
```bash
   heroku login
```

3. **Create app:**
```bash
   heroku create ee-research-scout
```

4. **Set environment variables:**
```bash
   heroku config:set LLM_PROVIDER=anthropic
   heroku config:set ANTHROPIC_API_KEY=your_key_here
   heroku config:set ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
```

5. **Deploy:**
```bash
   git push heroku main
```

6. **Open app:**
```bash
   heroku open
```

**Pricing:**
- Eco Dynos: $5/month (sleeps after 30min inactivity)
- Basic Dynos: $7/month (always-on)

---

### 5. Google Cloud Run (Advanced)

**Pros:**
- Pay only for actual usage
- Scales to zero (no cost when idle)
- Free tier: 2 million requests/month

**Steps:**

1. **Install gcloud CLI**

2. **Authenticate:**
```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
```

3. **Build container:**
```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ee-research-scout
```

4. **Deploy:**
```bash
   gcloud run deploy ee-research-scout \
     --image gcr.io/YOUR_PROJECT_ID/ee-research-scout \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars LLM_PROVIDER=anthropic,ANTHROPIC_API_KEY=your_key
```

---

## Neo4j Deployment (Optional)

If using knowledge graph features:

### Neo4j Aura (Free Tier)

1. Sign up at https://neo4j.com/cloud/aura/
2. Create free database
3. Save credentials
4. Add to environment variables:
```
   NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
```

---

## Performance Optimization

### For Free Tiers

1. **Enable keep-alive pinging:**
   - Use UptimeRobot or similar to ping every 5 minutes
   - Prevents Render/Heroku from sleeping

2. **Optimize cold starts:**
   - Minimize dependencies
   - Use smaller Docker base images

3. **Cache responses:**
   - Implement Redis caching for common queries
   - Store results in memory

### For Production

1. **Use CDN** for static assets (Cloudflare)
2. **Enable response caching**
3. **Database connection pooling**
4. **Horizontal scaling** (multiple instances)

---

## Monitoring

### Free Tools

**UptimeRobot** (uptime monitoring):
```
https://uptimerobot.com
```

**LogTail** (log aggregation):
```
https://logtail.com
```

**Sentry** (error tracking):
```bash
pip install sentry-sdk
```

Add to `app.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## Security Best Practices

1. **Never commit API keys** to GitHub
   - Use `.env` for local development
   - Use platform secrets for deployment

2. **Use HTTPS only** (all platforms provide free SSL)

3. **Rate limiting:**
```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   
   @limiter.limit("10/minute")
   async def assist_endpoint():
       pass
```

4. **Input validation:**
   - Sanitize user queries
   - Limit query length
   - Block malicious patterns

---

## Cost Estimation

### Monthly Costs (Estimated)

**Hobby Project (Low Traffic):**
- Render Free Tier: $0
- Railway: $5 (free credits)
- Fly.io: $0-2
- API Calls (Claude): $10-30

**Small Business (Moderate Traffic):**
- Render Starter: $7
- Railway: $10-20
- Fly.io: $5-10
- API Calls: $50-150
- **Total: ~$75-200/month**

**Enterprise (High Traffic):**
- Cloud hosting: $50-200
- API calls: $500-2000
- CDN: $20-50
- Monitoring: $50-100
- **Total: ~$650-2500/month**

---

## Support

For deployment issues:
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Fly.io**: https://fly.io/docs
- **GitHub Issues**: [your-repo]/issues