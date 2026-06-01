import api from './index'

export interface CrawlVideoParams {
  bv: string
  is_second?: boolean
}

export interface CrawlDynamicParams {
  opus: string
  is_second?: boolean
}

export interface CrawlZhihuParams {
  answer_id: string
  max_count?: number
}

export interface CrawlNeteaseParams {
  song_id: number
}

export interface CrawlDoubanParams {
  max_books?: number
}

export interface CrawlResponse {
  success: boolean
  message: string
  output: string
}

export interface FileContentItem {
  [key: string]: string | number
}

export const crawlVideo = (params: CrawlVideoParams) => {
  return api.post<CrawlResponse>('/api/crawl/video', params)
}

export const crawlDynamic = (params: CrawlDynamicParams) => {
  return api.post<CrawlResponse>('/api/crawl/dynamic', params)
}

export const crawlZhihu = (params: CrawlZhihuParams) => {
  return api.post<CrawlResponse>('/api/crawl/zhihu', params)
}

export const crawlNetease = (params: CrawlNeteaseParams) => {
  return api.post<CrawlResponse>('/api/crawl/netease', params)
}

export const crawlDouban = (params?: CrawlDoubanParams) => {
  return api.post<CrawlResponse>('/api/crawl/douban', params)
}

export interface FileItem {
  name: string
  url: string
}

export const getFileList = () => {
  return api.get<{ files: string[] }>('/api/files')
}

export const getFileContent = (filename: string) => {
  return api.get<{ success: boolean; filename: string; data: FileContentItem[] }>(`/api/files/content/${filename}`)
}

export const downloadFile = (filename: string) => {
  return api.get(`/api/files/download/${filename}`, {
    responseType: 'blob',
  })
}
