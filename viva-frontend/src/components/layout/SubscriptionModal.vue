<template>
  <div v-if="modelValue" class="modal-overlay" @click="$emit('update:modelValue', false)">
    <div class="modal-content" @click.stop>
      <h1 class="modal-title">Choose your plan</h1>
      
      <div class="plan-toggle">
        <button :class="['toggle-btn', { active: planType === 'personal' }]" @click="planType = 'personal'">Personal</button>
        <button :class="['toggle-btn', { active: planType === 'Team' }]" @click="planType = 'Team'">Team</button>
      </div>

      <div class="plans-container">
        <div class="plan-card">
          <h2>Free</h2>
          <div class="price">
            <span class="currency">$</span>
            <span class="amount">0</span>
            <span class="period">USD/month</span>
          </div>
          <p class="description">从语境中用 AI 反向映射，帮助你构建起自己的英语世界</p>
          <button class="plan-button">Free</button>
          
          <div class="features">
            <div class="feature">
              <span class="check">✓</span>
              Extended limits on messaging, file uploads, advanced data analysis, and image generation
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Standard and advanced voice mode
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Access to multiple reasoning models (o3-mini, o3-mini-high, and o1)
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Create and use projects and custom GPTs
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Limited access to Sora video generation
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Opportunities to test new features
            </div>
          </div>
          <p class="limits">Limits apply</p>
        </div>

        <div class="plan-card pro">
          <h2>Pro</h2>
          <div class="price">
            <span class="currency">$</span>
            <span class="amount">1</span>
            <span class="period">USD/month</span>
          </div>
          <p class="description"> 最好的模型，最全面的学习数据分析</p>
          <button class="plan-button">Get Pro</button>
          
          <div class="features">
            <div class="feature">
              <span class="check">✓</span>
              Everything in Free
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Unlimited access to all reasoning models and GPT-4o
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Unlimited access to advanced voice
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Access to deep research and o1 pro mode, which uses more compute for the best answers to the hardest questions
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Extended access to Sora video generation
            </div>
            <div class="feature">
              <span class="check">✓</span>
              Access to research preview of Operator
            </div>
          </div>
          <div class="links">
            <a href="#" class="help-link">I need help with a billing issue</a>
            <p class="note">Unlimited subject to abuse guardrails. <a href="#" class="learn-more">Learn more</a></p>
          </div>
        </div>
      </div>

      <div class="enterprise-section">
        <span class="icon material-symbols-outlined">groups</span>
        <p>有更多好的想法?</p>
        <a href="#" class="enterprise-link">联系我们</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SubscriptionModal',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      planType: 'personal'
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 32px;
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-title {
  text-align: center;
  font-size: 32px;
  margin-bottom: 24px;
}

.plan-toggle {
  display: flex;
  justify-content: center;
  background: #f0f0f0;
  padding: 4px;
  border-radius: 24px;
  width: fit-content;
  margin: 0 auto 32px;
}

.toggle-btn {
  padding: 8px 24px;
  border: none;
  background: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
}

.toggle-btn.active {
  background: white;
  font-weight: 600;
}

.plans-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.plan-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  padding: 24px;
}

.plan-card h2 {
  font-size: 24px;
  margin-bottom: 16px;
}

.price {
  margin-bottom: 16px;
  display: flex;
  align-items: baseline;
}

.currency {
  font-size: 24px;
  font-weight: 600;
}

.amount {
  font-size: 48px;
  font-weight: 600;
  margin-right: 8px;
}

.period {
  color: #666;
  font-size: 14px;
}

.description {
  color: #333;
  margin-bottom: 24px;
}

.plan-button {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background: var(--color-button-dark);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 24px;
}

.pro .plan-button {
  background: var(--color-button-dark);
}

.features {
  margin-bottom: 24px;
}

.feature {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  font-size: 14px;
  line-height: 1.4;
}

.check {
  color: #10a37f;
  margin-right: 8px;
  font-weight: bold;
}

.limits {
  color: #666;
  font-size: 14px;
}

.links {
  margin-top: 24px;
}

.help-link {
  color: #666;
  text-decoration: underline;
  font-size: 14px;
  display: block;
  margin-bottom: 8px;
}

.note {
  color: #666;
  font-size: 14px;
}

.learn-more {
  color: #666;
  text-decoration: underline;
}

.enterprise-section {
  text-align: center;
  padding: 24px;
  background: #f9f9f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.enterprise-section .icon {
  font-size: 24px;
}

.enterprise-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

@media (prefers-color-scheme: dark) {
  .modal-content {
    background: #1a1a1a;
    color: white;
  }

  .plan-toggle {
    background: #2a2a2a;
  }

  .toggle-btn.active {
    background: #333;
  }

  .plan-card {
    background: #2a2a2a;
    border-color: #333;
  }

  .period, .description, .limits, .help-link, .note {
    color: #999;
  }

  .enterprise-section {
    background: #2a2a2a;
  }
}
</style> 