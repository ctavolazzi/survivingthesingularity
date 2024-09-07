<script>
    import { onMount, afterUpdate } from 'svelte';
    import * as THREE from 'three';
    import { fade, fly, scale } from 'svelte/transition';
    import { elasticOut } from 'svelte/easing';
    import { tweened } from 'svelte/motion';
    import RoboticsCompanies from '$lib/components/RoboticsCompanies.svelte';
    import { darkMode } from '$lib/stores/darkMode';
    import { browser } from '$app/environment';

    let container;
    let scene, camera, renderer, particles;
    let titleVisible = false;
    let particleColor = 0xffffff;

    console.log("darkMode in robotics-companies/+page.svelte: start of script", $darkMode);
    console.log("typeof darkMode in robotics-companies/+page.svelte: start of script", typeof $darkMode);

    function updateParticleColor(isDarkMode) {
        if (particles) {
            particles.material.color.setHex(isDarkMode ? 0xffffff : 0x000000);
            particles.material.needsUpdate = true;
        }
    }

    $: {
        particleColor = $darkMode ? 0xffffff : 0x000000;
        if (browser) {
            document.body.classList.toggle('dark', $darkMode);
        }
    }

    onMount(() => {
        initScene();
        animate();
        setTimeout(() => titleVisible = true, 500);

        // Initial color update
        updateParticleColor($darkMode);

        // Listen for dark mode changes
        const handleDarkModeChange = (event) => {
            updateParticleColor(event.detail);
        };
        window.addEventListener('darkModeChanged', handleDarkModeChange);

        return () => {
            if (renderer) {
                renderer.dispose();
            }
            if (scene) {
                scene.clear();
            }
            window.removeEventListener('darkModeChanged', handleDarkModeChange);
        };
    });

    afterUpdate(() => {
        if (particles) {
            particles.material.color.setHex(particleColor);
            particles.material.needsUpdate = true;
        }
        console.log("darkMode in robotics-companies/+page.svelte: afterUpdate", $darkMode);
        console.log("typeof darkMode in robotics-companies/+page.svelte: afterUpdate", typeof $darkMode);
    });

    function initScene() {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        for (let i = 0; i < 15000; i++) {
            vertices.push(THREE.MathUtils.randFloatSpread(2000));
            vertices.push(THREE.MathUtils.randFloatSpread(2000));
            vertices.push(THREE.MathUtils.randFloatSpread(2000));
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        const material = new THREE.PointsMaterial({ 
            color: particleColor,  // Use the reactive particleColor here
            size: 2, 
            transparent: true, 
            opacity: 0.8
        });
        particles = new THREE.Points(geometry, material);
        scene.add(particles);

        camera.position.z = 1000;

        window.addEventListener('resize', onWindowResize, false);
    }

    function animate() {
        requestAnimationFrame(animate);
        if (particles) {
            particles.rotation.x += 0.0001;
            particles.rotation.y += 0.0001;
        }
        renderer.render(scene, camera);
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    $: console.log("darkMode in robotics-companies/+page.svelte: end of script", $darkMode);
    $: console.log("typeof darkMode in robotics-companies/+page.svelte: end of script", typeof $darkMode);

    $: {
        console.log("Dark mode changed in robotics-companies page. New value:", $darkMode);
        // Your existing dark mode logic here
    }
</script>

<div class="page-container">
    <div bind:this={container} class="particle-container"></div>

    <div class="content-container">
        {#if titleVisible}
            <div class="title-container" in:scale={{duration: 1000, easing: elasticOut}}>
                <h1 class="title">
                    <span class="char" style="animation-delay: 0.1s;">R</span>
                    <span class="char" style="animation-delay: 0.2s;">o</span>
                    <span class="char" style="animation-delay: 0.3s;">b</span>
                    <span class="char" style="animation-delay: 0.4s;">o</span>
                    <span class="char" style="animation-delay: 0.5s;">t</span>
                    <span class="char" style="animation-delay: 0.6s;">i</span>
                    <span class="char" style="animation-delay: 0.7s;">c</span>
                    <span class="char" style="animation-delay: 0.8s;">s</span>
                </h1>
                <h1 class="title subtitle" in:fly={{y: 50, duration: 1000, delay: 1000}}>
                    Revolution
                </h1>
            </div>
            <p class="tagline" in:fade={{delay: 2000, duration: 1000}}>
                These companies are at the forefront of the industry.<br>
                Please feel free to browse or download the raw data.
            </p>
        {/if}
        <div class="companies-container">
            <RoboticsCompanies />
        </div>
    </div>
</div>

<style>
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(0, 174, 255, 0.7), 0 0 40px rgba(166, 142, 255, 0.5); }
        50% { text-shadow: 0 0 40px rgba(0, 174, 255, 0.9), 0 0 80px rgba(166, 142, 255, 0.7); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    @keyframes popIn {
        0% { transform: scale(0); opacity: 0; }
        80% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }

    :global(body) {
        margin: 0;
        overflow-x: hidden;
        overflow-y: auto;
        font-family: 'Arial', sans-serif;
        transition: background-color 0.3s ease, color 0.3s ease;
        background: linear-gradient(to bottom, #f0f4f8, #d0e4f5);
        color: #333;
    }

    :global(body.dark) {
        background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
        color: #fff;
    }

    .page-container {
        position: relative;
        width: 100%;
        min-height: 100vh;
    }

    .particle-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
    }

    .content-container {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 75px 20px 20px;
    }

    .companies-container {
        width: 100%;
        max-width: 1200px;
        margin-top: 2rem;
    }

    .title-container {
        animation: float 6s ease-in-out infinite;
    }

    .title {
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: bold;
        margin: 0;
        background: linear-gradient(45deg, #00aeff, #a68eff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite;
        line-height: 1.2;
        text-align: center;
    }

    .subtitle {
        font-size: clamp(2rem, 7vw, 4rem);
        background: linear-gradient(45deg, #ff00aa, #ff7700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 0.5rem;
    }

    .tagline {
        font-size: clamp(1rem, 3vw, 1.5rem);
        text-align: center;
        max-width: 800px;
        margin: 2rem auto 0;
        line-height: 1.5;
        color: #333;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        transition: color 0.3s ease, text-shadow 0.3s ease;
    }

    :global(body.dark) .tagline {
        color: #f0f0f0;
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }

    .char {
        display: inline-block;
        animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) backwards;
    }

    @media (max-height: 500px) {
        .content-container {
            padding-top: 30px;
        }
        .title {
            font-size: clamp(2rem, 8vw, 4rem);
        }
        .subtitle {
            font-size: clamp(1.5rem, 6vw, 3rem);
        }
        .tagline {
            font-size: clamp(0.8rem, 2.5vw, 1.2rem);
            margin-top: 1rem;
        }
    }
</style>
