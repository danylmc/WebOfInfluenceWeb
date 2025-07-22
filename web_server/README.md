# Getting a temp URL
## Setup
- Run run.py
- Run database_api.py
- brew install ngrok
- ngrok config add-authtoken 2y2PcL2Xmq5exZo3yupTfLNkIam_3SRJx4ThhzMnXPgrXeE99
- cd demo-cand
- npm run dev
- ngrok http 5173 (tunnel localhost to ngrok)

this should show the temp URL to access the WebOfInfluence web page

Note:
- kill any active ports so that 5173 can be used
- npx kill-port 5173

