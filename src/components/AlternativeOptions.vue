<template>
  <div class="flex justify-start">
    <div class="bg-white rounded-2xl max-w-2xl shadow-lg border border-purple-100 overflow-hidden">
      <div class="p-5 space-y-4">
        <div class="flex items-start gap-3">
          <LightbulbIcon class="text-yellow-500 mt-1 flex-shrink-0" :size="24" />
          <div>
            <h3 class="text-lg font-bold text-gray-900">低步數替代方案</h3>
            <p class="text-sm text-gray-600 mt-1">了解！為您調整行程強度</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div
            v-for="(option, index) in options"
            :key="index"
            class="border-2 border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:bg-blue-50/50 transition-all cursor-pointer"
            @click="handleSelectOption(option)"
          >
            <div class="flex items-start gap-3">
              <component :is="getIconComponent(option.icon)" :size="20" :class="option.iconColor" />
              <div class="flex-1">
                <p class="font-medium text-gray-900">{{ option.title }}</p>
                <p class="text-sm text-gray-600 mt-1">{{ option.description }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <button
          @click="handleSelectOption(options[0])"
          class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-medium hover:shadow-lg transition-all"
        >
          選擇方案
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  Lightbulb as LightbulbIcon,
  Bus as BusIcon,
  Coffee as CoffeeIcon,
  Home as HomeIcon
} from 'lucide-vue-next';

const props = defineProps({
  options: {
    type: Array,
    required: true,
    default: () => [
      {
        icon: 'bus',
        iconColor: 'text-blue-500',
        title: '搭乘巴士前往下一站',
        description: '附近咖啡廳休息（步行2分鐘）'
      },
      {
        icon: 'coffee',
        iconColor: 'text-brown-500',
        title: '附近咖啡廳休息（步行2分鐘）',
        description: '放鬆一下再繼續行程'
      },
      {
        icon: 'home',
        iconColor: 'text-red-500',
        title: '回飯店休息，傍晚再出發',
        description: '充分休息後繼續探索'
      }
    ]
  }
});

const getIconComponent = (iconName) => {
  const iconMap = {
    'bus': BusIcon,
    'coffee': CoffeeIcon,
    'home': HomeIcon
  };
  return iconMap[iconName] || BusIcon;
};

const handleSelectOption = (option) => {
  console.log('選擇方案:', option);
  // 這裡可以觸發選擇方案的事件
};
</script>