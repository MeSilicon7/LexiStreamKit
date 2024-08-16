**Important Bug Fix Require:**
1. When the stop button is used to stop streaming, the data is not being saved.

**Optimization Required for Frontend:**

1. **Asynchronous Chat Loading:**  
   - Initially, load the first 10 chat messages asynchronously.
   - When the user scrolls down, load the next 10 messages one by one as needed.

2. **Asynchronous Thread Loading:**
   - Start by loading the first 10 threads asynchronously.
   - As the user scrolls, load additional threads in batches of 10.



Resources
HTMX: https://htmx.org/