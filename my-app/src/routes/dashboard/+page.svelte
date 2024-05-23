<script>
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import { user } from '$lib/userStore';
  import { Card, Avatar, Sidebar, SidebarItem, SidebarGroup, SidebarWrapper, SidebarDropdownWrapper, SidebarDropdownItem, Footer, FooterLink, FooterLinkGroup, Progressbar } from 'flowbite-svelte';
  import Navbar from '../../components/Navbar.svelte';
  import BottomNav from '../../components/BottomNav.svelte';
  import Spacer from '../../components/Spacer.svelte';
  import { goto } from '$app/navigation';

  let userData = null;
  let errorMessage = '';
  let completedTasks = 0;
  let totalTasks = 0;

  onMount(async () => {
    await fetchUserData();
    await fetchTaskData();
  });

  async function fetchUserData() {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', $user.id)
        .single();

      if (error) {
        console.error('Error fetching user data:', error);
        errorMessage = 'Failed to fetch user data. Please try again.';
      } else {
        userData = data;
        user.update((currentUser) => ({
          ...currentUser,
          ...data,
        }));
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      errorMessage = 'An error occurred. Please try again later.';
    }
  }

  async function fetchTaskData() {
    try {
      const { data, error } = await supabase
        .from('tasks')
        .select('*')
        .eq('user_id', $user.id);

      if (error) {
        console.error('Error fetching task data:', error);
      } else {
        completedTasks = data.filter(task => task.completed).length;
        totalTasks = data.length;
      }
    } catch (error) {
      console.error('Error fetching task data:', error);
    }
  }

  async function handleLogout() {
    await supabase.auth.signOut();
    user.set(null);
    goto('/auth');
  }
</script>

<div class="dashboard-page">
  <Navbar />

  <div class="content">
    <Sidebar>
      <SidebarWrapper>
        <SidebarGroup>
          <SidebarItem label="Logout" on:click={handleLogout} />
          <SidebarItem label="Tasks" />
          <SidebarItem label="Analytics" />
        </SidebarGroup>
        <SidebarGroup>
          <SidebarDropdownWrapper label="Settings">
            <SidebarDropdownItem label="Profile" href="/dashboard/profile" />
            <SidebarDropdownItem label="Notifications" />
            <SidebarDropdownItem label="Billing" />
          </SidebarDropdownWrapper>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarItem label="Support" />
        </SidebarGroup>
      </SidebarWrapper>
    </Sidebar>

    <div class="main-content">
      <Card class="mb-4">
        {#if errorMessage}
          <p class="text-red-500 mb-4">{errorMessage}</p>
        {/if}
        {#if userData}
          <div class="flex items-center mb-4">
            <Avatar src={userData.avatar_url || 'https://i.pravatar.cc/150?img=3'} size="lg" />
            <div class="ml-4">
              <h2 class="text-2xl font-bold">Welcome, {userData.username}!</h2>
              <p class="text-gray-600">{userData.email}</p>
            </div>
          </div>
          <!-- Display other user data or dashboard content -->
        {:else}
          <p>Loading user data...</p>
        {/if}
      </Card>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card>
          <h3 class="text-xl font-bold mb-2">Task Progress</h3>
          <div>
            <p class="text-gray-600">Completed Tasks: {completedTasks}/{totalTasks}</p>
            <Progressbar progress={completedTasks / totalTasks * 100} size="h-4" />
          </div>
        </Card>
        <!-- Add more cards for other dashboard data -->
      </div>
    </div>
  </div>

  <Footer class="mt-auto">
    <FooterLinkGroup>
      <FooterLink href="/">Home</FooterLink>
      <FooterLink href="/about">About</FooterLink>
      <FooterLink href="/contact">Contact</FooterLink>
    </FooterLinkGroup>
    <p class="text-center text-gray-600">
      &copy; {new Date().getFullYear()} Your Company. All rights reserved.
    </p>
  </Footer>

  <BottomNav />
</div>

<style>
  .dashboard-page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .content {
    display: flex;
    flex: 1;
  }

  .main-content {
    flex: 1;
    padding: 1rem;
  }
</style>
