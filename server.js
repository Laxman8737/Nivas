// Online payments are DISABLED. The earlier Razorpay server trusted amounts sent by the browser
// and let any signed-in user read any bill by id, so it must not be deployed.
// Nivas works without any server: owners record Cash/UPI payments themselves, and receipts are labelled
// "recorded by owner", never "verified by a payment gateway".
require('http').createServer((q,r)=>{r.writeHead(q.url==='/health'?200:503,{'content-type':'application/json'});r.end(JSON.stringify(q.url==='/health'?{ok:true}:{error:'Online payments are disabled'}))}).listen(process.env.PORT||3000);
