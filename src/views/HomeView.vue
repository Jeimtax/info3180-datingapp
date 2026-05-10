<template>
  <div class="home-wrapper">
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Find Your <span class="gradient-text">Drift</span></h1>
        <p class="hero-subtitle">
          DriftDater connects you with people who share your vibe — based on location,
          age, and interests. Create a profile, explore matches, and start a conversation.
        </p>
        <div class="hero-actions">
          <RouterLink to="/register" class="btn-primary">Get Started</RouterLink>
          <RouterLink to="/login" class="btn-secondary">Login</RouterLink>
        </div>
      </div>
      <div class="hero-visual">
        <div class="card-stack">
          <div class="fake-card fc3">
            <div class="fc-pic" style="background: #c7d2fe"></div>
            <div class="fc-lines">
              <div class="fc-line long"></div>
              <div class="fc-line short"></div>
            </div>
          </div>
          <div class="fake-card fc2">
            <div class="fc-pic" style="background: #ddd6fe"></div>
            <div class="fc-lines">
              <div class="fc-line long"></div>
              <div class="fc-line short"></div>
            </div>
          </div>
          <div class="fake-card fc1">
            <div class="fc-pic" style="background: linear-gradient(135deg, #6366f1, #8b5cf6)"></div>
            <div class="fc-lines">
              <div class="fc-line long"></div>
              <div class="fc-line short"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">👤</div>
        <h3>Build Your Profile</h3>
        <p>Add your photo, bio, hobbies, and relationship goals so others can get to know you.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Explore and Filter</h3>
        <p>Browse profiles filtered by age, location, and shared interests. Like or pass with one click.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>Chat with Matches</h3>
        <p>When two people like each other it is a match. Unlock messaging and start the conversation.</p>
      </div>
    </div>

    <div class="cta-section">
      <h2>Ready to meet someone?</h2>
      <RouterLink to="/register" class="btn-cta">Create a Free Account</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.home-wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 24px 80px;
}

.hero {
  display: flex;
  align-items: center;
  gap: 60px;
  margin-bottom: 80px;
}

.hero-content {
  flex: 1;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: #1f2937;
  margin: 0 0 16px;
  line-height: 1.15;
}

.gradient-text {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #6b7280;
  line-height: 1.7;
  margin: 0 0 32px;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 14px 32px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
}

.btn-secondary {
  padding: 14px 32px;
  background: white;
  color: #6366f1;
  border: 2px solid #6366f1;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
}

.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
}

.card-stack {
  position: relative;
  width: 220px;
  height: 280px;
}

.fake-card {
  position: absolute;
  width: 200px;
  height: 260px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fc1 {
  top: 0;
  left: 20px;
  z-index: 3;
}

.fc2 {
  top: 14px;
  left: 10px;
  z-index: 2;
  transform: rotate(-4deg);
}

.fc3 {
  top: 24px;
  left: 0;
  z-index: 1;
  transform: rotate(-8deg);
}

.fc-pic {
  height: 140px;
  border-radius: 10px;
}

.fc-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 4px;
}

.fc-line {
  height: 10px;
  border-radius: 6px;
  background: #e5e7eb;
}

.fc-line.long {
  width: 80%;
}

.fc-line.short {
  width: 50%;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 80px;
}

.feature-card {
  background: white;
  border-radius: 14px;
  padding: 28px 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.feature-card h3 {
  color: #1f2937;
  margin: 0 0 10px;
  font-size: 1.1rem;
}

.feature-card p {
  color: #6b7280;
  font-size: 0.93rem;
  line-height: 1.6;
  margin: 0;
}

.cta-section {
  text-align: center;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 20px;
  padding: 60px 24px;
  color: white;
}

.cta-section h2 {
  font-size: 1.8rem;
  margin: 0 0 24px;
}

.btn-cta {
  display: inline-block;
  padding: 14px 36px;
  background: white;
  color: #6366f1;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
}

@media (max-width: 700px) {
  .hero {
    flex-direction: column;
    gap: 40px;
    text-align: center;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .hero-subtitle {
    max-width: 100%;
  }

  .hero-actions {
    justify-content: center;
  }

  .hero-visual {
    display: none;
  }
}
</style>
