<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { supabase } from '$lib/utils/supabaseClient';
  
    export let size = 10;
    export let url: string | null = null;
  
    let avatarUrl: string | null = null;
    let uploading = false;
    let files: FileList;
  
    const dispatch = createEventDispatcher();
  
    $: if (url) downloadImage(url);
  
    async function downloadImage(path: string) {
      try {
        const { data, error } = await supabase.storage.from('avatars').download(path);
        if (error) throw error;
        avatarUrl = URL.createObjectURL(data);
      } catch (error) {
        if (error instanceof Error) console.error('Error downloading image: ', error.message);
      }
    }
  
    async function uploadAvatar() {
      try {
        uploading = true;
  
        if (!files || files.length === 0) {
          throw new Error('You must select an image to upload.');
        }
  
        const file = files[0];
        const fileExt = file.name.split('.').pop();
        const filePath = `${Math.random()}.${fileExt}`;
  
        const { error: uploadError } = await supabase.storage
          .from('avatars')
          .upload(filePath, file);
  
        if (uploadError) {
          throw uploadError;
        }
  
        url = filePath;
        dispatch('upload');
      } catch (error) {
        if (error instanceof Error) alert(error.message);
      } finally {
        uploading = false;
      }
    }
  </script>
  
  <div>
    {#if avatarUrl}
      <img
        src={avatarUrl}
        alt="Avatar"
        class="avatar image"
        style="width: {size}em; height: {size}em;"
      />
    {:else}
      <div class="avatar no-image" style="width: {size}em; height: {size}em;" />
    {/if}
  
    <div style="width: {size}em;">
      <label class="button primary block" for="single">
        {uploading ? 'Uploading ...' : 'Upload'}
      </label>
      <input
        style="visibility: hidden; position:absolute;"
        type="file"
        id="single"
        accept="image/*"
        bind:files
        on:change={uploadAvatar}
        disabled={uploading}
      />
    </div>
  </div>
  
  <style>
    .avatar {
      border-radius: 50%;
      overflow: hidden;
      max-width: 100%;
    }
  
    .avatar.no-image {
      background-color: #333;
      border: 1px solid rgb(200, 200, 200);
      border-radius: 50%;
    }
  
    .button {
      display: block;
      width: 100%;
      height: 40px;
      line-height: 40px;
      text-align: center;
      background-color: #4CAF50;
      color: white;
      border-radius: 4px;
      cursor: pointer;
    }
  
    input[type="file"] {
      position: absolute;
      visibility: hidden;
    }
  </style>