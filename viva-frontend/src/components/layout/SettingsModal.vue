<template>
  <Teleport to="body">
    <div v-if="modelValue" class="settings-modal-overlay" @click="$emit('update:modelValue', false)">
      <div class="settings-modal" @click.stop>
        <div class="settings-header">
          <h2>Settings</h2>
          <button class="close-button" @click="$emit('update:modelValue', false)">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>

        <div class="settings-content">
          <div class="settings-sidebar">
            <button 
              v-for="(section, index) in sections" 
              :key="index"
              :class="['section-button', { active: currentSection === section.id }]"
              @click="currentSection = section.id"
            >
              <span class="material-symbols-outlined">{{ section.icon }}</span>
              {{ section.name }}
            </button>
          </div>

          <div class="settings-main">
            <!-- General Settings -->
            <div v-if="currentSection === 'general'" class="settings-section">
              <div class="setting-item">
                <div class="setting-label">Theme</div>
                <select v-model="settings.theme" class="setting-control">
                  <option value="system">System</option>
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                </select>
              </div>

              <div class="setting-item">
                <div class="setting-label">Always show code when using data analyst</div>
                <div class="toggle-switch">
                  <input type="checkbox" v-model="settings.showCode">
                  <span class="slider"></span>
                </div>
              </div>

              <div class="setting-item">
                <div class="setting-label">Show follow-up suggestions in chats</div>
                <div class="toggle-switch">
                  <input type="checkbox" v-model="settings.showSuggestions">
                  <span class="slider"></span>
                </div>
              </div>

              <div class="setting-item">
                <div class="setting-label">Language</div>
                <select v-model="settings.language" class="setting-control">
                  <option value="auto">Auto-detect</option>
                  <option value="en">English</option>
                  <option value="zh">中文</option>
                </select>
              </div>
            </div>

            <!-- Chat Management -->
            <div v-if="currentSection === 'chats'" class="settings-section">
              <div class="setting-item">
                <div class="setting-label">Archived chats</div>
                <button class="action-button">Manage</button>
              </div>

              <div class="setting-item">
                <div class="setting-label">Archive all chats</div>
                <button class="action-button">Archive all</button>
              </div>

              <div class="setting-item">
                <div class="setting-label">Delete all chats</div>
                <button class="action-button danger">Delete all</button>
              </div>
            </div>

            <div class="settings-footer">
              <button class="logout-button" @click="handleLogout">
                Log out on this device
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
export default {
  name: 'SettingsModal',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      currentSection: 'general',
      sections: [
        { id: 'general', name: 'General', icon: 'settings' },
        { id: 'notifications', name: 'Notifications', icon: 'notifications' },
        { id: 'personalization', name: 'Personalization', icon: 'person' },
        { id: 'speech', name: 'Speech', icon: 'mic' },
        { id: 'data', name: 'Data controls', icon: 'database' },
        { id: 'builder', name: 'Builder profile', icon: 'build' },
        { id: 'apps', name: 'Connected apps', icon: 'apps' },
        { id: 'security', name: 'Security', icon: 'security' },
      ],
      settings: {
        theme: 'system',
        showCode: false,
        showSuggestions: true,
        language: 'auto'
      }
    }
  },
  methods: {
    handleLogout() {
      // Implement logout logic here
      this.$emit('update:modelValue', false)
    }
  }
}
</script>

<style scoped>
.settings-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99999999;
}

.settings-modal {
  background-color: #fff;
  border-radius: 12px;
  width: 800px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 99999999;
}

.settings-header {
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.settings-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
}

.close-button:hover {
  background-color: #f5f5f5;
}

.settings-content {
  display: flex;
  height: 600px;
  overflow: hidden;
}

.settings-sidebar {
  width: 200px;
  border-right: 1px solid #eee;
  padding: 16px 0;
  overflow-y: auto;
}

.section-button {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
  gap: 12px;
  text-align: left;
}

.section-button:hover {
  background-color: #f5f5f5;
}

.section-button.active {
  background-color: #f0f0f0;
}

.settings-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.settings-section {
  flex: 1;
}

.setting-item {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.setting-label {
  font-size: 14px;
}

.setting-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  min-width: 150px;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.action-button {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
}

.action-button.danger {
  color: #ff4444;
  border-color: #ff4444;
}

.settings-footer {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.logout-button {
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  border: none;
  background-color: #f5f5f5;
  cursor: pointer;
  font-size: 14px;
}

.logout-button:hover {
  background-color: #eee;
}

/* Dark mode styles */
@media (prefers-color-scheme: dark) {
  .settings-modal {
    background-color: #1a1a1a;
    color: #fff;
  }

  .settings-header {
    border-bottom-color: #333;
  }

  .settings-sidebar {
    border-right-color: #333;
  }

  .section-button:hover {
    background-color: #2a2a2a;
  }

  .section-button.active {
    background-color: #333;
  }

  .setting-control {
    background-color: #2a2a2a;
    border-color: #444;
    color: #fff;
  }

  .action-button {
    background-color: #2a2a2a;
    border-color: #444;
    color: #fff;
  }

  .settings-footer {
    border-top-color: #333;
  }

  .logout-button {
    background-color: #2a2a2a;
    color: #fff;
  }

  .logout-button:hover {
    background-color: #333;
  }
}
</style> 