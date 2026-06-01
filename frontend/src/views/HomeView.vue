<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAnalyzerStore } from '@/stores/analyzer'
import { ArrowRight, Download, Search } from '@element-plus/icons-vue'

const router = useRouter()
const analyzerStore = useAnalyzerStore()

const serverStatus = ref(false)

onMounted(async () => {
  serverStatus.value = await analyzerStore.checkServerHealth()
})

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<template>
  <div class="home-view">
    <div class="hero-section">
      <div class="hero-content">
        <h2 class="title">AIGC 多平台评论爬虫与AI率检测系统</h2>
        <p class="subtitle">智能识别AI生成内容，守护网络内容真实性</p>
      </div>
    </div>

    <div class="status-section">
      <div class="action-buttons">
        <el-button type="primary" size="large" @click="navigateTo('/crawler')">
          <el-icon><Download /></el-icon>
          开始爬取
          <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
        <el-button size="large" @click="navigateTo('/analyzer')">
          <el-icon><Search /></el-icon>
          AI检测
          <el-icon class="el-icon--right"><ArrowRight /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  padding: 20px;
}

.hero-section {
  background: url('@/assets/首页.jpg') center/cover no-repeat;
  border-radius: 12px;
  padding: 220px 40px;
  margin-bottom: 10px;
  color: white;
  text-align: center;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 12px;
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
  margin: 0 auto;
}

.title {
  font-size: 42px;
  font-weight: bold;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 24px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.status-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.server-status {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 20px;
}

.action-buttons .el-button {
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
}

.action-buttons .el-button--primary {
  background: white;
  border: 4px solid white;
  color: #000000;
}

.action-buttons .el-button--primary:hover {
  background: rgba(255, 255, 255, 0.8);
  color: #5a67d8;
}

.action-buttons .el-button:not(.el-button--primary) {
  background: white;
  border: 4px solid white;
  color: #000000;
}

.action-buttons .el-button:not(.el-button--primary):hover {
  background: rgba(255, 255, 255, 0.8);
  color: #5a67d8;
}
</style>
