<template>
  <div class="progress-dashboard">
    <!-- KPI Metric Cards -->
    <el-row :gutter="20" class="metric-cards">
      <el-col :span="6" v-for="(metric, index) in metrics" :key="index">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-content">
            <div class="metric-circle">
              <el-progress
                type="circle"
                :percentage="Math.round((metric.current / metric.total) * 100)"
                :color="getProgressColor(metric.current / metric.total)"
                :stroke-width="10"
                :width="120"
              >
                <template #default="{ percentage }">
                  <div class="progress-content">
                    <span class="progress-value">{{ percentage }}%</span>
                    <span class="progress-label">{{ metric.title }}</span>
                    <span class="progress-detail">{{ metric.current }}/{{ metric.total }}</span>
                  </div>
                </template>
              </el-progress>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Progress Section -->
    <el-row :gutter="20" class="progress-section">
      <el-col :span="16">
        <el-card shadow="hover" class="chart-card">
          <div slot="header" class="clearfix">
            <span>词汇掌握进度趋势</span>
            <el-select v-model="selectedTimeRange" size="small" style="float: right">
              <el-option label="最近一周" value="week" />
              <el-option label="最近一月" value="month" />
              <el-option label="最近三月" value="quarter" />
              <el-option label="最近一年" value="year" />
            </el-select>
          </div>
          <div class="chart-container" ref="lineChart"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="chart-card">
          <div slot="header" class="clearfix">
            <span>词汇分布</span>
          </div>
          <div class="chart-container" ref="donutChart"></div>
        </el-card>
      </el-col>
    </el-row>

   
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import api from '@/services/api'

// Data
const metrics = ref([
  { title: '前1000词', current: 800, total: 1000 },
  { title: '前3000词', current: 2400, total: 3000 },
  { title: '前5000词', current: 3800, total: 5000 },
  { title: '前10000词', current: 6000, total: 10000 }
])

const selectedTimeRange = ref('month')
const vocabularyLevels = ref([
  { name: '基础词汇 (1-1000)', mastered: 800, total: 1000 },
  { name: '进阶词汇 (1001-3000)', mastered: 1600, total: 2000 },
  { name: '高级词汇 (3001-5000)', mastered: 1400, total: 2000 },
  { name: '专业词汇 (5001-10000)', mastered: 2200, total: 5000 }
])

let lineChart = null
let donutChart = null

// Methods
const getProgressColor = (percentage) => {
  if (percentage >= 0.8) return '#1E88E5' // 深蓝
  if (percentage >= 0.6) return '#42A5F5' // 中蓝
  if (percentage >= 0.4) return '#90CAF9' // 浅蓝
  return '#E3F2FD' // 非常浅的蓝
}

const initLineChart = () => {
  const chartDom = document.querySelector('.chart-container')
  lineChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['前1000词', '前3000词', '前5000词', '前10000词']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: {
      type: 'value',
      max: 100,
      name: '掌握度(%)'
    },
    series: [
      {
        name: '前1000词',
        type: 'line',
        data: [80, 82, 85, 87, 89, 90],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#1E88E5' }
      },
      {
        name: '前3000词',
        type: 'line',
        data: [60, 63, 65, 68, 70, 72],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#42A5F5' }
      },
      {
        name: '前5000词',
        type: 'line',
        data: [40, 42, 45, 48, 50, 52],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#90CAF9' }
      },
      {
        name: '前10000词',
        type: 'line',
        data: [20, 22, 25, 28, 30, 32],
        smooth: true,
        lineStyle: { width: 3 },
        itemStyle: { color: '#E3F2FD' }
      }
    ]
  }
  lineChart.setOption(option)
}

const initDonutChart = () => {
  const chartDom = document.querySelectorAll('.chart-container')[1]
  donutChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '词汇分布',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '20',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 800, name: '基础词汇', itemStyle: { color: '#E3F2FD' } },
          { value: 1600, name: '进阶词汇', itemStyle: { color: '#90CAF9' } },
          { value: 1400, name: '高级词汇', itemStyle: { color: '#42A5F5' } },
          { value: 2200, name: '专业词汇', itemStyle: { color: '#1E88E5' } }
        ]
      }
    ]
  }
  donutChart.setOption(option)
}

// Lifecycle
onMounted(() => {
  initLineChart()
  initDonutChart()
  window.addEventListener('resize', () => {
    lineChart?.resize()
    donutChart?.resize()
  })
})

</script>

<style scoped>
.progress-dashboard {
  padding: 20px;
}

.metric-cards {
  margin-bottom: 20px;
}

.metric-card {
  height: auto;
  padding: 20px;
  transition: all 0.3s;
  background: #fff;
}

.metric-card:hover {
  transform: translateY(-5px);
}

.metric-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.metric-circle {
  text-align: center;
}

.progress-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.3;
}

.progress-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.progress-label {
  font-size: 14px;
  color: #606266;
  margin: 4px 0;
}

.progress-detail {
  font-size: 12px;
  color: #909399;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.progress-bars {
  padding: 10px;
}

.progress-bar-item {
  margin-bottom: 20px;
}

.level-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.level-name {
  font-size: 14px;
  color: #606266;
}

.level-stats {
  font-size: 14px;
  color: #909399;
}

.clearfix::after {
  content: '';
  display: table;
  clear: both;
}
</style> 