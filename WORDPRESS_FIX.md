# WordPress JavaScript Fix for Somaliland Legal AI Chatbot

## Problem
The chatbot is displaying "undefined" when receiving API responses because the JavaScript code doesn't safely check if the `data` object exists before accessing its properties.

## Location
WordPress Admin → Code Snippets → "Somaliland Legal AI Chatbot - Fixed" (ID: 449)

## Current Code (Line 86 - BROKEN):
```javascript
const botAnswer = data.answer || data.message || 'Maleesh, wax waaye';
```

## Fixed Code (Line 86-87):
```javascript
const botAnswer = (data && data.answer) ? data.answer : (data && data.error) ? data.error : 'Cilad ayaa dhacday';
```

## What Changed:
1. Added null-safe checking: `(data && data.answer)` checks if `data` exists BEFORE accessing `.answer`
2. Added proper error handling: Falls back to `data.error` if available
3. Changed default message to proper Somali: 'Cilad ayaa dhacday' (An error occurred)

## How to Apply:
1. Go to WordPress Admin: https://www.geedi.org/wp-admin/
2. Navigate to Code Snippets → Edit snippet ID 449
3. Find line 86 (search for `const botAnswer =`)
4. Replace the entire line with the fixed code above
5. Click "Update" to save

## Testing:
1. Open https://www.geedi.org/
2. Click the green chatbot button (⚖️)
3. Ask a question in Somali
4. The bot should now display proper responses instead of "undefined"

## Why This Fix Works:
The API returns `{"answer": "..."}` or `{"error": "..."}`. The old code tried to access `data.answer` without checking if `data` exists first. When `data` is undefined or null, JavaScript throws an error and the chatbot shows "undefined". The new code uses ternary operators with AND checks to safely navigate the object.
