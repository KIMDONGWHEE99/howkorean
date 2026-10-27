#!/usr/bin/env node

/**
 * 배포 후 훅
 * 배포가 끝난 뒤 실행됩니다
 */

async function postDeploy() {
  console.log('Running post-deployment tasks...');

  const { execSync } = require('child_process');

  // 파드가 준비될 때까지 대기
  console.log('Waiting for pods to be ready...');
  try {
    execSync('kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s', {
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('❌ Pods failed to become ready');
    process.exit(1);
  }

  // 스모크 테스트 실행
  console.log('Running smoke tests...');
  // 여기에 스모크 테스트 명령어를 추가하세요

  console.log('✅ Post-deployment tasks complete');
}

postDeploy().catch(error => {
  console.error('Post-deploy hook failed:', error);
  process.exit(1);
});
