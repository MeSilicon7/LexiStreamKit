## Overview
`LexiMark` is a LitElement-based web component for rendering Markdown content with syntax highlighting. It utilizes `markdown-it` for Markdown parsing and `PrismJS` for syntax highlighting.

### Methods

#### Constructor
- **Purpose**: Initializes default properties, sets up the Markdown parser, and loads syntax styles.
- **Customization**: You can modify the default properties or add additional configurations to the Markdown parser here.

#### `copyCodeToClipboard(button)`
- **Purpose**: Copies the content of a code block to the clipboard when the copy button is clicked.
- **Customization**: If you want to modify the copy functionality or add notifications, modify this method.

#### `updated(changedProperties)`
- **Purpose**: Called after the element updates. It attaches event listeners to copy buttons.
- **Customization**: To change how updates are handled or to add more operations post-update, modify this method.

#### `attachCopyEventListeners()`
- **Purpose**: Adds click event listeners to all copy buttons.
- **Customization**: You can add more events or modify the current event handling process here.

#### `connectedCallback()`
- **Purpose**: Performs operations when the element is added to the document. It starts the Markdown content update process and sets up an observer to monitor changes.
- **Customization**: Additional event listeners or initial setup operations can be added here.

#### `disconnectedCallback()`
- **Purpose**: Cleans up by disconnecting the observer when the element is removed from the document.
- **Customization**: Additional cleanup operations can be added here.

#### `updateMarkdown()`
- **Purpose**: Updates the internal Markdown content state of the component whenever the element's content changes.
- **Customization**: Modify how content is processed or update the conditions under which the Markdown content is refreshed.

#### `loadSyntaxStylesCSS()`
- **Purpose**: Loads external CSS for syntax highlighting styles.
- **Customization**: You can change the CSS file's URL, handle different themes, or manage error handling differently.

### Event Listeners

- **Window Scroll Listener**: Monitors whether the user is at the bottom of the page to manage automatic scrolling.
- **Customization**: Adjust the scrolling threshold or modify how scrolling behavior is determined.

### Properties

- `markdownContent`: Stores the processed Markdown content.
- `customStyles`: Contains custom styles for syntax highlighting.
- `autoscrolloff`: Flag to control automatic scrolling.
- `isUserAtBottom`: Indicates whether the user is at the bottom of the page.

### Render Method
- **Purpose**: Renders the transformed Markdown content along with syntax highlighting into the DOM.
- **Customization**: You can modify how content is rendered or add additional HTML elements and styles.

### How to Customize
1. **Changing Styles**: Modify the `css` template literal in the `styles` getter.
2. **Adding Syntax Support**: Include more PrismJS components in the document load listener.
3. **Adjusting Markdown Parsing**: Change the configuration in the `markdownParser` initialization within the constructor.
4. **Enhancing Functionality**: Add new properties or methods to extend the component's functionality.

### Repository and Licensing
- **Repository**: Hosted on GitHub, where you can fork or contribute.
- **License**: No license restrictions, but attribution is appreciated.

This documentation provides a comprehensive guide to understanding and customizing the `LexiMark` component for different needs.