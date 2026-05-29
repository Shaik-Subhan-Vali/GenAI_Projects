from http.server import HTTPServer, SimpleHTTPRequestHandler

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Transit Agent</title>
    <style>
        .message-history { padding: 20px; border: 1px solid #ccc; height: 300px; overflow-y: scroll; margin-bottom: 10px; font-family: sans-serif; }
        .user-message { color: blue; margin-bottom: 10px;}
        .ai-message { color: green; margin-bottom: 10px;}
    </style>
</head>
<body>
    <h2>Mock Agentic UI</h2>
    <div class="message-history" id="history"></div>
    <input type="text" id="chat-input" placeholder="Message the AI..." style="width: 300px; padding: 5px;">
    <button id="send-button">Send</button>

    <script>
        document.getElementById('send-button').addEventListener('click', () => {
            const input = document.getElementById('chat-input').value;
            const history = document.getElementById('history');
            
            // Replaced backticks with safe string concatenation
            history.innerHTML += '<div class="user-message">User: ' + input + '</div>';
            document.getElementById('chat-input').value = '';

            const aiDiv = document.createElement('div');
            aiDiv.className = 'ai-message';
            history.appendChild(aiDiv);

            const responseChunks = ["I have ", "checked the routes ", "from Hyderabad ", "to Amalapuram. ", "What time ", "would you like to depart?"];
            
            let i = 0;
            const streamInterval = setInterval(() => {
                if(i < responseChunks.length) {
                    aiDiv.innerHTML += responseChunks[i];
                    i++;
                } else {
                    clearInterval(streamInterval);
                    aiDiv.classList.add('streaming-done');
                }
            }, 500);
        });
    </script>
</body>
</html>
"""

class MockHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

print("Mock Server running on http://localhost:3000")
HTTPServer(("", 3000), MockHandler).serve_forever()