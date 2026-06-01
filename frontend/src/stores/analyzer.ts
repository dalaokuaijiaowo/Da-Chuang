import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as analyzeApi from '@/api/analyze'
import type { AnalyzeResult, AnalyzeStats, AnalyzeResponse } from '@/api/analyze'

interface ApiError {
  response?: {
    data?: {
      message?: string
    }
  }
  message?: string
}

export const useAnalyzerStore = defineStore('analyzer', () => {
  const loading = ref(false)
  const analyzeResults = ref<AnalyzeResult[]>([])
  const analyzeStats = ref<AnalyzeStats | null>(null)
  const currentText = ref('')
  const analyzeHistory = ref<AnalyzeResponse[]>([])

  const hasResults = computed(() => analyzeResults.value.length > 0)
  const aiRatio = computed(() => analyzeStats.value?.ai_ratio || 0)
  const totalCount = computed(() => analyzeStats.value?.total || 0)
  const aiCount = computed(() => analyzeStats.value?.ai_count || 0)
  const humanCount = computed(() => analyzeStats.value?.human_count || 0)

  const analyzeFile = async (file: File) => {
    loading.value = true
    try {
      const response = await analyzeApi.analyzeComments(file)
      analyzeResults.value = response.data.results
      analyzeStats.value = response.data.stats
      analyzeHistory.value.unshift(response.data)
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '分析失败'
      throw new Error(errorMsg)
    } finally {
      loading.value = false
    }
  }

  const analyzeSingleText = async (text: string) => {
    loading.value = true
    currentText.value = text
    try {
      const response = await analyzeApi.analyzeText(text)
      analyzeResults.value = response.data.results
      analyzeStats.value = response.data.stats
      analyzeHistory.value.unshift(response.data)
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '分析失败'
      throw new Error(errorMsg)
    } finally {
      loading.value = false
    }
  }

  const clearResults = () => {
    analyzeResults.value = []
    analyzeStats.value = null
    currentText.value = ''
  }

  const clearHistory = () => {
    analyzeHistory.value = []
  }

  const checkServerHealth = async () => {
    try {
      const response = await analyzeApi.checkHealth()
      return response.data.status === 'ok'
    } catch {
      return false
    }
  }

  const analyzeFileByName = async (filename: string) => {
    loading.value = true
    try {
      const response = await analyzeApi.analyzeFileByName(filename)
      analyzeResults.value = response.data.results
      analyzeStats.value = response.data.stats
      analyzeHistory.value.unshift(response.data)
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '分析失败'
      throw new Error(errorMsg)
    } finally {
      loading.value = false
    }
  }

  // 异步检测相关
  const currentTask = ref<{
    id: string
    filename: string
    status: 'running' | 'completed' | 'failed'
    progress: number
    total: number
    current: number
    error?: string
  } | null>(null)
  let progressInterval: number | null = null

  const startAnalyzeFile = async (filename: string) => {
    try {
      const response = await analyzeApi.startAnalyzeFile(filename)
      const taskId = response.data.task_id

      // 初始化当前任务
      currentTask.value = {
        id: taskId,
        filename: filename,
        status: 'running',
        progress: 0,
        total: 0,
        current: 0
      }

      return taskId
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '启动检测失败'
      throw new Error(errorMsg)
    }
  }

  const queryTaskProgress = async (taskId: string) => {
    try {
      const response = await analyzeApi.getTaskStatus(taskId)
      const task = response.data.task

      // 更新当前任务状态
      currentTask.value = {
        id: task.id,
        filename: task.filename,
        status: task.status,
        progress: task.progress,
        total: task.total,
        current: task.current
      }

      // 如果任务完成，保存结果
      if (task.status === 'completed' && task.result) {
        analyzeResults.value = task.result.results
        analyzeStats.value = task.result.stats
        analyzeHistory.value.unshift(task.result)
        stopProgressQuery()
        return true
      }

      // 如果任务失败
      if (task.status === 'failed') {
        stopProgressQuery()
        throw new Error(task.error || '检测失败')
      }

      return false
    } catch (error) {
      stopProgressQuery()
      throw error
    }
  }

  const startProgressQuery = (taskId: string, interval: number = 1000) => {
    // 清除之前的定时器
    stopProgressQuery()

    // 立即查询一次
    queryTaskProgress(taskId)

    // 设置定时器定期查询
    progressInterval = window.setInterval(() => {
      queryTaskProgress(taskId).catch(() => {
        // 错误处理在queryTaskProgress中完成
      })
    }, interval)
  }

  const stopProgressQuery = () => {
    if (progressInterval) {
      clearInterval(progressInterval)
      progressInterval = null
    }
  }

  const clearCurrentTask = () => {
    currentTask.value = null
    stopProgressQuery()
  }

  // 检测报告相关
  const detectedFiles = ref<string[]>([])
  const selectedDetectedFile = ref<string | null>(null)

  const loadDetectedFiles = async () => {
    try {
      const response = await analyzeApi.getDetectedFiles()
      detectedFiles.value = response.data.files
      return response.data.files
    } catch (error) {
      console.error('获取检测报告文件列表失败:', error)
      detectedFiles.value = []
      return []
    }
  }

  const loadDetectedFileContent = async (filename: string) => {
    loading.value = true
    try {
      const response = await analyzeApi.getDetectedFileContent(filename)
      analyzeResults.value = response.data.results
      analyzeStats.value = response.data.stats
      selectedDetectedFile.value = filename
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '获取检测报告失败'
      throw new Error(errorMsg)
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    analyzeResults,
    analyzeStats,
    currentText,
    analyzeHistory,
    hasResults,
    aiRatio,
    totalCount,
    aiCount,
    humanCount,
    analyzeFile,
    analyzeSingleText,
    analyzeFileByName,
    // 异步检测相关
    currentTask,
    startAnalyzeFile,
    queryTaskProgress,
    startProgressQuery,
    stopProgressQuery,
    clearCurrentTask,
    clearResults,
    clearHistory,
    checkServerHealth,
    // 检测报告相关
    detectedFiles,
    selectedDetectedFile,
    loadDetectedFiles,
    loadDetectedFileContent,
  }
})
