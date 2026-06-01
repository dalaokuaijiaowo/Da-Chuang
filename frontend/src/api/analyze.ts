import api from './index'

export interface AnalyzeResult {
  序号: number
  用户名: string
  评论内容: string
  ai_prob: number
  human_prob: number
  conclusion: string
}

export interface AnalyzeStats {
  total: number
  ai_count: number
  human_count: number
  ai_ratio: number
}

export interface AnalyzeResponse {
  success: boolean
  results: AnalyzeResult[]
  stats: AnalyzeStats
}

export const analyzeComments = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post<AnalyzeResponse>('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const analyzeText = (text: string) => {
  const formData = new FormData()
  const blob = new Blob([`评论内容\n${text}`], { type: 'text/csv' })
  const file = new File([blob], 'input.csv', { type: 'text/csv' })
  formData.append('file', file)
  return api.post<AnalyzeResponse>('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const checkHealth = () => {
  return api.get<{ status: string; message: string }>('/api/health')
}

export const analyzeFileByName = (filename: string) => {
  return api.get<AnalyzeResponse>(`/api/analyze/file/${filename}`)
}

export const startAnalyzeFile = (filename: string) => {
  return api.post<{ success: boolean; task_id: string; message: string }>(`/api/analyze/file/${filename}`)
}

export const getTaskStatus = (taskId: string) => {
  return api.get<{ success: boolean; task: {
    id: string
    filename: string
    status: 'running' | 'completed' | 'failed'
    progress: number
    total: number
    current: number
    result?: AnalyzeResponse
    error?: string
  } }>(`/api/analyze/task/${taskId}`)
}

export const getDetectedFiles = () => {
  return api.get<{ files: string[] }>('/api/detected/files')
}

export const getDetectedFileContent = (filename: string) => {
  return api.get<AnalyzeResponse & { filename: string }>(`/api/detected/file/${filename}`)
}
