<template>
  <div class="messages-layout">

    <div class="conversations-panel" :class="{ 'hidden-mobile': activeConvo }">
      <h2>Messages</h2>

      <div v-if="isLoadingConvos" class="state-msg">Loading...</div>

      <div v-else-if="conversations.length === 0" class="state-msg empty">
        <p>No conversations yet.</p>
        <router-link to="/matches" class="btn-link">Go to Matches</router-link>
      </div>

      <div v-else class="convo-list">
        <div
          v-for="convo in conversations"
          :key="convo.user_id"
          class="convo-item"
          :class="{ active: activeConvo?.user_id === convo.user_id }"
          @click="selectConvo(convo)"
        >
          <img v-if="picFor(convo) && !failedPics.has(convo.user_id)" :src="picFor(convo)" :alt="convo.name" class="convo-pic" @error="failedPics.add(convo.user_id)" />
          <div v-else class="convo-pic placeholder">{{ convo.name?.[0] }}</div>
          <div class="convo-info">
            <span class="convo-name">{{ convo.name }}</span>
            <span class="last-msg">{{ convo.last_message }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="thread-panel" :class="{ 'hidden-mobile': !activeConvo }">

      <div v-if="!activeConvo" class="no-convo">
        <p>Select a conversation to start chatting</p>
      </div>

      <template v-else>
        <div class="thread-header">
          <button class="btn-back" @click="activeConvo = null">&#8592;</button>
          <img v-if="picFor(activeConvo) && !failedPics.has(activeConvo.user_id)" :src="picFor(activeConvo)" :alt="activeConvo.name" class="header-pic" @error="failedPics.add(activeConvo.user_id)" />
          <div v-else class="header-pic placeholder">{{ activeConvo.name?.[0] }}</div>
          <span class="header-name">{{ activeConvo.name }}</span>
        </div>

        <div class="thread-messages" ref="threadEl">
          <div v-if="isLoadingMsgs" class="state-msg">Loading messages...</div>
          <template v-else>
            <div v-if="messages.length === 0" class="state-msg">No messages yet. Say hi!</div>
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="bubble-row"
              :class="msg.is_mine ? 'mine' : 'theirs'"
            >
              <div class="bubble">
                <p>{{ msg.content }}</p>
                <span class="ts">{{ formatTime(msg.timestamp) }}</span>
              </div>
            </div>
          </template>
        </div>

        <!-- Input -->
        <div class="thread-input">
          <input
            v-model="draft"
            type="text"
            placeholder="Type a message..."
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage" :disabled="!draft.trim() || isSending">Send</button>
        </div>
      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const conversations = ref([]);
const isLoadingConvos = ref(true);
const activeConvo = ref(null);
const messages = ref([]);
const isLoadingMsgs = ref(false);
const isSending = ref(false);
const draft = ref('');
const threadEl = ref(null);
const failedPics = reactive(new Set());

let pollInterval = null;

function picFor(convo) {
  if (!convo?.pic || convo.pic === 'default.png') return null;
  return 'http://localhost:5000/static/uploads/' + convo.pic;
}

function formatTime(iso) {
  const d = new Date(iso);
  const today = new Date();
  const isToday = d.toDateString() === today.toDateString();
  return isToday
    ? d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : d.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ' ' +
      d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

async function fetchConversations() {
  const token = localStorage.getItem('token');
  try {
    const res = await fetch('http://localhost:5000/api/v1/conversations', {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    if (res.ok) conversations.value = data.conversations;
  } catch (e) {
    console.error('Error loading conversations:', e);
  } finally {
    isLoadingConvos.value = false;
  }
}

async function fetchMessages(userId) {
  isLoadingMsgs.value = true;
  const token = localStorage.getItem('token');
  try {
    const res = await fetch(`http://localhost:5000/api/v1/messages/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    if (res.ok) {
      messages.value = data.messages;
      await nextTick();
      scrollToBottom();
    }
  } catch (e) {
    console.error('Error loading messages:', e);
  } finally {
    isLoadingMsgs.value = false;
  }
}

async function pollMessages() {
  if (!activeConvo.value) return;
  const token = localStorage.getItem('token');
  try {
    const res = await fetch(`http://localhost:5000/api/v1/messages/${activeConvo.value.user_id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    if (res.ok && data.messages.length !== messages.value.length) {
      messages.value = data.messages;
      await nextTick();
      scrollToBottom();
    }
  } catch (e) { /* silent */ }
}

async function sendMessage() {
  if (!draft.value.trim() || isSending.value) return;
  isSending.value = true;
  const token = localStorage.getItem('token');
  const content = draft.value.trim();
  draft.value = '';
  try {
    const res = await fetch(`http://localhost:5000/api/v1/messages/${activeConvo.value.user_id}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    const data = await res.json();
    if (res.ok) {
      messages.value.push(data);
      activeConvo.value.last_message = content;
      await nextTick();
      scrollToBottom();
    } else {
      draft.value = content;
      alert(data.error || 'Failed to send message.');
    }
  } catch (e) {
    draft.value = content;
    console.error('Send error:', e);
  } finally {
    isSending.value = false;
  }
}

function selectConvo(convo) {
  activeConvo.value = convo;
  messages.value = [];
  fetchMessages(convo.user_id);
  router.replace({ name: 'conversation', params: { userId: convo.user_id } });
  startPolling();
}

function startPolling() {
  stopPolling();
  pollInterval = setInterval(pollMessages, 3000);
}

function stopPolling() {
  if (pollInterval) { clearInterval(pollInterval); pollInterval = null; }
}

function scrollToBottom() {
  if (threadEl.value) threadEl.value.scrollTop = threadEl.value.scrollHeight;
}

async function initFromRouteParam() {
  const userId = route.params.userId ? parseInt(route.params.userId) : null;
  if (!userId) return;

  const existing = conversations.value.find(c => c.user_id === userId);
  if (existing) {
    selectConvo(existing);
    return;
  }

  const token = localStorage.getItem('token');
  try {
    const res = await fetch(`http://localhost:5000/api/v1/users/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    if (res.ok) {
      selectConvo({ user_id: userId, name: data.name, pic: data.pic, last_message: '' });
    }
  } catch (e) {
    console.error('Could not load user:', e);
  }
}

watch(() => route.params.userId, async (newId) => {
  if (!newId) { activeConvo.value = null; stopPolling(); return; }
  await initFromRouteParam();
});

watch(activeConvo, (val) => {
  if (!val) stopPolling();
});

onMounted(async () => {
  await fetchConversations();
  await initFromRouteParam();
});

onUnmounted(stopPolling);
</script>

<style scoped>
.messages-layout {
  display: flex;
  height: calc(100vh - 60px);
  margin-top: 60px;
  overflow: hidden;
}

.conversations-panel {
  width: 300px;
  min-width: 300px;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  background: #fafafa;
}

.conversations-panel h2 {
  padding: 20px;
  margin: 0;
  font-size: 1.2rem;
  color: #6366f1;
  border-bottom: 1px solid #e5e7eb;
}

.convo-list { overflow-y: auto; flex: 1; }

.convo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.15s;
}
.convo-item:hover, .convo-item.active { background: #ede9fe; }

.convo-pic { width: 46px; height: 46px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.convo-pic-wrap { flex-shrink: 0; }
.placeholder {
  width: 46px; height: 46px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; font-weight: 700; font-size: 1.1rem;
  display: flex; align-items: center; justify-content: center;
}

.convo-info { min-width: 0; }
.convo-name { display: block; font-weight: 600; color: #1f2937; font-size: 0.95rem; }
.last-msg {
  display: block; color: #9ca3af; font-size: 0.82rem;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px;
}


.thread-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.no-convo {
  flex: 1; display: flex; align-items: center; justify-content: center;
  color: #9ca3af; font-size: 1rem;
}

.thread-header {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 20px; border-bottom: 1px solid #e5e7eb;
  background: white;
}

.btn-back {
  background: none; border: none; font-size: 1.3rem;
  cursor: pointer; color: #6366f1; display: none; padding: 0;
}

.header-pic-wrap { flex-shrink: 0; }
.header-pic { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
.header-pic.placeholder {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.header-name { font-weight: 600; color: #1f2937; font-size: 1rem; }

.thread-messages {
  flex: 1; overflow-y: auto;
  padding: 20px; display: flex; flex-direction: column; gap: 10px;
  background: #f9fafb;
}

.bubble-row { display: flex; }
.bubble-row.mine { justify-content: flex-end; }
.bubble-row.theirs { justify-content: flex-start; }

.bubble {
  max-width: 65%; padding: 10px 14px;
  border-radius: 18px; word-break: break-word;
}
.mine .bubble { background: #6366f1; color: white; border-bottom-right-radius: 4px; }
.theirs .bubble { background: white; color: #1f2937; border-bottom-left-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }

.bubble p { margin: 0 0 4px; font-size: 0.95rem; }
.ts { font-size: 0.72rem; opacity: 0.7; }
.mine .ts { color: rgba(255,255,255,0.8); }

.thread-input {
  display: flex; gap: 10px;
  padding: 14px 20px; border-top: 1px solid #e5e7eb; background: white;
}

.thread-input input {
  flex: 1; padding: 10px 14px;
  border: 1px solid #d1d5db; border-radius: 24px;
  font-size: 0.95rem; outline: none;
}
.thread-input input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }

.thread-input button {
  padding: 10px 22px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border: none; border-radius: 24px;
  font-weight: 600; cursor: pointer;
}
.thread-input button:disabled { opacity: 0.5; cursor: not-allowed; }


.state-msg { text-align: center; color: #9ca3af; margin-top: 40px; font-size: 0.95rem; }
.empty { display: flex; flex-direction: column; align-items: center; gap: 12px; }
.btn-link {
  padding: 8px 20px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; border-radius: 8px; text-decoration: none; font-weight: 600;
}


@media (max-width: 640px) {
  .conversations-panel { width: 100%; min-width: unset; }
  .hidden-mobile { display: none; }
  .btn-back { display: block; }
}
</style>