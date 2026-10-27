#!/bin/bash
set -e

echo "⏪ Starting rollback..."

ENV=${1:-staging}
echo "📦 Target environment: $ENV"

# 이전 배포 가져오기
PREVIOUS=$(kubectl rollout history deployment/app -n $ENV | tail -2 | head -1 | awk '{print $1}')
echo "🔄 Rolling back to revision: $PREVIOUS"

# 롤백 실행
kubectl rollout undo deployment/app -n $ENV

# 롤백 완료 대기
echo "⏳ Waiting for rollback to complete..."
kubectl rollout status deployment/app -n $ENV

# 상태 확인
echo "🏥 Running health checks..."
sleep 5
curl -f http://api.$ENV.example.com/health

echo "✅ Rollback complete!"
