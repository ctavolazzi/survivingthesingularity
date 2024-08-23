<!-- src/routes/account/+page.svelte -->
<script lang="ts">
  // ... existing imports and logic ...
  
  let bio: string = profile?.bio ?? ''
  let location: string = profile?.location ?? ''
  let socialLinks = profile?.social_links ?? {}
</script>

<div class="form-widget">
  <form method="post" action="?/update" use:enhance={handleSubmit}>
    <!-- ... existing fields ... -->
    
    <div>
      <label for="bio">Bio</label>
      <textarea id="bio" name="bio" rows="4">{bio}</textarea>
    </div>

    <div>
      <label for="location">Location</label>
      <input id="location" name="location" type="text" value={location} />
    </div>

    <div>
      <label for="twitter">Twitter</label>
      <input id="twitter" name="twitter" type="text" value={socialLinks.twitter ?? ''} />
    </div>

    <div>
      <label for="github">GitHub</label>
      <input id="github" name="github" type="text" value={socialLinks.github ?? ''} />
    </div>

    <!-- ... submit button ... -->
  </form>
</div>