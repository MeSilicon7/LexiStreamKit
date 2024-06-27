# LexiStream Class 

The `LexiStream` class facilitates the interaction with a streaming API, handling user inputs, displaying server-sent messages, and managing the UI state accordingly. It's designed to be flexible, allowing customization of various HTML elements and messages.


### Constructor: `LexiStream(config)`

Initializes a new instance of the `LexiStream` class.

**Parameters:**
- `config` (Object): Configuration object containing selectors, endpoints, and optional custom settings.

#### Config Object Properties:
- `box` (string): Selector for the main container where messages will be displayed.
- `sendContent` (string): Selector for the input box where users type their messages.
- `start` (string): Selector for the start button.
- `stop` (string): Selector for the stop button.
- `listen` (string): Endpoint URL to listen to streaming data.
- `sendRequest` (string): Endpoint URL to send user messages.
- `customInputTag` (string, optional): HTML tag for user messages. Defaults to `'div'`.
- `customOutputTag` (string, optional): HTML tag for server messages. Defaults to `'lexi-mark'`.
- `customErrorTag` (string, optional): HTML tag for error messages. Defaults to `'div'`.
- `customLoadingTag` (string, optional): HTML tag for loading messages. Defaults to `'div'`.
- `customLoadingMessage` (string, optional): Message displayed during loading. Defaults to `'Processing...'`.
- `reportConnectionErrorMessage` (string, optional): Error message for connection issues. Defaults to `'Failed to send message. Please try again later. Please check your internet connection.'`.
- `streamingErrorMessage` (string, optional): Error message when the streaming server is not responsive. Defaults to `'Openai server is not responding. Please try again later.'`.

### Methods

#### `attachEventListeners()`
Sets up event listeners for the start and stop buttons, and the input box for submitting on enter key press.

#### `processInput()`
Processes the user input from the input box, sends it to the server, and clears the input box.

#### `startStream()`
Starts the streaming connection to the server, handling incoming data and errors.

#### `displayLoading(show)`
Displays or hides the loading message based on the boolean value `show`.

#### `appendData(data)`
Appends streamed data from the server to the message container in the UI.

#### `stopStream()`
Stops the streaming connection and updates the UI to reflect the inactive state.

#### `sendMessage(message)`
Sends a message to the server and handles the response to start streaming or display an error.

#### `displayMessage({ text, user })`
Displays a message in the UI, specifying whether it's a user or server message.

#### `displayError(text)`
Displays an error message in the UI.

#### `animateText(text, element)`
Animates the typing of text into an HTML element.

#### `updateUI()`
Updates the UI based on the streaming state, enabling or disabling the start and stop buttons.


**LexiStream relies on 'LexiMark' for its UI components, which you can find in the 'src' folder.** LexiMark converts markdown text into HTML using the markdown-it library and adds syntax highlighting with the PrismJS library. To fully utilize LexiStream, you'll need to include these libraries in your project. Additionally, feel free to customize the LexiMark library to meet your specific needs.


