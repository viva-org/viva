<template>
  <div class="vocabulary-gap">
    <el-card shadow="hover" class="gap-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span>主动词汇 vs 被动词汇</span>
            <el-tooltip
              content="主动词汇：能够在写作和口语中自如使用的词汇；被动词汇：能够理解但不一定能够主动使用的词汇"
              placement="top"
            >
              <el-icon class="info-icon"><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
          <img src="@/assets/draw/undraw_file-search_cbur.svg" alt="File search illustration" class="header-illustration">
        </div>
      </template>
      
      <!-- Venn Diagram -->
      <div class="venn-container" ref="vennChart"></div>

      <!-- Gap Trend -->
      <div class="trend-container" ref="trendChart"></div>
    </el-card>

    <!-- Word List Modal -->
    <el-dialog
      v-model="showWordList"
      :title="modalTitle"
      width="60%"
      destroy-on-close
    >
      <div class="word-list-header">
        <span>共 {{ selectedWords.length }} 个单词</span>
        <el-input
          v-model="searchWord"
          placeholder="搜索单词..."
          prefix-icon="Search"
          style="width: 200px"
        />
      </div>
      
      <el-table
        :data="filteredWords"
        style="width: 100%"
        max-height="400"
        v-loading="loading"
      >
        <el-table-column prop="word" label="单词" width="180" />
        <el-table-column prop="translation" label="释义" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              link
              @click="addToActive(row)"
              v-if="currentSection === 'gap'"
            >
              添加到主动词汇
            </el-button>
            <el-button 
              type="primary" 
              link
              @click="viewWordDetails(row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showWordList = false">关闭</el-button>
          <el-button 
            type="primary" 
            @click="handleBatchAction"
            v-if="currentSection === 'gap'"
          >
            批量添加到主动词汇
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { PieChart, LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/services/api'

// 注册必要的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  PieChart,
  LineChart,
  CanvasRenderer
])

// Data
const vennChart = ref(null)
const trendChart = ref(null)
const showWordList = ref(false)
const modalTitle = ref('')
const currentSection = ref('')
const searchWord = ref('')
const loading = ref(false)

const vocabularyData = ref({
  active: {
    total: 2000,
    words: []
  },
  passive: {
    total: 3000,
    words: []
  },
  intersection: {
    total: 1500,
    words: []
  }
})

const selectedWords = ref([])

// Computed
const filteredWords = computed(() => {
  if (!searchWord.value) return selectedWords.value
  const search = searchWord.value.toLowerCase()
  return selectedWords.value.filter(word => 
    word.word.toLowerCase().includes(search) || 
    word.translation.toLowerCase().includes(search)
  )
})

// Methods
const initVennDiagram = () => {
  const chartDom = document.querySelector('.venn-container')
  vennChart.value = echarts.init(chartDom)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      top: 'bottom',
      left: 'center',
      padding: [15, 0]
    },
    series: [
      {
        type: 'pie',
        radius: ['45%', '65%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}\n{c}词',
          fontSize: 14
        },
        labelLine: {
          length: 15,
          length2: 10,
          smooth: true
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        data: [
          {
            name: '仅主动词汇',
            value: vocabularyData.value.active.total - vocabularyData.value.intersection.total,
            itemStyle: { color: '#1E88E5' }
          },
          {
            name: '完全掌握',
            value: vocabularyData.value.intersection.total,
            itemStyle: { color: '#42A5F5' }
          },
          {
            name: '需要提升(Gap)',
            value: vocabularyData.value.passive.total - vocabularyData.value.intersection.total,
            itemStyle: { color: '#90CAF9' }
          }
        ]
      }
    ]
  }

  vennChart.value.setOption(option)
  
  // Add click event
  vennChart.value.on('click', params => {
    const { name } = params
    if (name === '仅主动词汇') {
      showWordsBySection('active', '仅主动词汇')
    } else if (name === '需要提升(Gap)') {
      showWordsBySection('gap', '需要提升的词汇（Gap）')
    } else if (name === '完全掌握') {
      showWordsBySection('mastered', '完全掌握的词汇')
    }
  })
}

const initTrendChart = () => {
  const chartDom = document.querySelector('.trend-container')
  trendChart.value = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '词汇掌握趋势',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['主动词汇', '被动词汇', 'Gap'],
      bottom: 10,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      top: 60,
      left: '5%',
      right: '5%',
      bottom: 60,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '主动词汇',
        type: 'line',
        data: [1500, 1600, 1800, 1900, 2000, 2200],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#1E88E5' }
      },
      {
        name: '被动词汇',
        type: 'line',
        data: [2500, 2600, 2700, 2800, 3000, 3200],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#42A5F5' }
      },
      {
        name: 'Gap',
        type: 'line',
        data: [1000, 1000, 900, 900, 1000, 1000],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#90CAF9' }
      }
    ]
  }
  
  trendChart.value.setOption(option)
}

const showWordsBySection = async (section, title) => {
  currentSection.value = section
  modalTitle.value = title
  loading.value = true
  
  try {
    // 模拟API调用，实际使用时替换为真实API
    // const response = await api.getWordsBySection(section)
    // selectedWords.value = response.data
    
    // 模拟数据
    selectedWords.value = [
      { word: 'abandon', translation: '放弃，遗弃' },
      { word: 'abbreviate', translation: '缩写，缩短' },
      { word: 'ability', translation: '能力，才能' },
      // ... 更多单词
    ]
    
    showWordList.value = true
  } catch (error) {
    console.error('Error fetching words:', error)
  } finally {
    loading.value = false
  }
}

const addToActive = async (word) => {
  try {
    // await api.addToActiveVocabulary(word.id)
    ElMessage.success(`已将 ${word.word} 添加到主动词汇`)
  } catch (error) {
    console.error('Error adding word to active vocabulary:', error)
    ElMessage.error('添加失败')
  }
}

const viewWordDetails = (word) => {
  // 实现查看单词详情的逻辑
  console.log('View details for:', word)
}

const handleBatchAction = async () => {
  try {
    // await api.addMultipleToActiveVocabulary(selectedWords.value.map(w => w.id))
    ElMessage.success('已批量添加到主动词汇')
    showWordList.value = false
  } catch (error) {
    console.error('Error batch adding words:', error)
    ElMessage.error('批量添加失败')
  }
}

// Lifecycle
onMounted(() => {
  initVennDiagram()
  initTrendChart()
  
  window.addEventListener('resize', () => {
    vennChart.value?.resize()
    trendChart.value?.resize()
  })
})
</script>

<style scoped>
.vocabulary-gap {
  padding: 0;
  max-width: 100%;
  margin: 0 auto;
}

.gap-card {
  margin-bottom: 20px;
  background: #fff;
  width: 100%;
}

.card-header {
  display: flex;
  height: 100px;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 15px 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 500;
}

.header-illustration {
  width: 180px;
  height: auto;
  margin-right: 20px;
}

.venn-container {
  height: 500px;
  width: 100%;
  margin: 0 auto;
}

.trend-container {
  height: 400px;
  width: 100%;
  margin: 20px auto 0;
}

.info-icon {
  cursor: pointer;
  color: #909399;
  font-size: 16px;
}

.word-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px;
}
</style> 