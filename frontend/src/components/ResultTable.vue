<script setup lang="ts">
import { computed } from 'vue'
import type { AnalyzeResult } from '@/api/analyze'

interface Props {
  results: AnalyzeResult[]
}

const props = defineProps<Props>()

const getConclusionType = (conclusion: string) => {
  if (conclusion === 'AI生成') return 'danger'
  if (conclusion === '人类撰写') return 'success'
  return 'info'
}

const getProbabilityColor = (prob: number) => {
  if (prob >= 0.8) return '#f56c6c'
  if (prob >= 0.5) return '#e6a23c'
  return '#67c23a'
}

const tableData = computed(() => {
  return props.results.map(item => ({
    ...item,
    aiProbPercent: (item.ai_prob * 100).toFixed(1),
    humanProbPercent: (item.human_prob * 100).toFixed(1),
  }))
})
</script>

<template>
  <el-table
    :data="tableData"
    style="width: 100%"
    height="400"
    border
    stripe
  >
    <el-table-column type="index" width="50" label="序号" />
    <el-table-column prop="用户名" label="用户名" min-width="120" show-overflow-tooltip />
    <el-table-column prop="评论内容" label="评论内容" min-width="300" show-overflow-tooltip />
    <el-table-column label="AI概率" width="120" align="center">
      <template #default="{ row }">
        <el-progress
          :percentage="parseFloat(row.aiProbPercent)"
          :color="getProbabilityColor(row.ai_prob)"
          :stroke-width="8"
          :show-text="true"
        />
      </template>
    </el-table-column>
    <el-table-column label="人类概率" width="120" align="center">
      <template #default="{ row }">
        <el-progress
          :percentage="parseFloat(row.humanProbPercent)"
          color="#67c23a"
          :stroke-width="8"
          :show-text="true"
        />
      </template>
    </el-table-column>
    <el-table-column label="结论" width="100" align="center" fixed="right">
      <template #default="{ row }">
        <el-tag :type="getConclusionType(row.conclusion)" size="small">
          {{ row.conclusion }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<style scoped>
:deep(.el-progress__text) {
  font-size: 12px;
}
</style>
