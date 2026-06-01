<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { AnalyzeStats } from '@/api/analyze'

interface Props {
  stats: AnalyzeStats
}

const props = defineProps<Props>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)
  updateChart()

  window.addEventListener('resize', () => {
    chart?.resize()
  })
}

const updateChart = () => {
  if (!chart) return

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['AI生成', '人类撰写'],
    },
    series: [
      {
        name: '检测结果',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: '{b}: {c} ({d}%)',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
          },
        },
        data: [
          {
            value: props.stats.ai_count,
            name: 'AI生成',
            itemStyle: { color: '#f56c6c' },
          },
          {
            value: props.stats.human_count,
            name: '人类撰写',
            itemStyle: { color: '#67c23a' },
          },
        ],
      },
    ],
  }

  chart.setOption(option)
}

watch(() => props.stats, () => {
  updateChart()
}, { deep: true })

onMounted(() => {
  initChart()
})
</script>

<template>
  <div ref="chartRef" class="stats-chart"></div>
</template>

<style scoped>
.stats-chart {
  width: 100%;
  height: 300px;
}
</style>
