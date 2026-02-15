<script>
  import { goto } from '$app/navigation';
  import { fade } from 'svelte/transition';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { blueprintProgress } from '$lib/stores/progress.js';
  import { toasts } from '$lib/stores/toasts.js';
  import { sections } from '$lib/data/blueprint.js';

  export let data;

  let user = data?.user;
  let displayName = user?.user_metadata?.full_name || user?.user_metadata?.display_name || '';
  let saving = false;
  let visible = false;

  onMount(() => { visible = true; });

  $: progress = $blueprintProgress;
  $: completedSections = Object.entries(progress).filter(([_, v]) => v.readAt);
  $: completedCount = completedSections.length;
  $: progressPercent = Math.round((completedCount / sections.length) * 100);
  $: avatarLetter = (displayName || user?.email || 'B')[0].toUpperCase();
  $: memberSince = user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : null;

  // Calculate reading streak (days with reads)
  $: readDates = completedSections.map(([_, v]) => new Date(v.readAt).toDateString());
  $: uniqueDays = [...new Set(readDates)].length;

  async function updateProfile() {
    saving = true;
    try {
      const { createSupabaseBrowserClient } = await import('$lib/supabase.js');
      const supabase = createSupabaseBrowserClient();
      const { error } = await supabase.auth.updateUser({
        data: { display_name: displayName }
      });
      if (error) throw error;
      toasts.success('Profile updated.');
    } catch (err) {
      toasts.error(err.message || 'Failed to update.');
    } finally {
      saving = false;
    }
  }

  async function handleLogout() {
    try {
      const { createSupabaseBrowserClient } = await import('$lib/supabase.js');
      const supabase = createSupabaseBrowserClient();
      await supabase.auth.signOut();
      toasts.info('Signed out.');
      goto('/');
    } catch {
      goto('/');
    }
  }

  function resetProgress() {
    if (browser && confirm('Reset all blueprint reading progress? This cannot be undone.')) {
      blueprintProgress.reset();
      toasts.info('Progress reset.');
    }
  }

  function getSectionTitle(slug) {
    return sections.find(s => s.slug === slug)?.title || slug;
  }

  function formatReadDate(iso) {
    return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
</script>

<svelte:head>
  <title>Your Profile — Surviving the Singularity</title>
</svelte:head>

{#if visible}
  <div class="profile-page" in:fade={{ duration: 400 }}>
    <div class="profile-card">
      <!-- Header -->
      <div class="profile-header">
        <div class="profile-avatar">
          <span class="avatar-letter">{avatarLetter}</span>
        </div>
        <div class="profile-info">
          <h1 class="profile-name">{displayName || 'Builder'}</h1>
          {#if user?.email}
            <p class="profile-email">{user.email}</p>
          {/if}
          {#if memberSince}
            <p class="profile-since">Member since {memberSince}</p>
          {/if}
        </div>
      </div>

      <!-- Blueprint Progress -->
      <div class="profile-section">
        <h2 class="section-title">Blueprint Progress</h2>

        <div class="progress-overview">
          <div class="progress-ring-wrap">
            <svg class="progress-ring" viewBox="0 0 100 100">
              <circle class="ring-bg" cx="50" cy="50" r="42" />
              <circle
                class="ring-fill"
                cx="50" cy="50" r="42"
                stroke-dasharray="{2 * Math.PI * 42}"
                stroke-dashoffset="{2 * Math.PI * 42 * (1 - progressPercent / 100)}"
              />
            </svg>
            <div class="ring-text">
              <span class="ring-percent">{progressPercent}%</span>
              <span class="ring-label">Complete</span>
            </div>
          </div>

          <div class="progress-stats">
            <div class="stat">
              <span class="stat-val">{completedCount}</span>
              <span class="stat-label">Chapters Read</span>
            </div>
            <div class="stat">
              <span class="stat-val">{sections.length - completedCount}</span>
              <span class="stat-label">Remaining</span>
            </div>
            <div class="stat">
              <span class="stat-val">{uniqueDays}</span>
              <span class="stat-label">Days Active</span>
            </div>
          </div>
        </div>

        {#if completedCount > 0}
          <div class="completed-list">
            <h3 class="completed-title">Completed Chapters</h3>
            {#each completedSections as [slug, data]}
              <a href="/blueprint/{slug}" class="completed-item">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                <span class="completed-name">{getSectionTitle(slug)}</span>
                <span class="completed-date">{formatReadDate(data.readAt)}</span>
              </a>
            {/each}
          </div>
        {/if}

        {#if completedCount < sections.length}
          <a href="/blueprint" class="btn-continue">
            {completedCount === 0 ? 'Start the Blueprint' : 'Continue Reading'}
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7H12M12 7L8 3M12 7L8 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
        {:else}
          <div class="blueprint-complete">
            <span class="complete-badge">Blueprint Mastered</span>
            <p class="complete-text">You've read every chapter. Time to execute.</p>
          </div>
        {/if}
      </div>

      <!-- Profile Settings (only if logged in) -->
      {#if user}
        <div class="profile-section">
          <h2 class="section-title">Profile Settings</h2>
          <form on:submit|preventDefault={updateProfile} class="profile-form">
            <div class="form-field">
              <label for="displayName" class="form-label">Display Name</label>
              <input
                id="displayName"
                type="text"
                bind:value={displayName}
                placeholder="What should we call you?"
                class="form-input"
              />
            </div>
            <div class="form-field">
              <label class="form-label">Email</label>
              <input type="email" value={user?.email || ''} disabled class="form-input form-input-disabled" />
            </div>
            <button type="submit" class="btn-save" disabled={saving}>
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        </div>

        <div class="profile-section profile-actions">
          <button class="btn-reset" on:click={resetProgress}>Reset Blueprint Progress</button>
          <button class="btn-logout" on:click={handleLogout}>Sign Out</button>
        </div>
      {:else}
        <div class="profile-section">
          <p class="no-auth-note">
            <a href="/login" class="login-link">Sign in</a> to save your profile and sync progress across devices.
          </p>
        </div>

        <div class="profile-section profile-actions">
          <button class="btn-reset" on:click={resetProgress}>Reset Blueprint Progress</button>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .profile-page {
    display: flex;
    justify-content: center;
    padding: 3rem 1rem 5rem;
  }

  .profile-card {
    width: 100%;
    max-width: 600px;
  }

  .profile-header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 2rem;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 18px;
    margin-bottom: 1.5rem;
  }

  .profile-avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(249, 115, 22, 0.2));
    border: 2px solid rgba(245, 158, 11, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .avatar-letter {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f59e0b;
  }

  .profile-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.2rem 0;
  }

  .profile-email {
    font-size: 0.9rem;
    color: #94a3b8;
    margin: 0;
  }

  .profile-since {
    font-size: 0.8rem;
    color: #475569;
    margin: 0.25rem 0 0 0;
  }

  .profile-section {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(148, 163, 184, 0.06);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1rem;
  }

  .section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0 0 1.25rem 0;
  }

  /* Progress ring */
  .progress-overview {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
  }

  .progress-ring-wrap {
    position: relative;
    width: 100px;
    height: 100px;
    flex-shrink: 0;
  }

  .progress-ring {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
  }

  .ring-bg {
    fill: none;
    stroke: rgba(255, 255, 255, 0.06);
    stroke-width: 6;
  }

  .ring-fill {
    fill: none;
    stroke: url(#progress-gradient);
    stroke-width: 6;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.8s ease;
  }

  .ring-text {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .ring-percent {
    font-size: 1.3rem;
    font-weight: 800;
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
  }

  .ring-label {
    font-size: 0.6rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .progress-stats {
    display: flex;
    gap: 1.5rem;
  }

  .stat {
    display: flex;
    flex-direction: column;
  }

  .stat-val {
    font-size: 1.3rem;
    font-weight: 800;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
  }

  .stat-label {
    font-size: 0.68rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  /* Completed list */
  .completed-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0 0 0.75rem 0;
  }

  .completed-list {
    margin-bottom: 1.25rem;
  }

  .completed-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0;
    text-decoration: none;
    border-bottom: 1px solid rgba(148, 163, 184, 0.04);
    transition: background 0.15s;
  }

  .completed-item:hover {
    background: rgba(245, 158, 11, 0.03);
  }

  .completed-name {
    font-size: 0.88rem;
    color: #cbd5e1;
    font-weight: 500;
    flex: 1;
  }

  .completed-date {
    font-size: 0.7rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
  }

  .btn-continue {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.25rem;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 10px;
    color: #f59e0b;
    font-size: 0.88rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s;
  }

  .btn-continue:hover {
    background: rgba(245, 158, 11, 0.15);
    border-color: rgba(245, 158, 11, 0.3);
    transform: translateY(-1px);
  }

  .blueprint-complete {
    text-align: center;
    padding: 1rem 0;
  }

  .complete-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #10b981;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
  }

  .complete-text {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
  }

  /* Form */
  .profile-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-field {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .form-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .form-input {
    padding: 0.7rem 1rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 10px;
    color: #f1f5f9;
    font-size: 0.95rem;
    font-family: inherit;
    transition: border-color 0.2s;
    outline: none;
  }

  .form-input:focus {
    border-color: rgba(245, 158, 11, 0.4);
  }

  .form-input-disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-save {
    padding: 0.7rem 1.5rem;
    background: #f59e0b;
    color: #0f172a;
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    align-self: flex-start;
    font-family: inherit;
  }

  .btn-save:hover:not(:disabled) {
    background: #fbbf24;
  }

  .btn-save:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Actions */
  .profile-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    border-color: transparent;
    background: transparent;
  }

  .btn-logout {
    padding: 0.6rem 1.5rem;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.15);
    border-radius: 10px;
    color: #f87171;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
  }

  .btn-logout:hover {
    background: rgba(239, 68, 68, 0.15);
  }

  .btn-reset {
    padding: 0.6rem 1.5rem;
    background: rgba(148, 163, 184, 0.05);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 10px;
    color: #64748b;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
  }

  .btn-reset:hover {
    background: rgba(148, 163, 184, 0.1);
    color: #94a3b8;
  }

  .no-auth-note {
    font-size: 0.9rem;
    color: #64748b;
    margin: 0;
    text-align: center;
  }

  .login-link {
    color: #f59e0b;
    font-weight: 600;
  }

  @media (max-width: 480px) {
    .profile-header {
      flex-direction: column;
      text-align: center;
    }

    .progress-overview {
      flex-direction: column;
      align-items: center;
    }

    .progress-stats {
      justify-content: center;
    }
  }
</style>

<!-- SVG gradient definition (outside the scoped style) -->
<svg style="position: absolute; width: 0; height: 0;">
  <defs>
    <linearGradient id="progress-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#10b981" />
    </linearGradient>
  </defs>
</svg>
