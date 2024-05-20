<script>
  export let activeTab;
  export let setActiveTab;

  const tabs = ['Home', 'About', 'Contact'];
</script>

<nav>
  <ul>
    {#each tabs as tab}
      <li class:selected={activeTab === tab}>
        <button
          class:selected={activeTab === tab}
          tabindex="0"
          on:click={() => setActiveTab(tab)}
          on:keydown={(e) => e.key === 'Enter' && setActiveTab(tab)}
        >{tab}</button>
      </li>
    {/each}
  </ul>
</nav>

<style>
nav {
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

ul {
  list-style-type: none;
  display: flex;
  justify-content: space-around;
  margin: 0;
  padding: 0;
}

li {
  margin: 0;
}

button {
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1.2rem;
  border: none;
  background: none;
  border-radius: 5px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

button:hover {
  background-color: #f0f0f0;
  color: #333;
}

.selected {
  background-color: #333;
  color: #ffffff;
  transition: background-color 0.2s ease, color 0.2s ease;
  font-weight: bold;
}
</style>
