# Cloudflare R2 Storage Setup

FitHire uses Cloudflare R2 for image storage (profile pictures, brand logos, and banners).

## Prerequisites

- Cloudflare account
- R2 subscription (free tier available)

## Setup Steps

### 1. Create R2 Bucket

1. Log in to Cloudflare Dashboard
2. Navigate to **R2 Object Storage**
3. Click **Create bucket**
4. Name your bucket (e.g., `fithire`)
5. Click **Create bucket**

### 2. Enable Public Access

By default, R2 buckets are private. To allow public image access:

1. Go to your bucket's **Settings**
2. Scroll to **Public access**
3. Click **Allow Access** or **Connect Domain**
4. Choose one of these options:

#### Option A: Use R2.dev Subdomain (Recommended for Development)

1. Click **Allow Access**
2. Cloudflare will provide a public URL like: `https://pub-xxxxxxxxxxxxx.r2.dev`
3. Copy this URL - you'll use it as `R2_PUBLIC_URL`

#### Option B: Use Custom Domain (Recommended for Production)

1. Click **Connect Domain**
2. Enter your custom domain (e.g., `media.fithire.com`)
3. Follow the DNS setup instructions
4. Wait for DNS propagation (can take up to 24 hours)
5. Use your custom domain as `R2_PUBLIC_URL`

### 3. Generate API Credentials

1. In Cloudflare Dashboard, go to **R2** → **Manage R2 API Tokens**
2. Click **Create API token**
3. Configure permissions:
   - **Token name**: FitHire Backend
   - **Permissions**: Object Read & Write
   - **Buckets**: Select your bucket (or all buckets)
4. Click **Create API Token**
5. Save these values:
   - **Access Key ID** → Use as `R2_ACCESS_KEY_ID`
   - **Secret Access Key** → Use as `R2_SECRET_ACCESS_KEY`
   - **Jurisdiction-specific endpoint** → Use as `R2_ENDPOINT`

### 4. Configure Environment Variables

Update your Railway environment variables:

```bash
R2_ACCOUNT_ID=<your-cloudflare-account-id>
R2_BUCKET_NAME=fithire
R2_ACCESS_KEY_ID=<your-access-key-id>
R2_SECRET_ACCESS_KEY=<your-secret-access-key>
R2_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com
R2_PUBLIC_URL=<your-public-url-from-step-2>
```

**Important**: Use the public URL from Step 2 (either R2.dev subdomain or your custom domain).

### 5. Test the Setup

1. Deploy the backend with new environment variables
2. Try uploading a profile picture from the frontend
3. Check Railway logs for the generated public URL
4. Verify the image loads in your browser

## Troubleshooting

### Images return 502 errors

**Cause**: Public access is not enabled on your R2 bucket, or the custom domain is not configured correctly.

**Solution**:
- Go to bucket Settings → Public access
- If using custom domain, verify DNS is configured correctly
- Try using the R2.dev subdomain instead

### Images don't load

**Cause**: The R2_PUBLIC_URL doesn't match your bucket's actual public URL.

**Solution**:
- Check your R2 bucket's public URL in Cloudflare Dashboard
- Update R2_PUBLIC_URL in Railway to match exactly
- Redeploy the backend

### 403 Forbidden errors

**Cause**: API credentials don't have the correct permissions.

**Solution**:
- Regenerate API token with Read & Write permissions
- Update R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY in Railway
- Redeploy the backend

## Cost Considerations

Cloudflare R2 pricing (as of 2024):

- **Storage**: $0.015/GB per month (first 10GB free)
- **Class A operations** (upload): $4.50 per million requests
- **Class B operations** (download): $0.36 per million requests
- **Egress**: FREE (no bandwidth charges)

For a startup with 1000 users, expect costs around $1-5/month.

## Security Best Practices

1. **Never commit API credentials** to git (they're in `.env`, which is gitignored)
2. **Use environment variables** for all sensitive values
3. **Rotate API tokens** periodically (every 90 days recommended)
4. **Limit token permissions** to only what's needed (Read & Write, specific bucket)
5. **Monitor usage** in Cloudflare Dashboard to detect anomalies

## Additional Resources

- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [R2 Public Buckets Guide](https://developers.cloudflare.com/r2/buckets/public-buckets/)
- [R2 API Documentation](https://developers.cloudflare.com/r2/api/s3/)
