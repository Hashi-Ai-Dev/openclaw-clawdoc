#!/usr/bin/env node
/**
 * honcho-write: Write conclusions to Honcho memory
 * Usage:
 *   node write-conclusion.mjs "<content>" <observer_id> <observed_id> [session_id]
 *   node write-conclusion.mjs "Learned X" "claw-doc" "claw-doc"
 */

const BASE_URL = 'http://127.0.0.1:8000';
const WORKSPACE = 'hashi';

async function ensurePeer(peerId) {
  const res = await fetch(`${BASE_URL}/v3/workspaces/${WORKSPACE}/peers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: peerId,
      metadata: { role: 'agent' },
      configuration: {}
    })
  });
  // 409 means already exists, that's fine
  if (!res.ok && res.status !== 409) {
    const err = await res.text();
    throw new Error(`Peer creation failed: ${res.status} ${err}`);
  }
}

async function writeConclusion(content, observerId, observedId, sessionId = null) {
  // Ensure observer peer exists
  await ensurePeer(observerId);

  const payload = {
    conclusions: [{
      content,
      observer_id: observerId,
      observed_id: observedId,
      session_id: sessionId
    }]
  };

  const res = await fetch(`${BASE_URL}/v3/workspaces/${WORKSPACE}/conclusions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Conclusion write failed: ${res.status} ${err}`);
  }

  const result = await res.json();
  return result;
}

// CLI mode
const [,, content, observerId, observedId, sessionId] = process.argv;
if (content && observerId && observedId) {
  writeConclusion(content, observerId, observedId, sessionId || null)
    .then(r => {
      console.log(JSON.stringify(r, null, 2));
      process.exit(0);
    })
    .catch(e => {
      console.error(e.message);
      process.exit(1);
    });
} else {
  console.error('Usage: node write-conclusion.mjs "<content>" <observer_id> <observed_id> [session_id]');
  process.exit(1);
}

export { writeConclusion };
