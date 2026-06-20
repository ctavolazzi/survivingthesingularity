<script>
	import { onMount } from 'svelte';
	import InfoModal from '$lib/components/InfoModal.svelte';

	let showInfo = false;

	const YEAR_START = 2026;
	const YEAR_SPAN = 14; // through 2040
	const ADOPTION_K = 1.1;
	const MAINSTREAM = 0.5;
	const INDEPENDENT = 0.8;

	let wrap;
	let canvas;
	let ctx;
	let revealed = false;
	let reducedMotion = false;

	// controls
	let takeoff = 6; // adoption midpoint, years after start (3 = fast, 10 = slow)
	let hoursPerWeek = 10;

	// animation state
	let progress = 0;
	let raf = null;
	let animStart = 0;
	const ANIM_MS = 2400;

	$: rate = hoursPerWeek * 0.04;
	$: tReach = 1.609 / rate; // independence(t) = 1 - e^(-rt) hits 0.8
	$: windowYear = YEAR_START + takeoff;
	$: reachYear = YEAR_START + tReach;
	$: verdict =
		tReach <= takeoff - 1
			? { text: 'AHEAD OF THE CURVE', cls: 'ok' }
			: tReach <= takeoff
				? { text: 'JUST IN TIME', cls: 'warn' }
				: { text: 'WINDOW MISSED', cls: 'bad' };

	function adoption(t) {
		return 1 / (1 + Math.exp(-ADOPTION_K * (t - takeoff)));
	}
	function independence(t) {
		return 1 - Math.exp(-rate * t);
	}

	function sizeCanvas() {
		if (!canvas) return;
		const dpr = Math.min(window.devicePixelRatio || 1, 2);
		const r = canvas.getBoundingClientRect();
		if (!r.width) return;
		canvas.width = r.width * dpr;
		canvas.height = r.height * dpr;
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
	}

	function draw() {
		if (!ctx) return;
		const W = canvas.getBoundingClientRect().width;
		const H = canvas.getBoundingClientRect().height;
		const PAD = { l: 46, r: 18, t: 18, b: 30 };
		const plotW = W - PAD.l - PAD.r;
		const plotH = H - PAD.t - PAD.b;
		const X = (t) => PAD.l + (t / YEAR_SPAN) * plotW;
		const Y = (v) => PAD.t + (1 - v) * plotH;

		ctx.clearRect(0, 0, W, H);
		const fontPx = W < 520 ? 12.5 : 11;
		ctx.font = `${fontPx}px "JetBrains Mono", monospace`;

		// closed-window band
		if (takeoff < YEAR_SPAN) {
			ctx.fillStyle = 'rgba(239,68,68,0.06)';
			ctx.fillRect(X(takeoff), PAD.t, plotW - (X(takeoff) - PAD.l), plotH);
			ctx.strokeStyle = 'rgba(239,68,68,0.35)';
			ctx.setLineDash([4, 5]);
			ctx.beginPath();
			ctx.moveTo(X(takeoff), PAD.t);
			ctx.lineTo(X(takeoff), PAD.t + plotH);
			ctx.stroke();
			ctx.setLineDash([]);
			ctx.fillStyle = 'rgba(239,68,68,0.8)';
			ctx.fillText('window closes', X(takeoff) + 6, PAD.t + 12);
		}

		// grid + year labels (sparser labels on narrow screens)
		const labelStep = W < 520 ? 4 : 2;
		ctx.strokeStyle = 'rgba(148,163,184,0.08)';
		ctx.fillStyle = '#cbd5e1';
		ctx.textAlign = 'center';
		for (let yr = 0; yr <= YEAR_SPAN; yr += 2) {
			ctx.beginPath();
			ctx.moveTo(X(yr), PAD.t);
			ctx.lineTo(X(yr), PAD.t + plotH);
			ctx.stroke();
			if (yr % labelStep === 0) ctx.fillText(String(YEAR_START + yr), X(yr), H - 10);
		}
		ctx.textAlign = 'left';

		// thresholds
		ctx.setLineDash([3, 5]);
		ctx.strokeStyle = 'rgba(59,130,246,0.35)';
		ctx.beginPath();
		ctx.moveTo(PAD.l, Y(MAINSTREAM));
		ctx.lineTo(W - PAD.r, Y(MAINSTREAM));
		ctx.stroke();
		ctx.fillStyle = 'rgba(96,165,250,0.8)';
		ctx.fillText('mainstream', PAD.l + 4, Y(MAINSTREAM) - 5);

		ctx.strokeStyle = 'rgba(245,158,11,0.35)';
		ctx.beginPath();
		ctx.moveTo(PAD.l, Y(INDEPENDENT));
		ctx.lineTo(W - PAD.r, Y(INDEPENDENT));
		ctx.stroke();
		ctx.fillStyle = 'rgba(251,191,36,0.85)';
		ctx.fillText('independent', PAD.l + 4, Y(INDEPENDENT) - 5);
		ctx.setLineDash([]);

		// y axis label
		ctx.save();
		ctx.translate(14, PAD.t + plotH / 2);
		ctx.rotate(-Math.PI / 2);
		ctx.textAlign = 'center';
		ctx.fillStyle = '#cbd5e1';
		ctx.fillText('PROGRESS', 0, 0);
		ctx.restore();

		// curves, drawn up to animation progress
		const tMax = progress * YEAR_SPAN;
		const drawCurve = (fn, color, glow) => {
			ctx.strokeStyle = color;
			ctx.lineWidth = 2.5;
			ctx.shadowColor = glow;
			ctx.shadowBlur = 10;
			ctx.beginPath();
			for (let t = 0; t <= tMax; t += 0.07) {
				const x = X(t);
				const y = Y(fn(t));
				t === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
			}
			ctx.stroke();
			ctx.shadowBlur = 0;
			// head dot
			if (tMax > 0 && tMax < YEAR_SPAN) {
				ctx.fillStyle = color;
				ctx.beginPath();
				ctx.arc(X(tMax), Y(fn(tMax)), 3.5, 0, Math.PI * 2);
				ctx.fill();
			}
		};
		drawCurve(adoption, '#3b82f6', 'rgba(59,130,246,0.6)');
		drawCurve(independence, '#f59e0b', 'rgba(245,158,11,0.6)');

		// crossing markers once animation passes them
		if (tMax >= takeoff) {
			ctx.fillStyle = '#3b82f6';
			ctx.beginPath();
			ctx.arc(X(takeoff), Y(MAINSTREAM), 5, 0, Math.PI * 2);
			ctx.fill();
		}
		if (tMax >= tReach && tReach <= YEAR_SPAN) {
			ctx.fillStyle = '#f59e0b';
			ctx.beginPath();
			ctx.arc(X(tReach), Y(INDEPENDENT), 5, 0, Math.PI * 2);
			ctx.fill();
		}

		// curve legends
		ctx.fillStyle = '#60a5fa';
		ctx.fillText('AI ADOPTION', W - PAD.r - 92, Y(adoption(YEAR_SPAN)) - 8);
		ctx.fillStyle = '#fbbf24';
		const iy = Y(independence(YEAR_SPAN));
		ctx.fillText('YOUR BUILD', W - PAD.r - 86, iy + (Math.abs(iy - Y(adoption(YEAR_SPAN))) < 22 ? 18 : -8));
	}

	function animate(now) {
		if (!animStart) animStart = now;
		const p = Math.min((now - animStart) / ANIM_MS, 1);
		progress = 1 - Math.pow(1 - p, 3);
		draw();
		if (p < 1) raf = requestAnimationFrame(animate);
		else raf = null;
	}

	function replay() {
		if (raf) cancelAnimationFrame(raf);
		if (reducedMotion) {
			progress = 1;
			draw();
			return;
		}
		animStart = 0;
		progress = 0;
		raf = requestAnimationFrame(animate);
	}

	function onParamChange() {
		// redraw fully without replaying the whole animation if already complete
		if (raf === null && progress > 0) {
			progress = 1;
			draw();
		}
	}

	$: if (ctx && (takeoff || hoursPerWeek)) onParamChange();

	onMount(() => {
		ctx = canvas.getContext('2d');
		reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		sizeCanvas();

		const onResize = () => {
			sizeCanvas();
			draw();
		};
		window.addEventListener('resize', onResize);

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						revealed = true;
						sizeCanvas();
						replay();
						observer.disconnect();
					}
				});
			},
			{ threshold: 0.3 }
		);
		observer.observe(wrap);

		return () => {
			window.removeEventListener('resize', onResize);
			observer.disconnect();
			if (raf) cancelAnimationFrame(raf);
		};
	});

	function fmtYear(y) {
		return y > YEAR_START + YEAR_SPAN ? `>${YEAR_START + YEAR_SPAN}` : `~${Math.round(y)}`;
	}
</script>

<div class="window-sim" bind:this={wrap} class:revealed>
	<div class="sim-top">
		<span class="sim-title">THE RACE: A TOY MODEL</span>
		<div class="sim-top-actions">
			<button class="sim-replay" on:click={() => (showInfo = true)} aria-label="How this simulation works">ⓘ How it works</button>
			<button class="sim-replay" on:click={replay}>↻ Replay</button>
		</div>
	</div>

	<canvas bind:this={canvas} aria-label="Animated chart racing AI mainstream adoption against your independence build-out"></canvas>

	<div class="sim-readouts">
		<div class="readout" title="The year AI capability crosses the mainstream line in this model. After that, the early-mover advantage is gone.">
			<span class="r-key">Window closes</span>
			<span class="r-val blue">{fmtYear(windowYear)}</span>
		</div>
		<div class="readout" title="The year your compounding build effort crosses the independence line in this model.">
			<span class="r-key">You arrive</span>
			<span class="r-val amber">{fmtYear(reachYear)}</span>
		</div>
		<div class="readout">
			<span class="r-key">Verdict</span>
			<span class="r-val verdict-{verdict.cls}">{verdict.text}</span>
		</div>
	</div>

	<div class="sim-controls">
		<label class="control">
			<span class="c-label">AI takeoff speed</span>
			<input type="range" min="3" max="10" step="0.5" bind:value={takeoff} style="direction: rtl" />
			<span class="c-val">{takeoff <= 4.5 ? 'fast' : takeoff <= 7 ? 'medium' : 'slow'}</span>
		</label>
		<label class="control">
			<span class="c-label">Your build pace</span>
			<input type="range" min="2" max="40" step="1" bind:value={hoursPerWeek} />
			<span class="c-val">{hoursPerWeek} hrs/wk</span>
		</label>
	</div>

	<p class="sim-caption">
		A deliberately simple model with made-up math: it illustrates the author's framing. The
		usefulness of preparation depends on starting before capability goes mainstream. It
		predicts nothing. Not a forecast, not advice.
	</p>
</div>

<InfoModal open={showInfo} title="How this race works" on:close={() => (showInfo = false)}>
	<p><strong style="color:#60a5fa">Blue curve: AI adoption.</strong> An S-curve: slow, then sudden, then saturated. The "AI takeoff speed" slider moves the midpoint. When it crosses the <em>mainstream</em> line, the window closes: whatever advantage early skills gave is priced in.</p>
	<p><strong style="color:#fbbf24">Amber curve: your build.</strong> Compounding skill and infrastructure. The "build pace" slider sets how many hours a week you put in. It crosses the <em>independent</em> line when the model says your setup covers your needs.</p>
	<p>The verdict compares the two crossing points. That's the whole model: two curves and a race. The math is invented for illustration; the framing is the author's hypothesis, not a forecast.</p>
</InfoModal>

<style>
	.window-sim {
		margin-top: 3rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: 1.25rem 1.5rem 1.5rem;
		opacity: 0;
		transform: translateY(24px);
		transition: opacity 0.9s ease, transform 0.9s ease;
	}
	.window-sim.revealed {
		opacity: 1;
		transform: none;
	}
	.sim-top {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}
	.sim-title {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		font-weight: 600;
		letter-spacing: 0.18em;
		color: var(--color-primary);
	}
	.sim-top-actions {
		display: flex;
		gap: 0.5rem;
	}
	.sim-replay {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		letter-spacing: 0.1em;
		color: #94a3b8;
		background: transparent;
		border: 1px solid var(--color-border-hover);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.85rem;
		cursor: pointer;
		transition: color 0.2s, border-color 0.2s;
	}
	.sim-replay:hover {
		color: var(--color-primary);
		border-color: var(--color-primary);
	}
	canvas {
		display: block;
		width: 100%;
		height: 320px;
	}
	.sim-readouts {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.75rem;
		margin-top: 1.1rem;
	}
	.readout {
		background: rgba(2, 6, 23, 0.5);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		padding: 0.7rem 0.9rem;
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
	}
	.r-key {
		font-family: var(--font-mono);
		font-size: 0.62rem;
		letter-spacing: 0.16em;
		text-transform: uppercase;
		color: #94a3b8;
	}
	.r-val {
		font-family: var(--font-mono);
		font-size: 1.05rem;
		font-weight: 600;
		font-variant-numeric: tabular-nums;
	}
	.r-val.blue { color: var(--color-secondary-light); }
	.r-val.amber { color: var(--color-primary-light); }
	.verdict-ok { color: var(--color-success); }
	.verdict-warn { color: var(--color-warning); }
	.verdict-bad { color: var(--color-error); }
	.sim-controls {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem 2.5rem;
		margin-top: 1.1rem;
	}
	.control {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}
	.c-label {
		font-family: var(--font-mono);
		font-size: 0.66rem;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: #94a3b8;
		white-space: nowrap;
	}
	.c-val {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: var(--color-primary-light);
		min-width: 4.5rem;
	}
	input[type='range'] {
		-webkit-appearance: none;
		appearance: none;
		width: 130px;
		height: 3px;
		background: var(--color-bg-tertiary);
		border-radius: 2px;
		outline: none;
	}
	input[type='range']::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 14px;
		height: 14px;
		border-radius: 50%;
		background: var(--color-primary);
		cursor: pointer;
	}
	input[type='range']::-moz-range-thumb {
		width: 14px;
		height: 14px;
		border-radius: 50%;
		background: var(--color-primary);
		border: none;
		cursor: pointer;
	}
	.sim-caption {
		margin-top: 1rem;
		font-family: var(--font-mono);
		font-size: 0.72rem;
		line-height: 1.6;
		color: #94a3b8;
	}
	@media (max-width: 640px) {
		.sim-readouts { grid-template-columns: 1fr; }
		canvas { height: 260px; }
	}
	@media (prefers-reduced-motion: reduce) {
		.window-sim { transition: none; opacity: 1; }
	}
</style>
