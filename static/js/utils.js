/**
 * Utility functions for English Practice games
 */

function shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

function getRandomItems(array, count) {
    return shuffle(array).slice(0, count);
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.8;
    speechSynthesis.speak(utterance);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showStars(score, total) {
    const pct = total > 0 ? (score / total) * 100 : 0;
    if (pct >= 90) return '⭐⭐⭐';
    if (pct >= 70) return '⭐⭐';
    if (pct >= 40) return '⭐';
    return '💪 Cố gắng hơn nhé!';
}

function getAllWords(topicsData) {
    let words = [];
    for (const topic of topicsData) {
        for (const w of topic.words) {
            words.push({...w, topic: topic.id, topicName: topic.name_vi});
        }
    }
    return words;
}

function getWordsByTopic(topicsData, topicId) {
    if (topicId === 'all') return getAllWords(topicsData);
    const topic = topicsData.find(t => t.id === topicId);
    if (!topic) return [];
    return topic.words.map(w => ({...w, topic: topic.id, topicName: topic.name_vi}));
}
