# 🌐 GEEDI.ORG Integration Guide

## Integrating Somaliland Legal AI with geedi.org

This guide explains how to integrate the Somaliland Legal AI backend with your GEDI Law and Consultancy Firm website (geedi.org).

## 🎯 Integration Options

### Option 1: Frontend Widget (Recommended for geedi.org)

Add an AI-powered chat widget to your website that connects to your deployed backend API.

#### Step 1: Deploy Backend API

Deploy your backend to a hosting service (Render/Railway/Heroku):

```bash
# Using Render (recommended)
1. Fork this repository
2. Go to https://dashboard.render.com
3. Click "New +" → "Web Service"
4. Connect GitHub and select this repo
5. Configure:
   - Name: somaliland-legal-ai
   - Environment: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn server:app
   - Add Environment Variables:
     * GROQ_API_KEY=your_groq_key
     * HUGGINGFACE_API_KEY=your_hf_key (optional)
6. Click "Create Web Service"
```

You'll get a URL like: `https://somaliland-legal-ai.onrender.com`

#### Step 2: Add Chat Widget to geedi.org

Create a file `legal-ai-widget.html` and add this code:

```html
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GEDI Legal AI Assistant</title>
    <style>
        .ai-chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .ai-chat-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s;
        }
        
        .ai-chat-button:hover {
            transform: scale(1.1);
        }
        
        .ai-chat-button svg {
            width: 30px;
            height: 30px;
            fill: white;
        }
        
        .ai-chat-window {
            display: none;
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 380px;
            height: 550px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3);
            flex-direction: column;
            overflow: hidden;
        }
        
        .ai-chat-window.active {
            display: flex;
        }
        
        .ai-chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            font-weight: bold;
            font-size: 18px;
        }
        
        .ai-chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f5f5f5;
        }
        
        .ai-message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .ai-message.user {
            background: #667eea;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }
        
        .ai-message.bot {
            background: white;
            color: #333;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .ai-chat-input {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #eee;
        }
        
        .ai-chat-input input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }
        
        .ai-chat-input button {
            margin-left: 10px;
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .ai-chat-input button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .ai-loading {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        
        .ai-disclaimer {
            font-size: 11px;
            color: #888;
            margin-top: 10px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="ai-chat-widget">
        <button class="ai-chat-button" id="aiChatToggle" aria-label="Legal AI Assistant">
            <svg viewBox="0 0 24 24">
                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
            </svg>
        </button>
        
        <div class="ai-chat-window" id="aiChatWindow">
            <div class="ai-chat-header">
                🏛️ GEDI Legal AI Assistant
            </div>
            <div class="ai-chat-messages" id="aiChatMessages">
                <div class="ai-message bot">
                    Salaan! Waxaan ahay Kaaliye Sharci oo AI ah. Waad igu weydiin kartaa su'aalaha ku saabsan sharciga Somaliland. Sidee kaa caawin karaa maanta?
                    <div class="ai-disclaimer">⚠️ Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah.</div>
                </div>
            </div>
            <div class="ai-chat-input">
                <input 
                    type="text" 
                    id="aiChatInput" 
                    placeholder="Su'aashaada halkan qor..."
                    maxlength="2000"
                />
                <button id="aiChatSend">Dir</button>
            </div>
        </div>
    </div>

    <script>
        const API_URL = 'https://somaliland-legal-ai.onrender.com/ask'; // Replace with your deployed URL
        
        const chatToggle = document.getElementById('aiChatToggle');
        const chatWindow = document.getElementById('aiChatWindow');
        const chatMessages = document.getElementById('aiChatMessages');
        const chatInput = document.getElementById('aiChatInput');
        const chatSend = document.getElementById('aiChatSend');
        
        let isLoading = false;
        
        chatToggle.addEventListener('click', () => {
            chatWindow.classList.toggle('active');
            if (chatWindow.classList.contains('active')) {
                chatInput.focus();
            }
        });
        
        async function sendMessage() {
            const question = chatInput.value.trim();
            if (!question || isLoading) return;
            
            // Add user message
            addMessage(question, 'user');
            chatInput.value = '';
            
            // Show loading
            isLoading = true;
            chatSend.disabled = true;
            const loadingMsg = addMessage('<span class="ai-loading"></span> Waa la eegayaa...', 'bot');
            
            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ question })
                });
                
                const data = await response.json();
                
                // Remove loading message
                loadingMsg.remove();
                
                if (response.ok) {
                    const answer = data.answer + 
                        `<div class="ai-disclaimer">⚠️ ${data.disclaimer}</div>` +
                        `<div class="ai-disclaimer">🤖 Model: ${data.model || 'AI'} | ⚡ ${data.response_time_ms || 0}ms</div>`;
                    addMessage(answer, 'bot');
                } else {
                    addMessage(`❌ Cilad: ${data.error || 'Fadlan isku day mar kale'}`, 'bot');
                }
            } catch (error) {
                loadingMsg.remove();
                addMessage('❌ Lama xiriiri karin server-ka. Fadlan isku day mar kale.', 'bot');
            } finally {
                isLoading = false;
                chatSend.disabled = false;
            }
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `ai-message ${sender}`;
            messageDiv.innerHTML = text;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            return messageDiv;
        }
        
        chatSend.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

#### Step 3: Add Widget to Your Website

**For InfinityFree Hosting (geedi.org):**

1. Log in to [InfinityFree Dashboard](https://dash.infinityfree.com/accounts/if0_40914676/domains/geedi.org)
2. Click "File Manager" or use FTP
3. Upload `legal-ai-widget.html` to your website directory
4. In your main website pages, add this before closing `</body>` tag:

```html
<!-- GEDI Legal AI Chat Widget -->
<script src="legal-ai-widget.html" async></script>
<!-- Or include as iframe: -->
<iframe src="legal-ai-widget.html" style="position:fixed;bottom:0;right:0;width:100%;height:100%;border:none;z-index:9999;" id="legal-ai-iframe" frameborder="0"></iframe>
<script>
    // Auto-hide iframe, show only widget button
    document.getElementById('legal-ai-iframe').style.height = '100px';
</script>
```

### Option 2: WordPress Plugin Integration

If using WordPress (which you already have fix-wpcode-snippet.php for):

1. Install the widget code via WPCode plugin
2. Add the HTML/JS code to a Custom HTML widget
3. Place it in your sidebar or footer

## 🔧 Configuration

### Update API URL

In the widget code, replace:
```javascript
const API_URL = 'https://somaliland-legal-ai.onrender.com/ask';
```

With your actual deployed backend URL.

### Customize Appearance

Modify the CSS colors to match your geedi.org branding:
- Primary: `#667eea` → Your blue (#1e3a8a from geedi.org)
- Secondary: `#764ba2` → Your accent color

## 📊 Monitoring

Check your API performance:
```bash
curl https://your-api.onrender.com/health
curl https://your-api.onrender.com/stats
```

## 🚀 Going Live Checklist

- [ ] Backend deployed and tested
- [ ] API URL updated in widget code
- [ ] Widget uploaded to geedi.org
- [ ] Widget tested on desktop and mobile
- [ ] Colors customized to match brand
- [ ] Error handling tested
- [ ] Somali text displays correctly
- [ ] Response times acceptable (<3s)

## 🆘 Troubleshooting

**Widget doesn't appear:**
- Check browser console for errors
- Verify API URL is correct
- Check CORS is enabled (already done in server.py)

**API errors:**
- Verify GROQ_API_KEY or HUGGINGFACE_API_KEY is set
- Check backend logs in Render/Railway
- Test `/health` endpoint

**Slow responses:**
- First request may be slow (cold start)
- Use caching features (already implemented)
- Consider upgrading hosting plan

## 📞 Support

For issues with integration, check:
- [Repository Issues](https://github.com/GEEDDIGA/somaliland-legal-ai/issues)
- Backend logs in your hosting platform
- Browser developer console

---

**Made with ❤️ for GEDI Law and Consultancy Firm**  
**Waxaa loo sameeyay GEDI Law - geedi.org** 🇸🇴
