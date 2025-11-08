import { embedText } from "./Embedding.js";

export async function findClosestTopic(text) {
  const response = await fetch("../Train/VectorData.json");
  const dataset = await response.json();

  const userVec = embedText(text);
  let bestMatch = null;
  let bestScore = -1;

  for (const topic of dataset.topics) {
    const score = cosineSimilarity(userVec, topic.vector);
    if (score > bestScore) {
      bestScore = score;
      bestMatch = topic;
    }
  }

  return bestMatch;
}

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}
