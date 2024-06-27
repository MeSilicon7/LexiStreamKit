/*
            
    Silence is golden.
    01001001 01000111 01101111 01110100 01001110 01101111 01110100 01101000 01101001 01101110 01100111 01110100 01101111 01001100 01101111 01110011 01100101
    
    Happy editing!

    
 * LexiStream - Easily Create a Chatbot Interface with OpenAI's GPT API
 *
 * Author: MeSilicon7
 * Version: 1.0.0-beta
 * Repository: https://github.com/MeSilicon7
 * License: No License
 *
 */

    class LexiStream {
        constructor(config) {
            this.config = config;
            this.box = document.querySelector(config.box);
            this.inputBox = document.querySelector(config.sendContent);
            this.startButton = document.querySelector(config.start);
            this.stopButton = document.querySelector(config.stop);
            this.customInputTag = config.customInputTag || 'div'; 
            this.customOutputTag = config.customOutputTag || 'lexi-mark'; 
            this.customErrorTag = config.customErrorTag || 'div'; 
            this.customLoadingTag = config.customLoadingTag || 'div'; 
            this.customLoadingMessage = config.customLoadingMessage || 'Processing...';
            this.eventSource = null;
            this.messageContainer = null;
            this.reportConnectionErrorMessage = config.reportConnectionErrorMessage || 'Failed to send message. Please try again later. Please check your internet connection.'; 
            this.streamingErrorMessage = config.streamingErrorMessage || 'Openai server is not responding. Please try again later.';  
    
            this.attachEventListeners();
        }
    
        attachEventListeners() {
            this.startButton.addEventListener('click', () => this.processInput());
            this.inputBox.addEventListener('keypress', e => {
                if (e.key === 'Enter') {
                    if (this.eventSource) {
                        e.preventDefault();
                    } else {
                        e.preventDefault();  
                        this.processInput();
                    }
                }
            });
            this.stopButton.addEventListener('click', () => this.stopStream());
        }
        
    
        processInput() {
            const message = this.inputBox.value.trim();
            if (message) {
                this.sendMessage(message);
                this.inputBox.value = '';
            }
        }
    
        startStream() {
            if (this.eventSource) {
                console.log('Stream is already active.');
                return;
            }
        
            this.displayLoading(true);
        
            this.eventSource = new EventSource(this.config.listen);
        
            this.eventSource.onmessage = event => {
                this.displayLoading(false);
                if (event.data.includes('finish_reason: stop')) {
                    this.stopStream();
                } else {
                    this.appendData(event.data);
                }
            };
        
            this.eventSource.onerror = () => {
                console.error('EventSource failed');
                this.displayError(this.streamingErrorMessage); 
                this.stopStream();
            };
        
            this.updateUI();
        }
    
        displayLoading(show) {
            
            if (!this.loadingElement) {
                this.loadingElement = document.createElement(this.customLoadingTag);
                this.loadingElement.classList.add('loading');
                this.loadingElement.innerHTML = this.customLoadingMessage;
                this.box.appendChild(this.loadingElement); 
            }
    
            // fix loading element not showing up after last message
            if (this.loadingElement) {
                this.loadingElement.remove();
                this.loadingElement = document.createElement(this.customLoadingTag);
                this.loadingElement.classList.add('loading');
                this.loadingElement.innerHTML = this.customLoadingMessage;
                this.box.appendChild(this.loadingElement);
            }
        
            this.loadingElement.style.display = show ? 'block' : 'none';
        }
        
        
    
    
        appendData(data) {
            if (!this.messageContainer) {
                this.messageContainer = document.createElement(this.customOutputTag);
                this.messageContainer.classList.add('assistant-message');
                this.box.appendChild(this.messageContainer);
            }
            this.messageContainer.textContent += data;
        }
        
        stopStream() {
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
                this.messageContainer = null;
            }
            this.updateUI();
            this.displayLoading(false); 
        }
    
        sendMessage(message) {
            fetch(this.config.sendRequest, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.displayMessage({ text: message, user: true });
                    this.startStream();
                } else {
                    console.error('Message was not processed successfully:', data);
                }
            })
            .catch(error => {
                this.displayError(this.reportConnectionErrorMessage);
                console.error('Error sending message:', error);
            });
        }
    
        displayMessage({ text, user }) {
            const messageElement = document.createElement(this.customInputTag);
            messageElement.classList.add(user ? 'user-message' : 'assistant-message');
            this.box.appendChild(messageElement);
            this.animateText(text, messageElement);
        }
    
        displayError(text) {
            const messageElement = document.createElement(this.customErrorTag);
            messageElement.classList.add('error');
            messageElement.innerHTML = text;
            this.box.appendChild(messageElement);
        }
    
        animateText(text, element) {
            let i = 0;
            const speed = 10;
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            };
            typeWriter();
        }
    
        updateUI() {
            const isActive = !!this.eventSource;  
            this.startButton.disabled = isActive; 
            this.stopButton.disabled = !isActive;
        }
    }
    