<script>
    import { onMount } from 'svelte';
    import * as THREE from 'three';
    import { fade, fly, scale } from 'svelte/transition';
    import { elasticOut } from 'svelte/easing';
    import { tweened } from 'svelte/motion';
    import RoboticsCompanies from '$lib/components/RoboticsCompanies.svelte';
    import { darkMode } from '$lib/stores/darkMode';

    let container;
    let scene, camera, renderer, particles;
    let titleVisible = false;
    let resizeObserver;

    const glowIntensity = tweened(0, {
        duration: 2000,
        easing: elasticOut
    });

    onMount(() => {
        console.log("onMount called");
        initScene();
        animate();
        setTimeout(() => titleVisible = true, 500);

        resizeObserver = new ResizeObserver(() => {
            console.log("ResizeObserver callback");
            onWindowResize();
        });
        resizeObserver.observe(container);

        return () => {
            if (renderer) {
                renderer.dispose();
            }
            if (scene) {
                scene.clear();
            }
            if (resizeObserver) {
                resizeObserver.disconnect();
            }
        };
    });

    function initScene() {
        console.log("initScene called");
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0000FF);
        
        const aspect = window.innerWidth / window.innerHeight;
        const frustumSize = 1000;
        camera = new THREE.OrthographicCamera(
            frustumSize * aspect / -2, 
            frustumSize * aspect / 2, 
            frustumSize / 2, 
            frustumSize / -2, 
            0.1, 
            2000
        );
        
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        for (let i = 0; i < 15000; i++) {
            vertices.push(THREE.MathUtils.randFloatSpread(2000) * aspect);
            vertices.push(THREE.MathUtils.randFloatSpread(2000));
            vertices.push(THREE.MathUtils.randFloatSpread(1000));
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

        const material = new THREE.PointsMaterial({ 
            size: 5, 
            transparent: true, 
            opacity: $darkMode ? 1 : 0.8, 
            sizeAttenuation: false
        });
        particles = new THREE.Points(geometry, material);
        scene.add(particles);

        updateParticleColor();

        // Subscribe to darkMode changes
        const unsubscribe = darkMode.subscribe(() => {
            updateParticleColor();
        });

        camera.position.z = 500;

        window.addEventListener('resize', onWindowResize, false);

        // Clean up the subscription when the component is destroyed
        return () => {
            unsubscribe();
            window.removeEventListener('resize', onWindowResize);
        };
    }

    function updateParticleColor() {
        const color = $darkMode ? 0xffffff : 0x000000;
        const opacity = $darkMode ? 0.8 : 0.5;
        particles.material.color.setHex(color);
        particles.material.opacity = opacity;
    }

    function onWindowResize() {
        const aspect = window.innerWidth / window.innerHeight;
        const frustumSize = 1000;
        
        camera.left = frustumSize * aspect / -2;
        camera.right = frustumSize * aspect / 2;
        camera.top = frustumSize / 2;
        camera.bottom = frustumSize / -2;
        
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        
        // Update particle positions
        const positions = particles.geometry.attributes.position.array;
        for (let i = 0; i < positions.length; i += 3) {
            positions[i] = THREE.MathUtils.randFloatSpread(2000) * aspect;
        }
        particles.geometry.attributes.position.needsUpdate = true;
    }

    function animate() {
        console.log("animate called");
        requestAnimationFrame(animate);
        particles.rotation.x += 0.0001;
        particles.rotation.y += 0.0001;
        renderer.render(scene, camera);
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
    }

    :global(body:not(.dark)) {
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
        height: 100vh;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
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
        padding: 20px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    :global(body:not(.dark)) .companies-container {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
    }

    :global(body.dark) .companies-container {
        background-color: rgba(0, 0, 0, 0.2);
        color: #e0e0e0;
    }

    .title-container {
        animation: float 6s ease-in-out infinite;
    }

    .title {
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: bold;
        margin: 0;
        background: linear-gradient(45deg, #440c79, #350588);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite;
        line-height: 1.2;
        text-align: center;
    }

    .subtitle {
        font-size: clamp(2rem, 7vw, 4rem);
        background: linear-gradient(45deg, #FF4081, #FFA000);
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
        transition: color 0.3s ease, text-shadow 0.3s ease;
    }

    :global(body:not(.dark)) .tagline {
        color: #555;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    :global(body.dark) .tagline {
        color: #e0e0e0;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
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

    :global(.company-card) {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }

    :global(body:not(.dark)) .company-card {
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    :global(body.dark) .company-card {
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    :global(.company-card:hover) {
        transform: translateY(-5px);
    }

    :global(body:not(.dark)) .company-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    :global(body.dark) .company-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    :global(.company-card h2) {
        font-size: 1.5rem;
        margin-bottom: 10px;
    }

    :global(body:not(.dark)) .company-card h2 {
        color: #2196F3;
    }

    :global(body.dark) .company-card h2 {
        color: #00aeff;
    }

    :global(.company-card p) {
        margin: 8px 0;
    }

    :global(body:not(.dark)) .company-card p {
        color: #333;
    }

    :global(body.dark) .company-card p {
        color: #e0e0e0;
    }

    :global(.company-card strong) {
        font-weight: 600;
    }

    :global(body:not(.dark)) .company-card strong {
        color: #FF4081;
    }

    :global(body.dark) .company-card strong {
        color: #ff00aa;
    }

    :global(.company-card a) {
        display: inline-block;
        margin-right: 10px;
        text-decoration: none;
        padding: 5px 10px;
        border-radius: 5px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    :global(body:not(.dark)) .company-card a {
        color: #2196F3;
        border: 1px solid #2196F3;
    }

    :global(body.dark) .company-card a {
        color: #00aeff;
        border: 1px solid #00aeff;
    }

    :global(body:not(.dark)) .company-card a:hover {
        background-color: #2196F3;
        color: #ffffff;
    }

    :global(body.dark) .company-card a:hover {
        background-color: #00aeff;
        color: #1a1a1a;
    }
</style>
