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
        <!-- <li class:selected={activeTab === 'News'} on:click={() => setActiveTab('News')}>News</li> -->
        <!-- <li class:selected={activeTab === 'Chat'} on:click={() => setActiveTab('Chat')}>Chat</li> -->
        <li class:selected={activeTab === 'About'} on:click={() => setActiveTab('About')}>About</li>
        <li class:selected={activeTab === 'Contact'} on:click={() => setActiveTab('Contact')}>Contact</li>
    </ul>
</nav>

<style>
    nav {
        background-color: #ffffff;
        padding: 10px;
    }

    ul {
        list-style-type: none;
        display: flex;
        justify-content: space-between;
    }

    li {
        padding: 5px;
        cursor: pointer;
    }

    .selected {
        font-weight: bold;
    }
</style>

