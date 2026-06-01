<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  HomeFilled,
  VideoPlay,
  Cpu,
  Folder,
  Fold,
  Expand,
  Check,
  Close,
  InfoFilled,
} from '@element-plus/icons-vue'
import { useAnalyzerStore } from '@/stores/analyzer'

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)
const analyzerStore = useAnalyzerStore()
const serverStatus = ref(false)

const activeMenu = computed(() => route.path)

const menuItems = [
  { path: '/', name: '首页', icon: HomeFilled },
  {
    name: '评论爬虫',
    icon: VideoPlay,
    children: [
      { path: '/crawler/bilibili', name: 'B站' },
      { path: '/crawler/zhihu', name: '知乎' },
      { path: '/crawler/netease', name: '网易云' },
      { path: '/crawler/douban', name: '豆瓣' },
    ],
  },
  { path: '/files', name: '文件管理', icon: Folder },
  { path: '/analyzer', name: '检测报告', icon: Cpu },
  { path: '/about', name: '系统说明', icon: InfoFilled },
]

const handleMenuSelect = (path: string) => {
  router.push(path)
}

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

onMounted(async () => {
  serverStatus.value = await analyzerStore.checkServerHealth()
})
</script>

<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <div class="sidebar" :style="{ width: isCollapse ? '64px' : '200px' }">
      <div class="logo">
        <el-icon class="logo-icon"><Cpu /></el-icon>
        <span v-show="!isCollapse" class="logo-text">AIGC检测</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        @select="handleMenuSelect"
      >
        <template v-for="item in menuItems" :key="item.path || item.name">
          <el-menu-item v-if="!item.children" :index="item.path">
            <el-icon>
              <component :is="item.icon" />
            </el-icon>
            <template #title>{{ item.name }}</template>
          </el-menu-item>
          <el-sub-menu v-else :index="item.name">
            <template #title>
              <el-icon>
                <component :is="item.icon" />
              </el-icon>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item v-for="child in item.children" :key="child.path" :index="child.path">
              {{ child.name }}
            </el-menu-item>
          </el-sub-menu>
        </template>
      </el-menu>
    </div>

    <!-- 主内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="header">
        <div class="header-left">
          <el-button type="link" class="collapse-btn" @click="toggleCollapse">
            <el-icon :size="20">
              <Fold v-if="!isCollapse" />
              <Expand v-else />
            </el-icon>
          </el-button>
        </div>
        <div class="header-right">
          <div class="server-status-indicator">
            <el-tooltip :content="serverStatus ? '服务正常运行' : '服务连接失败'">
              <div
                class="status-icon"
                :class="{ 'status-online': serverStatus, 'status-offline': !serverStatus }"
              >
                <el-icon v-if="serverStatus"><Check /></el-icon>
                <el-icon v-else><Close /></el-icon>
              </div>
            </el-tooltip>
            <span class="status-text">{{ serverStatus ? '服务正常' : '服务异常' }}</span>
          </div>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="content-area">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: url('@/assets/首页.jpg') center/cover no-repeat fixed;
  position: relative;
}

.app-layout::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 0;
}

.sidebar {
  background-color: rgba(48, 65, 86, 0.9);
  transition: width 0.3s ease;
  min-width: 64px;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid rgba(31, 45, 61, 0.8);
}

.logo-icon {
  font-size: 24px;
  margin-right: 8px;
}

.logo-text {
  white-space: nowrap;
}

.sidebar-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  position: relative;
  z-index: 1;
}

.header {
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.collapse-btn {
  color: #303133;
  padding: 0;
}

.collapse-btn:hover {
  color: #409eff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.server-status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  border: 1px solid #e4e7ed;
}

.status-icon {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 12px;
}

.status-icon.status-online {
  background: #f0f9eb;
  color: #67c23a;
}

.status-icon.status-offline {
  background: #fef0f0;
  color: #f56c6c;
}

.status-text {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.welcome-text {
  color: #606266;
  font-size: 14px;
}

.content-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: rgba(240, 242, 245, 0.9);
}
</style>
