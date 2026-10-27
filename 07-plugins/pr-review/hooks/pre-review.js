#!/usr/bin/env node

/**
 * 리뷰 전 훅
 * PR 리뷰를 시작하기 전에 사전 요구 사항을 갖추었는지 확인합니다
 */

async function preReview() {
  console.log('Running pre-review checks...');

  // git 저장소인지 확인
  const { execSync } = require('child_process');
  try {
    execSync('git rev-parse --git-dir', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Not a git repository');
    process.exit(1);
  }

  // 커밋하지 않은 변경 사항이 있는지 확인
  try {
    const status = execSync('git status --porcelain', { encoding: 'utf-8' });
    if (status.trim()) {
      console.warn('⚠️  Warning: Uncommitted changes detected');
    }
  } catch (error) {
    console.error('❌ Failed to check git status');
    process.exit(1);
  }

  console.log('✅ Pre-review checks passed');
}

preReview().catch(error => {
  console.error('Pre-review hook failed:', error);
  process.exit(1);
});
