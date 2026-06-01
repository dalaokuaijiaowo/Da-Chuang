<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCrawlerStore } from '@/stores/crawler'
import { ElMessage } from 'element-plus'
import { VideoPlay, Document, ChatDotRound, Headset, Collection, Loading } from '@element-plus/icons-vue'

const route = useRoute()
const crawlerStore = useCrawlerStore()
const activeTab = ref('bilibili-video')

// 根据路由设置默认tab
const updateActiveTabFromRoute = () => {
  const path = route.path
  if (path.includes('/crawler/bilibili')) {
    activeTab.value = 'bilibili-video'
  } else if (path.includes('/crawler/zhihu')) {
    activeTab.value = 'zhihu'
  } else if (path.includes('/crawler/netease')) {
    activeTab.value = 'netease'
  } else if (path.includes('/crawler/douban')) {
    activeTab.value = 'douban'
  }
}

// 初始化时设置tab
updateActiveTabFromRoute()

// 监听路由变化
watch(() => route.path, updateActiveTabFromRoute)

const bilibiliVideoForm = reactive({
  bv: '',
  isSecond: true,
})

const bilibiliDynamicForm = reactive({
  opus: '',
  isSecond: true,
})

const zhihuForm = reactive({
  answerId: '',
  maxCount: 500,
})

const neteaseForm = reactive({
  songId: null as number | null,
})

const doubanForm = reactive({
  maxBooks: 5,
})

// 爬取进度对话框
const crawlDialogVisible = ref(false)
const crawlTaskName = ref('')
const crawlStatus = ref('')

const handleCrawlVideo = async () => {
  if (!bilibiliVideoForm.bv) {
    ElMessage.warning('请输入BV号')
    return
  }
  try {
    crawlTaskName.value = `B站视频评论 (${bilibiliVideoForm.bv})`
    crawlStatus.value = '爬取中，请耐心等待...'
    crawlDialogVisible.value = true

    await crawlerStore.crawlVideo(bilibiliVideoForm.bv, bilibiliVideoForm.isSecond)
    ElMessage.success('爬取成功')
    crawlDialogVisible.value = false
  } catch {
    ElMessage.error('爬取失败')
    crawlDialogVisible.value = false
  }
}

const handleCrawlDynamic = async () => {
  if (!bilibiliDynamicForm.opus) {
    ElMessage.warning('请输入动态ID')
    return
  }
  try {
    crawlTaskName.value = `B站动态评论 (${bilibiliDynamicForm.opus})`
    crawlStatus.value = '爬取中，请耐心等待...'
    crawlDialogVisible.value = true

    await crawlerStore.crawlDynamic(bilibiliDynamicForm.opus, bilibiliDynamicForm.isSecond)
    ElMessage.success('爬取成功')
    crawlDialogVisible.value = false
  } catch {
    ElMessage.error('爬取失败')
    crawlDialogVisible.value = false
  }
}

const handleCrawlZhihu = async () => {
  if (!zhihuForm.answerId) {
    ElMessage.warning('请输入回答ID')
    return
  }
  try {
    crawlTaskName.value = `知乎回答评论 (${zhihuForm.answerId})`
    crawlStatus.value = '爬取中，请耐心等待...'
    crawlDialogVisible.value = true

    await crawlerStore.crawlZhihu(zhihuForm.answerId, zhihuForm.maxCount)
    ElMessage.success('爬取成功')
    crawlDialogVisible.value = false
  } catch {
    ElMessage.error('爬取失败')
    crawlDialogVisible.value = false
  }
}

const handleCrawlNetease = async () => {
  if (!neteaseForm.songId) {
    ElMessage.warning('请输入歌曲ID')
    return
  }
  try {
    crawlTaskName.value = `网易云音乐评论 (${neteaseForm.songId})`
    crawlStatus.value = '爬取中，请耐心等待...'
    crawlDialogVisible.value = true

    await crawlerStore.crawlNetease(neteaseForm.songId)
    ElMessage.success('爬取成功')
    crawlDialogVisible.value = false
  } catch {
    ElMessage.error('爬取失败')
    crawlDialogVisible.value = false
  }
}

const handleCrawlDouban = async () => {
  try {
    crawlTaskName.value = `豆瓣月度热书 (${doubanForm.maxBooks}本)`
    crawlStatus.value = '爬取中，请耐心等待...'
    crawlDialogVisible.value = true

    await crawlerStore.crawlDouban(doubanForm.maxBooks)
    ElMessage.success('爬取成功')
    crawlDialogVisible.value = false
  } catch {
    ElMessage.error('爬取失败')
    crawlDialogVisible.value = false
  }
}
</script>

<template>
  <div class="crawler-view">
    <el-card class="page-header">
      <template #header>
        <div class="card-header">
          <span class="title">
            <el-icon><VideoPlay /></el-icon>
            爬取你想要的评论吧
          </span>
          <span class="subtitle">支持多平台评论数据爬取</span>
        </div>
      </template>
    </el-card>

    <el-row :gutter="20" class="main-content">
      <el-col :span="12">
        <el-card class="crawler-form">
          <el-tabs v-model="activeTab" type="border-card">
            <el-tab-pane name="bilibili-video">
              <template #label>
                <span class="tab-label">
                  <el-icon><VideoPlay /></el-icon>
                  B站视频
                </span>
              </template>
              <el-form :model="bilibiliVideoForm" label-position="top">
                <el-form-item label="BV号">
                  <el-input
                    v-model="bilibiliVideoForm.bv"
                    placeholder="例如: BV1GYAwzJEza"
                    clearable
                  />
                </el-form-item>
                <el-form-item>
                  <el-checkbox v-model="bilibiliVideoForm.isSecond"> 爬取二级评论 </el-checkbox>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="crawlerStore.loading"
                    @click="handleCrawlVideo"
                  >
                    开始爬取
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane name="bilibili-dynamic">
              <template #label>
                <span class="tab-label">
                  <el-icon><Document /></el-icon>
                  B站动态
                </span>
              </template>
              <el-form :model="bilibiliDynamicForm" label-position="top">
                <el-form-item label="动态ID (opus)">
                  <el-input
                    v-model="bilibiliDynamicForm.opus"
                    placeholder="例如: 123456789"
                    clearable
                  />
                </el-form-item>
                <el-form-item>
                  <el-checkbox v-model="bilibiliDynamicForm.isSecond"> 爬取二级评论 </el-checkbox>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="crawlerStore.loading"
                    @click="handleCrawlDynamic"
                  >
                    开始爬取
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane name="zhihu">
              <template #label>
                <span class="tab-label">
                  <el-icon><ChatDotRound /></el-icon>
                  知乎
                </span>
              </template>
              <el-form :model="zhihuForm" label-position="top">
                <el-form-item label="回答ID">
                  <el-input
                    v-model="zhihuForm.answerId"
                    placeholder="例如: 2018449337789719535"
                    clearable
                  />
                </el-form-item>
                <el-form-item label="最大爬取数量">
                  <el-slider v-model="zhihuForm.maxCount" :max="1000" :min="100" show-input />
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="crawlerStore.loading"
                    @click="handleCrawlZhihu"
                  >
                    开始爬取
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane name="netease">
              <template #label>
                <span class="tab-label">
                  <el-icon><Headset /></el-icon>
                  网易云
                </span>
              </template>
              <el-form :model="neteaseForm" label-position="top">
                <el-form-item label="歌曲ID">
                  <el-input
                    v-model="neteaseForm.songId"
                    type="number"
                    placeholder="例如: 2122308127"
                    clearable
                  />
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="crawlerStore.loading"
                    @click="handleCrawlNetease"
                  >
                    开始爬取
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane name="douban">
              <template #label>
                <span class="tab-label">
                  <el-icon><Collection /></el-icon>
                  豆瓣
                </span>
              </template>
              <el-form :model="doubanForm" label-position="top">
                <el-form-item label="爬取书籍数量">
                  <el-slider v-model="doubanForm.maxBooks" :max="20" :min="1" show-input />
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="crawlerStore.loading"
                    @click="handleCrawlDouban"
                  >
                    开始爬取
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="crawler-logs">
          <template #header>
            <div class="card-header">
              <span>爬取日志</span>
              <el-button type="danger" size="small" @click="crawlerStore.clearLogs">
                清空日志
              </el-button>
            </div>
          </template>
          <div class="logs-container">
            <div v-for="(log, index) in crawlerStore.crawlLogs" :key="index" class="log-item">
              {{ log }}
            </div>
            <div v-if="crawlerStore.crawlLogs.length === 0" class="empty-logs">暂无日志</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 爬取进度对话框 -->
    <el-dialog
      v-model="crawlDialogVisible"
      title="爬取中"
      width="400px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <div class="crawl-progress">
        <div class="progress-info">
          <p class="task-name">{{ crawlTaskName }}</p>
          <p class="status">
            <el-icon class="loading-icon"><Loading /></el-icon>
            {{ crawlStatus }}
          </p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.crawler-view {
  padding: 0;
}

.page-header {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}

.subtitle {
  font-size: 14px;
  color: #909399;
}

.main-content {
  margin-top: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 5px;
}

.crawler-form {
  height: 100%;
}

.crawler-logs {
  height: 100%;
}

.crawler-logs :deep(.el-card__body) {
  padding: 0;
  height: calc(100% - 55px);
}

.logs-container {
  height: 100%;
  overflow-y: auto;
  padding: 15px;
  background-color: #1e1e1e;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.6;
}

.log-item {
  color: #d4d4d4;
  padding: 2px 0;
  border-bottom: 1px solid #333;
}

.log-item:last-child {
  border-bottom: none;
}

.empty-logs {
  color: #666;
  text-align: center;
  padding: 20px;
}

.crawl-progress {
  padding: 40px 0;
  text-align: center;
}

.progress-info .task-name {
  font-weight: bold;
  margin-bottom: 20px;
  word-break: break-all;
  font-size: 16px;
}

.progress-info .status {
  color: #909399;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.loading-icon {
  animation: rotate 1s linear infinite;
  font-size: 24px;
  color: #409eff;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
