<template>
  <div class="h-full overflow-y-auto p-4 pb-6" ref="chatContainer">
    <div class="max-w-4xl mx-auto space-y-4">
      <div v-for="(message, index) in messages" :key="index">
        <UserMessage v-if="message.type === 'user'" :message="message" />
        <AssistantMessage v-else-if="message.type === 'assistant'" :message="message" />
        <ItineraryCard 
          v-else-if="message.type === 'itinerary'" 
          :data="message.data" 
          @view-details="handleViewItinerary"
        />
        <AlternativeOptions v-else-if="message.type === 'alternative'" :options="message.options" />
      </div>
      <div ref="messagesEnd"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import UserMessage from './UserMessage.vue';
import AssistantMessage from './AssistantMessage.vue';
import ItineraryCard from './ItineraryCard.vue';
import AlternativeOptions from './AlternativeOptions.vue';

const props = defineProps({
  messages: {
    type: Array,
    required: true
  },
  selectedImage: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['view-itinerary', 'remove-image']);

const messagesEnd = ref(null);
const chatContainer = ref(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesEnd.value) {
      messagesEnd.value.scrollIntoView({ behavior: 'smooth' });
    }
  });
};

const handleViewItinerary = (data) => {
  emit('view-itinerary', data);
};

watch(() => props.messages.length, () => {
  scrollToBottom();
});
</script>