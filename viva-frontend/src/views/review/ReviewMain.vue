<template>
  <el-container style="height: 100vh;  flex-direction: column;">
    <el-main style="flex: 1;  flex-direction: column;">
      <el-row :gutter="20" style="flex: 1; ">
        <!-- 今日复习统计 -->
        <el-col :span="24">
          <el-card shadow="hover" style="margin-bottom: 20px;">
            <div slot="header" class="clearfix">
              <span>今日复习统计</span>
            </div>
            <el-row style="display: flex; flex-direction: row;">
              <el-col :span="8">
                <div class="stat-item"
                     style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                  <h3>今日复习单词</h3>
                  <p>{{ reviewStat.todayReviewCount }}</p>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item"
                     style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                  <h3>今日待复习单词</h3>
                  <p>{{ reviewStat.todayNeedReviewCount }}</p>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item"
                     style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                  <h3>已熟知单词</h3>
                  <p>{{ reviewStat.totalKnowWordReviewCount }}</p>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </el-col>

        <!-- 开始学习按钮 -->
        <el-col :span="24" style="text-align: center; margin-bottom: 20px;">
          <el-button style="width: 60%; min-height: 50px" type="primary" @click="startLearning">开始学习</el-button>
        </el-col>

        <!-- 学习热力图 -->
        <el-col :span="24">
          <el-card shadow="hover" style="flex: 1;">
            <div slot="header" class="clearfix">
              <span>学习热力图</span>
            </div>
            <div id="heatmapContainer" style="width: 100%; height: 100%;"></div>
            <div style="float: right; fontSize: 12 "/>
            <span style="color: #768390">Less</span>
            <div id="ex-ghDay-legend" style="display: inline-block; margin: 0 4px"></div>
            <span style="color: #768390; fontSize: 12">More</span>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>

  <ReviewWordModal v-if="showReviewWord" @close="closeModal"/>
</template>

<script setup>
import {onMounted, ref, watch} from 'vue'
import {useRoute} from 'vue-router'
import api from '@/services/api'
import CalHeatmap from 'cal-heatmap'
import 'cal-heatmap/cal-heatmap.css';
import Tooltip from 'cal-heatmap/plugins/Tooltip';
import LegendLite from 'cal-heatmap/plugins/LegendLite';
import CalendarLabel from "cal-heatmap/plugins/CalendarLabel";
import ReviewWordModal from "@/views/review/ReviewWordModal.vue";


const route = useRoute()
const showReviewWord = ref(false)
const reviewStat = ref({"todayReviewCount": 0, "todayNeedReviewCount": 0, "totalKnowWordReviewCount": 0})

const fetchData = async () => {

};

const closeModal = () => {
  showReviewWord.value = false
}

const getHeatmapData = async () => {
  try {
    const response = await api.getReviewDayStat(getLastYearFormattedDate(), getFormattedDate())
    const data = response.data;
    if (data.status !== 0) {
      throw new Error('Failed to fetch word stats');
    }
    return data.data;
  } catch (error) {
    console.error('Error fetching word stats:', error);
  }
};

const getReviewStatData = async () => {
  try {
    const response = await api.getReviewStat();
    const data = response.data;
    if (data.status !== 0) {
      throw new Error('Failed to fetch word stats');
    }
    reviewStat.value = data.data;
    console.log(reviewStat.value)
    return data.data;
  } catch (error) {
    console.error('Error fetching word stats:', error);
  }
};


const initHeatmap = async () => {
  const heatmap = new CalHeatmap();
  await heatmap.paint({
    data: {source: await getHeatmapData(), x: (datum) => +new Date(datum['date']), y: (datum) => +datum['value'],},
    date: {start: new Date()},
    range: 12,
    scale: {
      color: {
        type: 'threshold',
        range: ['#14432a', '#166b34', '#37a446', '#4dd05a'],
        domain: [10, 20, 30],
      },
    },
    domain: {
      type: 'month',
      gutter: 4,
      label: {text: 'MMM', textAlign: 'start', position: 'top'},
    },
    subDomain: {type: 'ghDay', radius: 2, width: 11, height: 11, gutter: 4},
    itemSelector: '#heatmapContainer',
  }, [
    [
      Tooltip,
      {
        text: function (date, value, dayjsDate) {
          return (
              (value ? value : 'No') +
              ' learning on ' +
              dayjsDate.format('dddd, MMMM D, YYYY')
          );
        },
      },
    ],
    [
      LegendLite,
      {
        includeBlank: true,
        itemSelector: '#ex-ghDay-legend',
        radius: 2,
        width: 11,
        height: 11,
        gutter: 4,
      },
    ],
    [
      CalendarLabel,
      {
        width: 30,
        textAlign: 'start',
        text: () => dayjs.weekdaysShort().map((d, i) => (i % 2 === 0 ? '' : d)),
        padding: [25, 0, 0, 0],
      },
    ],
  ]);
}

onMounted(() => {
  console.log("切换到ReviewMain")
  fetchData()
  initHeatmap()
  getReviewStatData()
})

// 监听路由变化，重新获取文章列表
watch(() => route.fullPath, initHeatmap)

const startLearning = () => {
  showReviewWord.value = true
  console.log(showReviewWord.value)
  // 这里可以添加跳转到学习页面或触发学习逻辑的代码
}


const getFormattedDate = () => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const getLastYearFormattedDate = () => {
  const now = new Date();
  const year = now.getFullYear() - 1;
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
</script>

<style scoped>.stat-item {
  text-align: center;
}

.stat-item h3 {
  margin-bottom: 8px;
  font-size: 1.2em;
}

.stat-item p {
  font-size: 2em;
  font-weight: bold;
  color: #409eff;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-main {
  padding: 20px;
}

.el-button--primary {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

/* 添加间距和样式 */
.el-card {
  margin-bottom: 20px;
}

/* 确保按钮居中 */
.el-col button {
  margin: 0 auto;
}

/* 确保热力图容器有足够的高度 */
#heatmapContainer {
  min-height: 150px; /* 根据需要调整高度 */
}
</style>