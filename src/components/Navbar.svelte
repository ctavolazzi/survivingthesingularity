<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let activeTab = 'Home';

    function setActiveTab(tab) {
      activeTab = tab;
      console.log(activeTab);
      dispatch('tabChange', { tab });
    }

    console.log(activeTab);
  </script>

  <nav>
    <ul>
      <li class:selected={activeTab === 'Home'} on:click={() => setActiveTab('Home')}>Home</li>
      <li class:selected={activeTab === 'About'} on:click={() => setActiveTab('About')}>About</li>
      <li class:selected={activeTab === 'Contact'} on:click={() => setActiveTab('Contact')}>Contact</li>
    </ul>
  </nav>

  <style>
    nav {
      background-color: #ffffff;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Adding subtle shadow for better separation */
    }

    ul {
      list-style-type: none;
      display: flex;
      justify-content: space-around; /* Space out the items equally */
      margin: 0;
      padding: 0;
    }

    li {
      padding: 10px 20px; /* Larger padding for bigger buttons */
      cursor: pointer;
      font-size: 1.2rem; /* Increase font size */
      border-radius: 5px; /* Rounded corners */
      transition: background-color 0.2s ease, color 0.2s ease; /* Smooth transition */
    }

    li:hover {
      background-color: #f0f0f0; /* Light background on hover */
      color: #333; /* Darker text color on hover */
    }

    .selected {
      background-color: #333; /* Dark background for the selected tab */
      color: #ffffff; /* White text color for the selected tab */
      transition: background-color 0.2s ease, color 0.2s ease; /* Smooth transition */
    }
  </style>
