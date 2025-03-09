<!-- src/routes/profile/[username]/+page.svelte -->
<script lang="ts">
    export let data;
    const { profile } = data;
  </script>
  
  <div class="profile-container">
    <h1>{profile.full_name}</h1>
    <p>@{profile.username}</p>
    {#if profile.avatar_url}
      <img src={profile.avatar_url} alt="Profile avatar"  loading="lazy" \/\>
    {/if}
    <p>{profile.bio}</p>
    <p>Location: {profile.location}</p>
    <a href={profile.website} target="_blank" rel="noopener noreferrer">Website</a>
    {#if profile.social_links.twitter}
      <a href="https://twitter.com/{profile.social_links.twitter}" target="_blank">Twitter</a>
    {/if}
    {#if profile.social_links.github}
      <a href="https://github.com/{profile.social_links.github}" target="_blank">GitHub</a>
    {/if}
  </div>