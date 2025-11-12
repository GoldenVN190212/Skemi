export function embedText(text) {
  const words = text.toLowerCase().replace(/[^a-z0-9\s]/g, "").split(/\s+/);
  const vector = new Array(100).fill(0);

  for (const w of words) {
    let sum = 0;
    for (let i = 0; i < w.length; i++) sum += w.charCodeAt(i);
    vector[sum % 100] += 1;
  }

  return normalize(vector);
}

function normalize(vec) {
  const len = Math.sqrt(vec.reduce((a, b) => a + b * b, 0));
  return vec.map((x) => (len === 0 ? 0 : x / len));
}
