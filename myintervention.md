# Manual Intervention Points

While the development, testing, and local deployment are automated via the multi-agent coordination strategy, the following points require manual intervention to move the system to a production-ready state or to handle external dependencies.

## 🔑 1. External API Credentials & Secrets
Agents can generate the code, but for security reasons, you must manually provide:
- **Google Cloud Console Setup**: Creating the project, enabling the Google Drive API, and generating the `credentials.json` for OAuth.
- **Remote LLM Keys**: If using fallbacks (OpenAI/Anthropic), you must manually add these keys to the `.env` file.
- **MinIO/S3 Production Credentials**: Setting up non-default access keys and secret keys for a production-grade object storage instance.

## 🌐 2. Production Environment Deployment
- **Domain & SSL**: Manually configuring your DNS settings and purchasing/assigning SSL certificates (e.g., via Let's Encrypt/Certbot).
- **CI/CD Triggers**: Manually pushing the "Production" tag in your repository to trigger the final deployment to your cloud provider (AWS/GCP/DigitalOcean).
- **Database Migrations on Production**: While automated in dev, the first run on a production RDS/Postgres instance should be monitored.

## 🎨 3. Subjective Aesthetic & Tone Approval
- **Neo-Brutalist "Feel"**: While automated snapshots verify borders and colors, a human must decide if the *user experience* feels premium and intuitive enough for the target persona.
- **LLM Tone Tuning**: Reviewing the "Professional" vs "Casual" tone outputs to ensure they align with your specific brand voice.

## 📧 4. Email Service Provider Setup
- **SMTP/SendGrid**: Manually configuring the API key and verified sender address for the system to send completion notifications.

## ⚖️ 5. Legal & Compliance
- **Terms of Service & Privacy Policy**: Manually drafting and placing these files in the public directory to ensure GDPR/regulatory compliance.
- **ISBN/Copyright Information**: Manually entering the official publisher details if the ebooks are intended for commercial distribution.
