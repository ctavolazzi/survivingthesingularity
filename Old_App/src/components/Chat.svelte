<script>
    import { onDestroy } from 'svelte';
    import { useChat } from 'ai/svelte';
  
    const { input, handleSubmit, messages } = useChat();
  
    let chatMessages = [];
    let streamingMessage = '';
  
    const unsubscribe = messages.subscribe((value) => {
      if (value.length > chatMessages.length) {
        const lastMessage = value[value.length - 1];
        if (lastMessage.role === 'assistant') {
          streamingMessage += lastMessage.content;
        } else {
          chatMessages = [...chatMessages, lastMessage];
          streamingMessage = '';
        }
      }
    });
  
    onDestroy(unsubscribe);
  </script>
  
  <svelte:head>
    <title>Chat</title>
    <meta name="description" content="AI-powered chat using SvelteKit" />
  </svelte:head>
  
  <section>
    <h1>Chat with AI</h1>
    <ul>
      {#each chatMessages as message}
        <li>{message.role}: {message.content}</li>
      {/each}
      {#if streamingMessage}
        <li>assistant: {streamingMessage}</li>
      {/if}
    </ul>
    <form on:submit|preventDefault={handleSubmit}>
      <input bind:value={$input} placeholder="Type your message..." />
      <button type="submit">Send</button>
    </form>
  </section>
  
  <style>
    section {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      flex: 0.6;
    }
  
    h1 {
      width: 100%;
    }
  
    ul {
      list-style-type: none;
      padding: 0;
    }
  
    li {
      margin-bottom: 10px;
    }
  
    form {
      display: flex;
      margin-top: 20px;
    }
  
    input {
      flex: 1;
      padding: 5px;
    }
  
    button {
      margin-left: 10px;
      padding: 5px 10px;
    }
  </style>