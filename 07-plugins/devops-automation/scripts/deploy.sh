#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# 환경 불러오기
ENV=${1:-staging}
echo "📦 Target environment: $ENV"

# 배포 전 검사
echo "✓ Running pre-deployment checks..."
npm run lint
npm test

# 빌드
echo "🔨 Building application..."
npm run build

# 배포
echo "🚢 Deploying to $ENV..."
kubectl apply -f k8s/$ENV/

# 상태 확인
echo "🏥 Running health checks..."
sleep 10
curl -f http://api.$ENV.example.com/health

echo "✅ Deployment complete!"
