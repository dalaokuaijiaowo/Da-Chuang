<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAnalyzerStore } from '@/stores/analyzer'
import { ElMessage } from 'element-plus'
import { Cpu, Document, Delete, Refresh, Folder } from '@element-plus/icons-vue'
import StatsChart from '@/components/StatsChart.vue'
import ResultTable from '@/components/ResultTable.vue'

const analyzerStore = useAnalyzerStore()
const selectedReport = ref<number | null>(null)

const hasResults = computed(() => analyzerStore.hasResults)
const hasHistory = computed(() => analyzerStore.analyzeHistory.length > 0)
const hasDetectedFiles = computed(() => analyzerStore.detectedFiles.length > 0)

const handleSelectReport = (index: number) => {
  selectedReport.value = index
  const report = analyzerStore.analyzeHistory[index]
  if (report) {
    analyzerStore.analyzeResults = report.results
    analyzerStore.analyzeStats = report.stats
  }
}

const handleSelectDetectedFile = async (filename: string) => {
  try {
    await analyzerStore.loadDetectedFileContent(filename)
    selectedReport.value = null // 清除历史报告选择
  } catch (error) {
    console.error('加载检测报告失败:', error)
    ElMessage.error('加载检测报告失败')
  }
}

const handleClear = () => {
  analyzerStore.clearResults()
  selectedReport.value = null
  ElMessage.success('已清空')
}

const handleClearHistory = () => {
  analyzerStore.clearHistory()
  analyzerStore.clearResults()
  selectedReport.value = null
  ElMessage.success('已清空历史记录')
}

const handleRefreshDetectedFiles = async () => {
  try {
    await analyzerStore.loadDetectedFiles()
    ElMessage.success('检测报告列表已刷新')
  } catch (error) {
    console.error('刷新检测报告列表失败:', error)
    ElMessage.error('刷新失败')
  }
}

onMounted(async () => {
  // 加载历史检测报告
  if (analyzerStore.analyzeHistory.length > 0 && !selectedReport.value) {
    handleSelectReport(0)
  }

  // 加载detected目录中的检测报告文件
  await analyzerStore.loadDetectedFiles()
})
</script>

<template>
  <div class="analyzer-view">
    <el-card class="page-header">
      <template #header>
        <div class="card-header">
          <span class="title">
            <el-icon><Cpu /></el-icon>
            检测报告
          </span>
          <span class="subtitle">查看文件检测报告</span>
        </div>
      </template>
    </el-card>

    <el-row :gutter="20" class="main-content">
      <el-col :span="hasResults ? 8 : 24">
        <el-card class="report-list">
          <template #header>
            <div class="card-header">
              <span>检测报告列表</span>
              <el-button type="danger" size="small" @click="handleClearHistory">
                <el-icon><Delete /></el-icon>
                清空历史
              </el-button>
            </div>
          </template>

          <el-empty v-if="!hasHistory && !hasDetectedFiles" description="暂无检测报告" />

          <!-- 历史检测报告 -->
          <div v-if="hasHistory" class="report-section">
            <div class="section-title">历史检测</div>
            <el-list class="report-items">
              <el-list-item
                v-for="(report, index) in analyzerStore.analyzeHistory"
                :key="index"
                :class="{ 'active': selectedReport === index && !analyzerStore.selectedDetectedFile }"
                @click="handleSelectReport(index)"
              >
                <template #prefix>
                  <el-icon><Document /></el-icon>
                </template>
                <div class="report-item-content">
                  <div class="report-item-title">检测报告 {{ index + 1 }}</div>
                  <div class="report-item-meta">
                    <span>AI率: {{ report.stats.ai_ratio.toFixed(1) }}%</span>
                    <span>总样本: {{ report.stats.total }}</span>
                  </div>
                </div>
              </el-list-item>
            </el-list>
          </div>

          <!-- 已保存的检测报告 -->
          <div v-if="hasDetectedFiles" class="report-section">
            <div class="section-header">
              <div class="section-title">已保存的检测报告</div>
              <el-button size="small" @click="handleRefreshDetectedFiles">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
            <el-list class="report-items">
              <el-list-item
                v-for="(filename, index) in analyzerStore.detectedFiles"
                :key="index"
                :class="{ 'active': analyzerStore.selectedDetectedFile === filename }"
                @click="handleSelectDetectedFile(filename)"
              >
                <template #prefix>
                  <el-icon><Folder /></el-icon>
                </template>
                <div class="report-item-content">
                  <div class="report-item-title">{{ filename }}</div>
                  <div class="report-item-meta">
                    <span>已保存的检测报告</span>
                  </div>
                </div>
              </el-list-item>
            </el-list>
          </div>
        </el-card>
      </el-col>

      <el-col v-if="hasResults" :span="16">
        <el-card class="analyzer-results">
          <template #header>
            <div class="card-header">
              <span>检测结果</span>
              <el-tag :type="analyzerStore.aiRatio > 50 ? 'danger' : 'success'" size="large">
                AI率: {{ analyzerStore.aiRatio.toFixed(1) }}%
              </el-tag>
            </div>
          </template>

          <div class="stats-overview">
            <el-row :gutter="10">
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ analyzerStore.totalCount }}</div>
                  <div class="stat-label">总样本</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item ai">
                  <div class="stat-value">{{ analyzerStore.aiCount }}</div>
                  <div class="stat-label">AI生成</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item human">
                  <div class="stat-value">{{ analyzerStore.humanCount }}</div>
                  <div class="stat-label">人类撰写</div>
                </div>
              </el-col>
            </el-row>
          </div>

          <StatsChart v-if="analyzerStore.analyzeStats" :stats="analyzerStore.analyzeStats" />
        </el-card>
      </el-col>
    </el-row>

    <el-row v-if="hasResults" class="table-section">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>详细检测结果</span>
              <el-button @click="handleClear">
                <el-icon><Delete /></el-icon>
                清空
              </el-button>
            </div>
          </template>
          <ResultTable :results="analyzerStore.analyzeResults" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.analyzer-view {
  padding: 0;
}

.page-header {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.report-list {
  height: 100%;
}

.report-items {
  max-height: 500px;
  overflow-y: auto;
}

.report-item-content {
  width: 100%;
}

.report-item-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
}

.report-item-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #909399;
}

.el-list-item.active {
  background-color: #ecf5ff;
}

.analyzer-results {
  height: 100%;
}

.stats-overview {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.stat-item.ai {
  background-color: #fef0f0;
}

.stat-item.human {
  background-color: #f0f9eb;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-item.ai .stat-value {
  color: #f56c6c;
}

.stat-item.human .stat-value {
  color: #67c23a;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.table-section {
  margin-top: 20px;
}

.report-section {
  margin-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 15px;
}

.report-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.section-title {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.el-list-item.active {
  background-color: #ecf5ff;
}

.el-list-item:hover {
  background-color: #f5f7fa;
}
</style>
