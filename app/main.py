from flask import Flask, jsonify, render_template_string
import os
import datetime

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Pipeline — Live</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            min-height: 100vh;
            background: #0d1117;
            font-family: 'Segoe UI', system-ui, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 48px;
            max-width: 680px;
            width: 100%;
            text-align: center;
        }

        .badge {
            display: inline-block;
            background: #1a3a1a;
            color: #3fb950;
            border: 1px solid #3fb950;
            border-radius: 20px;
            padding: 6px 18px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.05em;
            margin-bottom: 24px;
        }

        .checkmark {
            font-size: 64px;
            margin-bottom: 16px;
            display: block;
        }

        h1 {
            color: #e6edf3;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #8b949e;
            font-size: 15px;
            margin-bottom: 40px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 32px;
            text-align: left;
        }

        .info-item {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 14px 16px;
        }

        .info-label {
            color: #8b949e;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .info-value {
            color: #e6edf3;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Courier New', monospace;
        }

        .info-value.green  { color: #3fb950; }
        .info-value.blue   { color: #58a6ff; }
        .info-value.yellow { color: #d29922; }
        .info-value.purple { color: #a371f7; }

        .pipeline-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }

        .stage {
            background: #0d2b1a;
            border: 1px solid #3fb950;
            color: #3fb950;
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
        }

        .arrow {
            color: #30363d;
            font-size: 16px;
        }

        .footer {
            border-top: 1px solid #30363d;
            padding-top: 20px;
            color: #8b949e;
            font-size: 12px;
            line-height: 1.6;
        }

        .footer span {
            color: #58a6ff;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        .live-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #3fb950;
            border-radius: 50%;
            margin-right: 6px;
            animation: pulse 2s ease-in-out infinite;
        }
    </style>
</head>
<body>
    <div class="card">

        <div class="badge">
            <span class="live-dot"></span>DEPLOYED &amp; LIVE
        </div>

        <span class="checkmark">✅</span>

        <h1>Great job, you are deployed!</h1>
        <p class="subtitle">Your CI/CD pipeline ran successfully and this service is live on AWS ECS Fargate</p>

        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Version</div>
                <div class="info-value green">v{{ version }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Environment</div>
                <div class="info-value blue">{{ environment }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Deployed at</div>
                <div class="info-value yellow">{{ deployed_at }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Commit SHA</div>
                <div class="info-value purple">{{ commit_sha }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Service</div>
                <div class="info-value">{{ service }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Status</div>
                <div class="info-value green">healthy</div>
            </div>
        </div>

        <div class="pipeline-row">
            <span class="stage">✓ Test</span>
            <span class="arrow">→</span>
            <span class="stage">✓ Build</span>
            <span class="arrow">→</span>
            <span class="stage">✓ Push ECR</span>
            <span class="arrow">→</span>
            <span class="stage">✓ Deploy ECS</span>
            <span class="arrow">→</span>
            <span class="stage">✓ Live</span>
        </div>

        <div class="footer">
            Built with <span>Terraform</span> · <span>GitHub Actions</span> ·
            <span>Docker</span> · <span>AWS ECS Fargate</span><br>
            Part of a 6-project DevOps portfolio by <span>{{ author }}</span>
        </div>

    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML_PAGE,
        version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("ENVIRONMENT", "dev"),
        commit_sha=os.getenv("COMMIT_SHA", "local"),
        service=os.getenv("SERVICE_NAME", "devops-p02-app"),
        author=os.getenv("AUTHOR_NAME", "DevOps Engineer"),
        deployed_at=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/api/info")
def info():
    return jsonify({
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "commit_sha": os.getenv("COMMIT_SHA", "local"),
        "service": os.getenv("SERVICE_NAME", "devops-p02-app"),
        "status": "healthy",
        "deployed_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)