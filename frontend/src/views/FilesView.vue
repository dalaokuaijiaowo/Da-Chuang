<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useCrawlerStore } from '@/stores/crawler'
import { useAnalyzerStore } from '@/stores/analyzer'
import { ElMessage } from 'element-plus'
import { Folder, Download, View, Refresh, Cpu } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const crawlerStore = useCrawlerStore()
const analyzerStore = useAnalyzerStore()
const dialogVisible = ref(false)
const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

onMounted(() => {
  loadFileList()
})

const loadFileList = async () => {
  try {
    await crawlerStore.fetchFileList()
  } catch {
    ElMessage.error('获取文件列表失败')
  }
}

const handleView = async (filename: string) => {
  try {
    await crawlerStore.fetchFileContent(filename)
    dialogVisible.value = true
    if (crawlerStore.fileContent && crawlerStore.fileContent.length > 0) {
      nextTick(() => {
        initChart()
      })
    } else {
      ElMessage.warning('文件内容为空')
    }
  } catch (error) {
    console.error('获取文件内容失败:', error)
    ElMessage.error('获取文件内容失败')
  }
}

const handleDownload = async (filename: string) => {
  try {
    await crawlerStore.downloadFile(filename)
    ElMessage.success('下载成功')
  } catch {
    ElMessage.error('下载失败')
  }
}

// 检测进度对话框
const analyzeDialogVisible = ref(false)
const analyzingFilename = ref('')

const handleAnalyze = async (filename: string) => {
  try {
    analyzingFilename.value = filename
    analyzeDialogVisible.value = true

    // 启动异步检测任务
    const taskId = await analyzerStore.startAnalyzeFile(filename)

    // 开始轮询进度
    analyzerStore.startProgressQuery(taskId, 500)

    // 等待检测完成
    const checkComplete = setInterval(() => {
      if (analyzerStore.currentTask?.status === 'completed') {
        clearInterval(checkComplete)
        analyzeDialogVisible.value = false
        ElMessage.success('检测完成')
        // 清空当前任务
        analyzerStore.clearCurrentTask()
      } else if (analyzerStore.currentTask?.status === 'failed') {
        clearInterval(checkComplete)
        analyzeDialogVisible.value = false
        ElMessage.error('检测失败: ' + analyzerStore.currentTask?.error)
        analyzerStore.clearCurrentTask()
      }
    }, 500)

  } catch (error) {
    console.error('检测失败:', error)
    ElMessage.error('检测失败')
    analyzeDialogVisible.value = false
    analyzerStore.clearCurrentTask()
  }
}

const getFileIcon = (filename: string) => {
  if (filename.includes('BV')) return 'VideoPlay'
  if (filename.includes('zhihu')) return 'ChatDotRound'
  if (filename.includes('netease')) return 'Headset'
  if (filename.includes('douban')) return 'Collection'
  return 'Document'
}

const getFileType = (filename: string) => {
  if (filename.includes('BV')) return 'B站视频'
  if (filename.includes('dynamic')) return 'B站动态'
  if (filename.includes('zhihu')) return '知乎'
  if (filename.includes('netease')) return '网易云'
  if (filename.includes('douban')) return '豆瓣'
  return '其他'
}

const initChart = () => {
    if (!chartRef.value) return

    if (chart) {
      chart.dispose()
    }

    try {
      chart = echarts.init(chartRef.value)

      const contentLength = crawlerStore.fileContent ? crawlerStore.fileContent.length : 0

      const option: echarts.EChartsOption = {
        title: {
          text: '数据概览',
          left: 'center',
        },
        tooltip: {
          trigger: 'item',
        },
        xAxis: {
          type: 'category',
          data: ['评论数量'],
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: [contentLength],
            type: 'bar',
            itemStyle: {
              color: '#409eff',
            },
            label: {
              show: true,
              position: 'top',
            },
          },
        ],
      }

      chart.setOption(option)

      window.addEventListener('resize', () => {
        chart?.resize()
      })
    } catch (error) {
      console.error('初始化图表失败:', error)
    }
  }
</script>

<template>
  <div class="files-view">
    <el-card class="page-header">
      <template #header>
        <div class="card-header">
          <span class="title">
            <el-icon><Folder /></el-icon>
            文件管理
          </span>
          <el-button type="primary" @click="loadFileList">
            <el-icon><Refresh /></el-icon>
            刷新列表
          </el-button>
        </div>
      </template>
    </el-card>

    <el-card class="file-list">
      <el-table
        :data="crawlerStore.fileList"
        style="width: 100%"
        border
        stripe
        v-loading="crawlerStore.loading"
      >
        <el-table-column type="index" width="50" label="序号" />
        <el-table-column label="文件名" min-width="300">
          <template #default="{ row }">
            <el-icon class="file-icon">
              <component :is="getFileIcon(row)" />
            </el-icon>
            {{ row }}
          </template>
        </el-table-column>
        <el-table-column label="类型" width="120" align="center">
          <template #default="{ row }">
            <el-tag size="small">{{ getFileType(row) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button type="success" size="small" @click="handleDownload(row)">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
            <el-button type="warning" size="small" @click="handleAnalyze(row)" v-if="row.endsWith('.csv')">
              <el-icon><Cpu /></el-icon>
              检测
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="crawlerStore.fileList.length === 0" description="暂无文件" />
    </el-card>

    <el-dialog v-model="dialogVisible" title="文件内容" width="80%" destroy-on-close>
      <div class="dialog-content">
        <div ref="chartRef" class="content-chart"></div>
        <el-table v-if="crawlerStore.fileContent && crawlerStore.fileContent.length > 0 && crawlerStore.fileContent[0]" :data="crawlerStore.fileContent" height="400" border stripe>
          <el-table-column type="index" width="50" label="序号" />
          <template v-for="key in Object.keys(crawlerStore.fileContent[0] as Record<string, any>)" :key="key">
            <el-table-column
              v-if="key !== '序号'"
              :prop="key"
              :label="key"
              min-width="150"
              show-overflow-tooltip
            />
          </template>
        </el-table>
        <div v-else-if="crawlerStore.fileContent && crawlerStore.fileContent.length > 0" class="empty-content">
          <el-empty description="文件内容格式异常" />
        </div>
        <div v-else class="empty-content">
          <el-empty description="文件内容为空" />
        </div>
      </div>
    </el-dialog>

    <!-- 检测进度对话框 -->
    <el-dialog
      v-model="analyzeDialogVisible"
      title="AI检测中"
      width="400px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <div class="analyze-progress">
        <div class="progress-info">
          <p class="filename">{{ analyzingFilename }}</p>
          <p class="status">
            <span v-if="analyzerStore.currentTask?.status === 'running'">
              正在检测... {{ analyzerStore.currentTask?.current || 0 }} / {{ analyzerStore.currentTask?.total || 0 }}
            </span>
            <span v-else-if="analyzerStore.currentTask?.status === 'completed'">检测完成</span>
            <span v-else-if="analyzerStore.currentTask?.status === 'failed'">检测失败</span>
            <span v-else>准备中...</span>
          </p>
        </div>
        <el-progress
          :percentage="analyzerStore.currentTask?.progress || 0"
          :status="analyzerStore.currentTask?.status === 'failed' ? 'exception' : ''"
          :stroke-width="15"
          striped
          striped-flow
          :duration="10"
        />
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.files-view {
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

.file-icon {
  margin-right: 8px;
  color: #409eff;
}

.dialog-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.content-chart {
  width: 100%;
  height: 200px;
}

.analyze-progress {
  padding: 20px 0;
}

.progress-info {
  margin-bottom: 20px;
  text-align: center;
}

.progress-info .filename {
  font-weight: bold;
  margin-bottom: 10px;
  word-break: break-all;
}

.progress-info .status {
  color: #909399;
  font-size: 14px;
}
</style>
