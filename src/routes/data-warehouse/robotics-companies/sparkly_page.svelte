<script>
    import { onMount } from 'svelte';
    import * as THREE from 'three';
    import { fade, fly, scale } from 'svelte/transition';
    import { elasticOut } from 'svelte/easing';
    import { tweened } from 'svelte/motion';

    let container;
    let scene, camera, renderer, particles;
    let titleVisible = false;

    const glowIntensity = tweened(0, {
        duration: 2000,
        easing: elasticOut
    });

    onMount(() => {
        initScene();
        animate();
        setTimeout(() => titleVisible = true, 500);

        return () => {
            if (renderer) {
                renderer.dispose();
            }
            if (scene) {
                scene.clear();
            }
        };
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
        const material = new THREE.PointsMaterial({ color: 0xffffff, size: 2, transparent: true, opacity: 0.8 });
        particles = new THREE.Points(geometry, material);
        scene.add(particles);

        camera.position.z = 1000;

        window.addEventListener('resize', onWindowResize, false);
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function animate() {
        requestAnimationFrame(animate);
        particles.rotation.x += 0.0001;
        particles.rotation.y += 0.0001;
        renderer.render(scene, camera);
    }
</script>

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
        overflow: hidden;
        background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
        color: #fff;
        font-family: 'Arial', sans-serif;
    }

    .particle-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    .content-container {
        position: absolute;
        top: 75px; /* Positioned 75px from the top */
        left: 0;
        right: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
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
        color: #f0f0f0;
        text-align: center;
        max-width: 800px;
        margin: 2rem auto 0;
        line-height: 1.5;
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }

    .char {
        display: inline-block;
        animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) backwards;
    }

    @media (max-height: 500px) {
        .content-container {
            top: 30px; /* Adjust for very small heights */
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
