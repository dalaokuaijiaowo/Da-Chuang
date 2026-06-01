import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as crawlerApi from '@/api/crawler'
import type { CrawlResponse, FileContentItem } from '@/api/crawler'

interface ApiError {
  response?: {
    data?: {
      message?: string
    }
  }
  message?: string
}

export const useCrawlerStore = defineStore('crawler', () => {
  const loading = ref(false)
  const crawlResult = ref<CrawlResponse | null>(null)
  const fileList = ref<string[]>([])
  const currentFile = ref<string>('')
  const fileContent = ref<FileContentItem[]>([])
  const crawlLogs = ref<string[]>([])

  const hasResult = computed(() => crawlResult.value !== null)
  const hasFileContent = computed(() => fileContent.value.length > 0)

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString()
    crawlLogs.value.push(`[${timestamp}] ${message}`)
  }

  const clearLogs = () => {
    crawlLogs.value = []
  }

  const crawlVideo = async (bv: string, isSecond: boolean = true) => {
    loading.value = true
    clearLogs()
    addLog(`开始爬取B站视频评论: ${bv}`)
    try {
      const response = await crawlerApi.crawlVideo({ bv, is_second: isSecond })
      crawlResult.value = response.data
      addLog(response.data.message)
      if (response.data.output) {
        response.data.output.split('\n').forEach(line => {
          if (line.trim()) addLog(line)
        })
      }
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '爬取失败'
      addLog(`错误: ${errorMsg}`)
      throw error
    } finally {
      loading.value = false
    }
  }

  const crawlDynamic = async (opus: string, isSecond: boolean = true) => {
    loading.value = true
    clearLogs()
    addLog(`开始爬取B站动态评论: ${opus}`)
    try {
      const response = await crawlerApi.crawlDynamic({ opus, is_second: isSecond })
      crawlResult.value = response.data
      addLog(response.data.message)
      if (response.data.output) {
        response.data.output.split('\n').forEach(line => {
          if (line.trim()) addLog(line)
        })
      }
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '爬取失败'
      addLog(`错误: ${errorMsg}`)
      throw error
    } finally {
      loading.value = false
    }
  }

  const crawlZhihu = async (answerId: string, maxCount: number = 500) => {
    loading.value = true
    clearLogs()
    addLog(`开始爬取知乎回答评论: ${answerId}`)
    try {
      const response = await crawlerApi.crawlZhihu({ answer_id: answerId, max_count: maxCount })
      crawlResult.value = response.data
      addLog(response.data.message)
      if (response.data.output) {
        response.data.output.split('\n').forEach(line => {
          if (line.trim()) addLog(line)
        })
      }
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '爬取失败'
      addLog(`错误: ${errorMsg}`)
      throw error
    } finally {
      loading.value = false
    }
  }

  const crawlNetease = async (songId: number) => {
    loading.value = true
    clearLogs()
    addLog(`开始爬取网易云音乐评论: ${songId}`)
    try {
      const response = await crawlerApi.crawlNetease({ song_id: songId })
      crawlResult.value = response.data
      addLog(response.data.message)
      if (response.data.output) {
        response.data.output.split('\n').forEach(line => {
          if (line.trim()) addLog(line)
        })
      }
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '爬取失败'
      addLog(`错误: ${errorMsg}`)
      throw error
    } finally {
      loading.value = false
    }
  }

  const crawlDouban = async (maxBooks: number = 5) => {
    loading.value = true
    clearLogs()
    addLog(`开始爬取豆瓣月度热书`)
    try {
      const response = await crawlerApi.crawlDouban({ max_books: maxBooks })
      crawlResult.value = response.data
      addLog(response.data.message)
      if (response.data.output) {
        response.data.output.split('\n').forEach(line => {
          if (line.trim()) addLog(line)
        })
      }
      return response.data
    } catch (error: unknown) {
      const apiError = error as ApiError
      const errorMsg = apiError.response?.data?.message || apiError.message || '爬取失败'
      addLog(`错误: ${errorMsg}`)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchFileList = async () => {
    const response = await crawlerApi.getFileList()
    fileList.value = response.data.files
    return response.data.files
  }

  const fetchFileContent = async (filename: string) => {
    loading.value = true
    // 先清空文件内容，避免显示之前的内容
    fileContent.value = []
    try {
      const response = await crawlerApi.getFileContent(filename)
      currentFile.value = filename
      // 检查响应数据
      if (response.data) {
        // 如果response.data本身是数组
        if (Array.isArray(response.data)) {
          fileContent.value = response.data
          return response.data
        }
        // 如果response.data有data属性且是数组
        else if (Array.isArray(response.data.data)) {
          fileContent.value = response.data.data
          return response.data.data
        }
      }
      // 如果响应格式异常，设置为空数组
      fileContent.value = []
      return []
    } catch (error: unknown) {
      console.error('获取文件内容失败:', error)
      // 确保即使出错，fileContent也是一个空数组
      fileContent.value = []
      throw error
    } finally {
      loading.value = false
    }
  }

  const downloadFile = async (filename: string) => {
    const response = await crawlerApi.downloadFile(filename)
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  return {
    loading,
    crawlResult,
    fileList,
    currentFile,
    fileContent,
    crawlLogs,
    hasResult,
    hasFileContent,
    crawlVideo,
    crawlDynamic,
    crawlZhihu,
    crawlNetease,
    crawlDouban,
    fetchFileList,
    fetchFileContent,
    downloadFile,
    addLog,
    clearLogs,
  }
})
