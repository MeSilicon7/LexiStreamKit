
<p align="center">
  <a href="https://lexistreamkit.mesilicon7.com" target="_blank" rel="noopener noreferrer">
    <img src="assets/Logo.svg" alt="LexiStream logo" width="600"> 
  </a>
</p>


<h3 align="center">Copy, Paste, Edit & Deploy</h3>
<p align="center">
    <a href="https://lexistreamkit.mesilicon7.com" target="_blank">
        <img alt="Static Badge" src="https://img.shields.io/badge/Product-F04438"></a>
    <a href="https://twitter.com/intent/follow?screen_name=mesilicon7" target="_blank">
        <img src="https://img.shields.io/twitter/follow/mesilicon7?logo=X&color=%20%23f5f5f5"
            alt="follow on Twitter"></a>
    <a href="https://github.com/MeSilicon7/LexiStreamKit/graphs/commit-activity" target="_blank">
        <img alt="Commits last month" src="https://img.shields.io/github/commit-activity/m/MeSilicon7/LexiStreamKit?labelColor=%20%2332b583&color=%20%2312b76a"></a>
    <a href="https://github.com/MeSilicon7/LexiStreamKit/" target="_blank">
        <img alt="Issues closed" src="https://img.shields.io/github/issues-search?query=repo%3AMeSilicon7%2FLexiStreamKit%20is%3Aclosed&label=issues%20closed&labelColor=%20%237d89b0&color=%20%235d6b98"></a>
    <a href="https://github.com/MeSilicon7/LexiStreamKit/discussions/" target="_blank">
        <img alt="Discussion posts" src="https://img.shields.io/github/discussions/MeSilicon7/LexiStreamKit?labelColor=%20%239b8afb&color=%20%237a5af8"></a>
</p>

<!-- <p align="center">
  <a href="./README.md"><img alt="README in English" src="https://img.shields.io/badge/English-blue?style=flat-square&logo=github"></a>
  <a href="./README_CN.md"><img alt="简体中文版自述文件" src="https://img.shields.io/badge/简体中文-red?style=flat-square&logo=github"></a>
  <a href="./README_JP.md"><img alt="日本語のREADME" src="https://img.shields.io/badge/日本語-purple?style=flat-square&logo=github"></a>
  <a href="./README_ES.md"><img alt="README en Español" src="https://img.shields.io/badge/Español-yellow?style=flat-square&logo=github"></a>
  <a href="./README_FR.md"><img alt="README en Français" src="https://img.shields.io/badge/Français-green?style=flat-square&logo=github"></a>
  <a href="./README_MS.md"><img alt="README in Malay" src="https://img.shields.io/badge/Malay-orange?style=flat-square&logo=github"></a>
  <a href="./README_TR.md"><img alt="README in Korean" src="https://img.shields.io/badge/한국어-pink?style=flat-square&logo=github"></a>
  <a href="./README_AR.md"><img alt="README بالعربية" src="https://img.shields.io/badge/العربية-lightgrey?style=flat-square&logo=github"></a>
  <a href="./README_RU.md"><img alt="README in Russian" src="https://img.shields.io/badge/Русский-cyan?style=flat-square&logo=github"></a>
  <a href="./README_KO.md"><img alt="README in Korean" src="https://img.shields.io/badge/한국어-pink?style=flat-square&logo=github"></a>
  <a href="./README_IT.md"><img alt="README in Italian" src="https://img.shields.io/badge/Italian-blue?style=flat-square&logo=github"></a>
  <a href="./README_DE.md"><img alt="README in German" src="https://img.shields.io/badge/German-green?style=flat-square&logo=github"></a>
  <a href="./README_PT.md"><img alt="README in Portuguese" src="https://img.shields.io/badge/Portuguese-yellow?style=flat-square&logo=github"></a>
  <a href="./README_VI.md"><img alt="README in Vietnamese" src="https://img.shields.io/badge/Vietnamese-orange?style=flat-square&logo=github"></a>
  <a href="./README_BN.md"><img alt="README in Bengali" src="https://img.shields.io/badge/Bengali-cyan?style=flat-square&logo=github"></a>
  <a href="./README_ID.md"><img alt="README in Indonesian" src="https://img.shields.io/badge/Indonesian-yellow?style=flat-square&logo=github"></a>
  <a href="./README_TH.md"><img alt="README in Thai" src="https://img.shields.io/badge/Thai-lightgrey?style=flat-square&logo=github"></a>
</p> -->


# LexiStream - A simple code snippet for rendering markdown in real-time built for OpenAi GPT

Hello there! Thank you for stopping by. I’m thrilled to share this project with you and I’m eager to make it better with your help. Whether you’re here to use the project, report a bug, or contribute, your input is highly appreciated.

This guide introduces LexiStream, a library designed to streamline the creation of a chatbot interface that interacts seamlessly with OpenAI's GPT API. Ideal for developers looking to integrate advanced conversational capabilities without being tied to a specific backend architecture.

## Features

- Real-time streaming of chat responses.
- Customizable UI components.
- Easy integration with any web application.
- No complex build tools required.

https://github.com/MeSilicon7/LexiStreamKit/blob/main/assets/Github-intro.mp4

## Table of contents

- [Installation & Usage](#installation--usage)
- [Configuration Options](#configuration-options)
- [Methods](#methods)
- [Styling](#styling)
- [Language Syntax Highlighting](#language-syntax-highlighting)
- [Future Roadmap](#future-roadmap)
- [License](#license)



## Installation & Usage

Include the LexiStream.js script in your project:

> [!NOTE]
> Short Tutorial [LexiStream Kit Tutorial](https://lexistreamkit.mesilicon7.com).Here example projects [LexiStream Example](https://lexistreamkit.mesilicon7.com) 

> [!IMPORTANT]
> Your backend needs to support Server-Sent Events (SSE) to stream data to the client effectively. **Replace every newline character ('\n') with ' \<br\> ' since '\n' does not behave as expected in SSE; it seems to disappear.** Additionally, you should conclude your streaming with 'data: finish_reason: stop\n\n' to ensure the client side recognizes that the stream has ended. Without this specific message, LexiStream will continue to wait for more data and won't close the stream.


```html
<script type='module' src="path/to/LexiMark.js"></script>
<script src="path/to/LexiStream.js"></script>
```

Setup your HTML:

```html
<div id="chat-box">
    <input type="text" id="input-box" placeholder="Type your message here...">
    <button id="start-button">Start</button>
    <button id="stop-button" disabled>Stop</button>
</div>
```

Initialize LexiStream in your JavaScript file:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const config = {
        box: '#chat-box',
        sendContent: '#input-box',
        start: '#start-button',
        stop: '#stop-button',
        sendRequest: '/send',
        listen: '/stream'
    };

    const chatInterface = new LexiStream(config);
});
```



## Configuration Options

- `box`: Selector for the chat box container.
- `sendContent`: Selector for the input box.
- `start`: Selector for the start button.
- `stop`: Selector for the stop button.
- `sendRequest`: URL for sending messages.
- `listen`: URL for receiving streamed messages.

## Methods

- `startStream()`: Starts the message stream.
- `stopStream()`: Stops the message stream.
- `sendMessage(message)`: Sends a message to the server.


## Styling

You can use custom tag or class names to style the chat interface. The default tags are `div` for user messages and `lexi-mark` for server messages. You can customize these tags in the LexiStream configuration object.

```javascript
const config = {
  customInputTag: 'input',
  customOutputTag: 'output',
  customErrorTag: 'error',
  customLoadingTag: 'loading'
};

const chatInterface = new LexiStream(config);
```

See advanced usage for more customization options. [Link](#advance)

## Language Syntax Highlighting

LexiStream uses the LexiMark library for rendering markdown text and syntax highlighting. You can customize the syntax highlighting theme by including the desired PrismJS theme in your project. The default theme is `prism-twilight.css`. Read LexiMark documentation for more details. 
[LexiMark](docs/LexiMark/README-LexiMark.md)

## Future Roadmap ::

- [ ] Task 1: Make a full example with a backend.
- [ ] Task 2: Add a bar for the user to select the model, TTS, and STT etc.

## Advance

LexiStream is highly customizable and can be configured to fit your specific needs. [LexiStream](docs/LexiStream/README.md)


**Contributors**

<a href="https://github.com/MeSilicon7/LexiStreamKit/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MeSilicon7/LexiStreamKit" />
</a>

## Community & contact

* [Github Discussion](https://github.com/MeSilicon7/LexiStreamKit/discussions). Best for: sharing feedback and asking questions.
* [GitHub Issues](https://github.com/MeSilicon7/LexiStreamKit/issues).
* [Twitter](https://twitter.com/mesilicon7).


<!-- ## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=MeSilicon7/LexiStreamKit&type=Date)](https://star-history.com/#MeSilicon7/LexiStreamKit&Date) -->


## License

No license restrictions, but attribution is appreciated.
