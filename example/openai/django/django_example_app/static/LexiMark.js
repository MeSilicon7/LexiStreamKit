/*
            
    Silence is golden.
    01001001 01000111 01101111 01110100 01001110 01101111 01110100 01101000 01101001 01101110 01100111 01110100 01101111 01001100 01101111 01110011 01100101
    
    Happy editing!

    
 * LexiMark - A LitElement-based Web Component for Markdown Rendering with Syntax Highlighting Made for LexiStream
 *
 * Author: MeSilicon7
 * Version: 1.0.0-beta.1
 * Repository: https://github.com/MeSilicon7
 * License: MIT
 *
 */


    import { LitElement, html, css } from 'https://cdn.skypack.dev/lit';
    import { unsafeHTML } from 'https://cdn.skypack.dev/lit/directives/unsafe-html.js';
    import markdownIt from 'https://cdn.skypack.dev/markdown-it';
    import Prism from 'https://cdn.skypack.dev/prismjs';
    
    // Include necessary language Support for Prism Syntax Highlighting as needed
    import 'https://cdn.skypack.dev/prismjs/components/prism-javascript.js';
    import 'https://cdn.skypack.dev/prismjs/components/prism-css.js';
    import 'https://cdn.skypack.dev/prismjs/components/prism-markup-templating.js';
    import 'https://cdn.skypack.dev/prismjs/components/prism-python.js';
    import 'https://cdn.skypack.dev/prismjs/components/prism-bash.js';
    import 'https://cdn.skypack.dev/prismjs/components/prism-json.js';
    import 'https://cdn.skypack.dev/prismjs/components/prism-ruby.js';
    
    
    class LexiMark extends LitElement {
        static get styles() {
            return css`
            .code-block-header {
                line-height: 0 !important;
                display: flex !important;
                justify-content: space-between !important;
                background: #2f2f2f !important;
                padding: 6px 14px !important;
                border-radius: 4px 4px 0px 0px !important;
            }
            pre[class*="language-"]{
                margin: 0 !important;
                border: none !important;
                border-radius: 0 0 4px 4px !important;
            }
    
            table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            }
            th, td {
                border-bottom: 1px solid #00000026;
                padding: 8px;
                text-align: left;
                background-color: white;
            }
            th, td {
                border-left: 1px solid #00000026; 
            }
            th:last-child, td:last-child {
                border-right: 1px solid #00000026; 
            }
            th {
                background-color: #0000001a;
                color: black;
                border-top:1px solid #00000026;
            }
            tr:first-child th:first-child {
                border-top-left-radius: 10px;
            }
            tr:first-child th:last-child {
                border-top-right-radius: 10px; 
            }
            tr:last-child td:first-child {
                border-bottom-left-radius: 10px;
            }
            tr:last-child td:last-child {
                border-bottom-right-radius: 10px; 
            }
            `;
        }
    
        static get properties() {
            return {
                markdownContent: { type: String },
                customStyles: { type: String },
                autoscrolloff: { type: Boolean },
                isUserAtBottom: { type: Boolean }
            };
        }
    
        constructor() {
            super();
            this.markdownContent = '';
            this.customStyles = '';
            this.autoscrolloff = false;
            this.isUserAtBottom = true;
            
            this.markdownParser = markdownIt({
                highlight: function (str, lang) {
                    if (lang && Prism.languages[lang]) {
                        try {
                            return `<div class="code-block"><div class="code-block-header"><p>${lang}</p><button class="copy-button">Copy</button></div><pre class="language-${lang}"><code class="language-${lang}">${Prism.highlight(str, Prism.languages[lang], lang)}</code></pre></div>`;
                        } catch (error) {
                            console.error('Error highlighting code:', error);
                            return `<div class="code-block"><div class="code-block-header"><p>${lang}</p><button class="copy-button">Copy</button></div><pre class="language-${lang}"><code class="language-${lang}">${Prism.highlight(str, Prism.languages[lang], lang)}</code></pre></div>`;
                        }
                    }
                    return ''; 
                }
            });
            this.loadSyntaxStylesCSS();
        }
    
            
        copyCodeToClipboard(button) {
            const codeElement = button.closest('.code-block').querySelector('code');
            const codeToCopy = codeElement.textContent; 
            navigator.clipboard.writeText(codeToCopy).then(() => {
                button.textContent = 'Copied!';
                setTimeout(() => button.textContent = 'Copy', 2000);
            }, err => {
                console.error('Failed to copy text: ', err);
            });
        }
    
        updated(changedProperties) {
            super.updated(changedProperties);
            this.attachCopyEventListeners();
        }
        
        attachCopyEventListeners() {
            const buttons = this.shadowRoot.querySelectorAll('.copy-button');
            buttons.forEach(button => {
                button.addEventListener('click', (event) => this.copyCodeToClipboard(event.target));
            });
        }
        
    
    
       
        connectedCallback() {
            super.connectedCallback();
            this.updateMarkdown();
            this.observer = new MutationObserver(() => this.updateMarkdown());
            this.observer.observe(this, {
                characterData: true,
                childList: true,
                subtree: true
            });
    
            window.addEventListener('scroll', () => {
                const windowHeight = window.innerHeight;
                const totalPageHeight = document.body.scrollHeight; 
                const scrollPoint = window.scrollY; 
            
                const scrolledFromTop = windowHeight + scrollPoint;
                const threshold = 25; // Distance from the bottom to consider "at the bottom"
    
                this.isUserAtBottom = scrolledFromTop >= totalPageHeight - threshold;
                
                // console.log('Window Height:', windowHeight);
                // console.log('Total Page Height:', totalPageHeight);
                // console.log('Scroll Point:', scrollPoint);
                // console.log('Scrolled from Top:', scrolledFromTop);
                // console.log('Is User At Bottom:', this.isUserAtBottom);
            });
            
        }
    
        disconnectedCallback() {
            super.disconnectedCallback();
            this.observer.disconnect();
        }
    
        updateMarkdown() {
            let content = this.textContent;
            content = content.replace(/<br>(\s*#{1,6} )/g, '\n$1');
            content = content.replace(/<br\s*\/?>/g, '\n');
            this.markdownContent = content;
    
            if (!this.autoscrolloff && this.isUserAtBottom) {
                window.scrollTo(0, document.body.scrollHeight);
            }
        }
    
        async loadSyntaxStylesCSS() {
            try {
                const response = await fetch('https://cdn.jsdelivr.net/npm/prismjs/themes/prism-twilight.css');
                if (!response.ok) {
                    throw new Error('Failed to load Twilight theme styles.');
                }
                this.customStyles = await response.text();
            } catch (error) {
                console.error('Error loading Twilight theme styles:', error);
                this.customStyles = ''; 
            }
        }
    
    
         render() {
            const htmlContent = this.markdownParser.render(this.markdownContent);
            return html`
                <style>${this.customStyles}</style>
                ${unsafeHTML(htmlContent)}
            `;
        }
        
    }
    
    customElements.define('lexi-mark', LexiMark);
    
    