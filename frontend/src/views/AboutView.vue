<script setup lang="ts">
import { onMounted } from 'vue'
import { useCrawlerStore } from '@/stores/crawler'
import {
  VideoPlay,
  Document,
  ChatDotRound,
  Headset,
  Collection,
  Cpu,
} from '@element-plus/icons-vue'

const crawlerStore = useCrawlerStore()

onMounted(async () => {
  await crawlerStore.fetchFileList()
})

const platforms = [
  {
    name: 'B站视频',
    icon: VideoPlay,
    color: '#00a1d6',
  },
  {
    name: 'B站动态',
    icon: Document,
    color: '#00a1d6',
  },
  {
    name: '知乎',
    icon: ChatDotRound,
    color: '#0084ff',
  },
  {
    name: '网易云',
    icon: Headset,
    color: '#c20c0c',
  },
  {
    name: '豆瓣',
    icon: Collection,
    color: '#007722',
  },
]

const features = [
  {
    title: '多平台支持',
    description: '支持B站、知乎、网易云、豆瓣等多个平台的评论爬取',
    icon: VideoPlay,
  },
  {
    title: 'AI智能检测',
    description: '采用先进的AI检测算法，准确识别AI生成内容',
    icon: Cpu,
  },
  {
    title: '批量处理',
    description: '支持批量上传CSV文件进行大规模检测分析',
    icon: Document,
  },
  {
    title: '可视化展示',
    description: '直观的数据可视化图表，清晰展示检测结果',
    icon: Collection,
  },
]

const guideSteps = [
  {
    title: '第一步：爬取评论数据',
    description: '在"爬虫"页面选择相应平台，输入必要参数，点击"开始爬取"按钮。爬取完成后，数据会自动保存到系统中。',
    icon: VideoPlay,
  },
  {
    title: '第二步：查看爬取结果',
    description: '在"文件管理"页面查看已爬取的文件列表，可以点击"查看"按钮查看文件内容，或点击"下载"按钮下载文件。',
    icon: Document,
  },
  {
    title: '第三步：AI检测分析',
    description: '在"文件管理"页面，对需要检测的CSV文件点击"检测"按钮，系统会自动进行AI检测并生成检测报告。',
    icon: Cpu,
  },
  {
    title: '第四步：查看检测报告',
    description: '在"检测报告"页面查看所有检测报告，包括历史检测结果和已保存的检测报告文件。',
    icon: Collection,
  },
]
</script>

<template>
  <div class="about-view">
    <div class="guide-section">
      <h2 class="section-title">使用指南</h2>
      <div class="guide-steps">
        <div
          v-for="(step, index) in guideSteps"
          :key="index"
          class="guide-step"
        >
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-content">
            <el-icon class="step-icon" :size="32">
              <component :is="step.icon" />
            </el-icon>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-description">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="platforms-section">
      <h2 class="section-title">支持平台</h2>
      <el-row :gutter="20">
        <el-col
          v-for="platform in platforms"
          :key="platform.name"
          :span="4"
          :xs="12"
          :sm="8"
          :md="6"
          :lg="4"
        >
          <div
            class="platform-card"
            :style="{ '--platform-color': platform.color }"
          >
            <el-icon class="platform-icon" :size="40">
              <component :is="platform.icon" />
            </el-icon>
            <span class="platform-name">{{ platform.name }}</span>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="features-section">
      <h2 class="section-title">功能特性</h2>
      <el-row :gutter="20">
        <el-col
          v-for="feature in features"
          :key="feature.title"
          :span="6"
          :xs="24"
          :sm="12"
          :md="12"
          :lg="6"
        >
          <el-card class="feature-card" shadow="hover">
            <el-icon class="feature-icon" :size="48">
              <component :is="feature.icon" />
            </el-icon>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="stats-section">
      <h2 class="section-title">数据统计</h2>
      <el-row :gutter="20">
        <el-col :span="12" :xs="24" :sm="12" :md="12">
          <el-card class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">支持平台</div>
          </el-card>
        </el-col>
        <el-col :span="12" :xs="24" :sm="12" :md="12">
          <el-card class="stat-card">
            <div class="stat-number">{{ crawlerStore.fileList.length }}</div>
            <div class="stat-label">已爬取文件</div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.about-view {
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
}

.subtitle {
  font-size: 14px;
  color: #909399;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 24px;
  color: #303133;
  text-align: center;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.platforms-section {
  margin-bottom: 30px;
  padding: 20px;
}

.platform-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.platform-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  border-color: var(--platform-color);
}

.platform-icon {
  color: var(--platform-color);
  margin-bottom: 12px;
}

.platform-name {
  display: block;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.features-section {
  margin-bottom: 30px;
  padding: 20px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  text-align: center;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  color: #667eea;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
  color: #303133;
}

.feature-description {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

.stats-section {
  margin-bottom: 30px;
  padding: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  text-align: center;
  padding: 30px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.guide-section {
  margin-bottom: 30px;
  padding: 20px;
}

.guide-steps {
  max-width: 800px;
  margin: 0 auto;
}

.guide-step {
  display: flex;
  margin-bottom: 30px;
  align-items: flex-start;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #667eea;
  color: white;
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.step-content:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.step-icon {
  color: #667eea;
  margin-bottom: 12px;
}

.step-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
  color: #303133;
}

.step-description {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .guide-step {
    flex-direction: column;
  }

  .step-number {
    margin-right: 0;
    margin-bottom: 15px;
  }
}
</style>
