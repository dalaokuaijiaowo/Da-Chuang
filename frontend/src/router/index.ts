import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: '首页' }
    },
    {
      path: '/crawler',
      redirect: '/crawler/bilibili',
      meta: { title: '评论爬虫' }
    },
    {
      path: '/crawler/bilibili',
      name: 'crawler-bilibili',
      component: () => import('../views/CrawlerView.vue'),
      meta: { title: 'B站爬虫' }
    },
    {
      path: '/crawler/zhihu',
      name: 'crawler-zhihu',
      component: () => import('../views/CrawlerView.vue'),
      meta: { title: '知乎爬虫' }
    },
    {
      path: '/crawler/netease',
      name: 'crawler-netease',
      component: () => import('../views/CrawlerView.vue'),
      meta: { title: '网易云爬虫' }
    },
    {
      path: '/crawler/douban',
      name: 'crawler-douban',
      component: () => import('../views/CrawlerView.vue'),
      meta: { title: '豆瓣爬虫' }
    },
    {
      path: '/analyzer',
      name: 'analyzer',
      component: () => import('../views/AnalyzerView.vue'),
      meta: { title: 'AI检测' }
    },
    {
      path: '/files',
      name: 'files',
      component: () => import('../views/FilesView.vue'),
      meta: { title: '文件管理' }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { title: '系统说明' }
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - AIGC检测系统`
  }
  return true
})

export default router
