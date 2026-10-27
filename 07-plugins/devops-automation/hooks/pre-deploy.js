#!/usr/bin/env node

/**
 * 배포 전 훅
 * 배포하기 전에 환경과 사전 요구 사항을 검증합니다
 */

async function preDeploy() {
  console.log('Running pre-deployment checks...');

  const { execSync } = require('child_process');

  // kubectl이 설치되어 있는지 확인
  try {
    execSync('which kubectl', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ kubectl not found. Please install Kubernetes CLI.');
    process.exit(1);
  }

  // 클러스터에 연결되어 있는지 확인
  try {
    execSync('kubectl cluster-info', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Not connected to Kubernetes cluster');
    process.exit(1);
  }

  console.log('✅ Pre-deployment checks passed');
}

preDeploy().catch(error => {
  console.error('Pre-deploy hook failed:', error);
  process.exit(1);
});
