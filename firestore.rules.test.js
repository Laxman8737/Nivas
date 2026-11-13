// NOT RUN in this delivery (needs the Firebase emulator, which could not be installed offline).
// Run: npm i -D @firebase/rules-unit-testing && firebase emulators:exec --only firestore "node tests/firestore.rules.test.js"
const { initializeTestEnvironment, assertFails } = require('@firebase/rules-unit-testing');
const fs = require('fs');
(async () => {
  const env = await initializeTestEnvironment({ projectId: 'nivas-test', firestore: { rules: fs.readFileSync('firestore.rules', 'utf8') } });
  const a = env.authenticatedContext('alice', { email_verified: true }).firestore();
  const b = env.authenticatedContext('bob', { email_verified: true }).firestore();
  const anon = env.unauthenticatedContext().firestore();
  await assertFails(anon.collection('owners').doc('alice').get());
  await assertFails(b.collection('owners').doc('alice').get());
  await assertFails(b.collection('owners').doc('alice').set({ data: '{}', rev: 1, schema: 1 }));
  await assertFails(a.collection('other').doc('x').set({ a: 1 }));
  console.log('negative checks finished; add create/update cases with serverTimestamp');
  await env.cleanup();
})();
