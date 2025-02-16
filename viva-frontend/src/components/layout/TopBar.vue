<template>
    <div class="top-bar">
      <div class="search-group">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input 
          type="text" 
          class="search-input" 
          placeholder="搜你想搜的" 
          v-model="searchQuery"
          @input="handleSearch"
        />
      </div>
      <div class="nav-links">
        <router-link to="/creator" class="nav-link">加入社群</router-link>
        <router-link to="/business" class="nav-link">业务合作</router-link>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const searchQuery = ref('');

const handleSearch = () => {
  // 处理搜索逻辑
  console.log('Searching for:', searchQuery.value);
};
</script>

<style scoped>
.top-bar {
  padding: 1rem 2rem;
  border-bottom: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #FFFFFF;
}

.search-group {
  display: flex;
  line-height: 28px;
  align-items: center;
  position: relative;
  max-width: 400px;
  padding-top: 15px;
  width: 100%;
  margin-left: 200px;
}

.search-input {
  width: 100%;
  height: 40px;
  line-height: 28px;
  padding: 0 1rem;
  padding-left: 2.5rem;
  border: 2px solid transparent;
  border-radius: 8px;
  outline: none;
  background-color: #f3f3f4;
  color: #0d0c22;
  transition: .3s ease;
  font-size: 14px;
}

.search-input::placeholder {
  color: #9e9ea7;
}

.search-input:focus, 
.search-input:hover {
  outline: none;
  border-color: #1D1D1F;
  background-color: #fff;
}

.search-icon {
  position: absolute;
  left: 1rem;
  width: 1rem;
  height: 1rem;
  color: #9e9ea7;
  pointer-events: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
  padding-top: 15px;
}

.nav-link {
  text-decoration: none;
  color: #1D1D1F;
  font-size: 14px;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--color-primary);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .top-bar {
    background-color: #1a1a1a;
    border-bottom: none;
  }

  .search-input {
    background-color: #2c2c2e;
    color: #ffffff;
  }

  .search-input::placeholder {
    color: #6e6e73;
  }

  .search-input:focus,
  .search-input:hover {
    background-color: #3c3c3e;
    border-color: rgba(234,76,137,0.4);
    box-shadow: 0 0 0 4px rgba(234,76,137,0.2);
  }

  .nav-link {
    color: #ffffff;
  }

  .nav-link:hover {
    color: #EA4C89;
  }
}

/* Mobile responsive */
@media (max-width: 768px) {
  .top-bar {
    padding: 0.75rem 1rem;
  }

  .search-group {
    max-width: 100%;
  }

  .search-input {
    height: 36px;
    font-size: 13px;
  }

  .nav-links {
    gap: 1rem;
  }

  .nav-link {
    font-size: 13px;
  }
}
</style>