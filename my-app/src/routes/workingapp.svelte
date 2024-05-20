<script>
  import { Alert } from 'flowbite-svelte';
  import { Timeline, TimelineItem, Activity, ActivityItem, Group, GroupItem } from 'flowbite-svelte';
  import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';

  import { Banner } from 'flowbite-svelte';
  import { BullhornSolid } from 'flowbite-svelte-icons';
  import { Button } from 'flowbite-svelte';
  import { Card } from 'flowbite-svelte';
  import { ArrowRightOutline, GiftBoxSolid, ArrowUpRightFromSquareOutline  } from 'flowbite-svelte-icons';

  import { BottomNav, BottomNavItem, Tooltip, Skeleton, ImagePlaceholder } from 'flowbite-svelte';
  import { HomeSolid, WalletSolid, AdjustmentsVerticalOutline, UserCircleSolid, PlusOutline } from 'flowbite-svelte-icons';
</script>

<!-- <Banner id="default-banner" position="absolute">
  <p class="flex items-center text-sm font-normal text-gray-500 dark:text-gray-400">
    <span class="inline-flex p-1 me-3 bg-gray-200 rounded-full dark:bg-gray-600">
      <BullhornSolid class="w-3 h-3 text-gray-500 dark:text-gray-400" />
      <span class="sr-only">Light bulb</span>
    </span>
    <span>
      New brand identity has been launched for the <a href="https://flowbite.com" class="inline font-medium text-primary-600 underline dark:text-primary-500 underline-offset-2 decoration-600 dark:decoration-500 decoration-solid hover:no-underline"> Flowbite Library </a>
    </span>
  </p>
</Banner> -->

<Navbar>
  <NavBrand href="/">
    <img src="https://flowbite.com/docs/images/logo.svg" class="me-3 h-6 sm:h-9" alt="Flowbite Logo" />
    <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Flowbite</span>
  </NavBrand>
  <NavHamburger />
  <NavUl>
    <NavLi href="/">Home</NavLi>
    <NavLi href="/about">About</NavLi>
    <NavLi href="/docs/components/navbar">Navbar</NavLi>
    <NavLi href="/pricing">Pricing</NavLi>
    <NavLi href="/contact">Contact</NavLi>
  </NavUl>
</Navbar>

<Button>Default</Button>
<Button color="alternative">Alternative</Button>
<Button color="dark">Dark</Button>
<Button color="light">Light</Button>
<Button color="blue">Blue</Button>
<Button color="green">Green</Button>
<Button color="red">Red</Button>
<Button color="yellow">Yellow</Button>
<Button color="purple">Purple</Button>

<Card>
  <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Noteworthy technology acquisitions 2021</h5>
  <p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.</p>
  <Button class="w-fit">
    Read more <ArrowRightOutline class="w-6 h-6 ms-2 text-white" />
  </Button>
</Card>

<Card>
  <GiftBoxSolid class="w-8 h-8 mb-3 text-gray-500 dark:text-gray-400" />
  <a href="/">
    <h5 class="mb-2 text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Need a help in Claim?</h5>
  </a>
  <p class="mb-3 font-normal text-gray-500 dark:text-gray-400">Go to this step by step guideline process on how to certify for your weekly benefits:</p>
  <a href="/" class="inline-flex items-center text-primary-600 hover:underline">
    See our guideline
    <ArrowUpRightFromSquareOutline class="w-4 h-4 ms-2.5" />
  </a>
</Card>

<div class="p-8">
  <Alert>
    <span class="font-medium">Info alert!</span>
    Change a few things up and try submitting again.
  </Alert>
</div>

<Timeline>
  <TimelineItem title="Application UI code in Tailwind CSS" date="February 2022">
    <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">
      Get access to over 20+ pages including a dashboard layout, charts, kanban board, calendar, and pre-order E-commerce & Marketing pages.
    </p>
  </TimelineItem>
  <TimelineItem title="Application UI code in Tailwind CSS" date="March 2022">
    <p class="text-base font-normal text-gray-500 dark:text-gray-400">
      All of the pages and components are first designed in Figma and we keep a parity between the two versions even as we update the project.
    </p>
  </TimelineItem>
  <TimelineItem title="Application UI code in Tailwind CSS" date="April 2022">
    <p class="text-base font-normal text-gray-500 dark:text-gray-400">
      Get started with dozens of web components and interactive elements built on top of Tailwind CSS.
    </p>
  </TimelineItem>
</Timeline>



<Skeleton class="py-4" />
<ImagePlaceholder class="pb-20" />

<BottomNav position="fixed" navType="application" classInner="grid-cols-5">
  <BottomNavItem btnName="Home" appBtnPosition="left">
    <HomeSolid class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-500" />
    <Tooltip arrow={false}>Home</Tooltip>
  </BottomNavItem>
  <BottomNavItem btnName="Wallet" appBtnPosition="middle">
    <WalletSolid class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-500" />
    <Tooltip arrow={false}>Wallet</Tooltip>
  </BottomNavItem>
  <div class="flex items-center justify-center">
    <BottomNavItem btnName="Create new item" appBtnPosition="middle" btnClass="inline-flex items-center justify-center w-10 h-10 font-medium bg-primary-600 rounded-full hover:bg-primary-700 group focus:ring-4 focus:ring-primary-300 focus:outline-none dark:focus:ring-primary-800">
      <PlusOutline class="text-white" />
      <Tooltip arrow={false}>Create new item</Tooltip>
    </BottomNavItem>
  </div>
  <BottomNavItem btnName="Settings" appBtnPosition="middle">
    <AdjustmentsVerticalOutline class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-500" />
    <Tooltip arrow={false}>Settings</Tooltip>
  </BottomNavItem>
  <BottomNavItem btnName="Profile" appBtnPosition="right">
    <UserCircleSolid class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-primary-600 dark:group-hover:text-primary-500" />
    <Tooltip arrow={false}>Profile</Tooltip>
  </BottomNavItem>
</BottomNav>
