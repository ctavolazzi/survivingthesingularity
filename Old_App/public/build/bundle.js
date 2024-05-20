
(function(l, r) { if (!l || l.getElementById('livereloadscript')) return; r = l.createElement('script'); r.async = 1; r.src = '//' + (self.location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1'; r.id = 'livereloadscript'; l.getElementsByTagName('head')[0].appendChild(r) })(self.document);
var app = (function () {
	'use strict';

	/** @returns {void} */
	function noop() {}

	const identity = (x) => x;

	/**
	 * @template T
	 * @template S
	 * @param {T} tar
	 * @param {S} src
	 * @returns {T & S}
	 */
	function assign(tar, src) {
		// @ts-ignore
		for (const k in src) tar[k] = src[k];
		return /** @type {T & S} */ (tar);
	}

	/** @returns {void} */
	function add_location(element, file, line, column, char) {
		element.__svelte_meta = {
			loc: { file, line, column, char }
		};
	}

	function run(fn) {
		return fn();
	}

	function blank_object() {
		return Object.create(null);
	}

	/**
	 * @param {Function[]} fns
	 * @returns {void}
	 */
	function run_all(fns) {
		fns.forEach(run);
	}

	/**
	 * @param {any} thing
	 * @returns {thing is Function}
	 */
	function is_function(thing) {
		return typeof thing === 'function';
	}

	/** @returns {boolean} */
	function safe_not_equal(a, b) {
		return a != a ? b == b : a !== b || (a && typeof a === 'object') || typeof a === 'function';
	}

	/** @returns {boolean} */
	function is_empty(obj) {
		return Object.keys(obj).length === 0;
	}

	/** @returns {void} */
	function validate_store(store, name) {
		if (store != null && typeof store.subscribe !== 'function') {
			throw new Error(`'${name}' is not a store with a 'subscribe' method`);
		}
	}

	function subscribe(store, ...callbacks) {
		if (store == null) {
			for (const callback of callbacks) {
				callback(undefined);
			}
			return noop;
		}
		const unsub = store.subscribe(...callbacks);
		return unsub.unsubscribe ? () => unsub.unsubscribe() : unsub;
	}

	/**
	 * Get the current value from a store by subscribing and immediately unsubscribing.
	 *
	 * https://svelte.dev/docs/svelte-store#get
	 * @template T
	 * @param {import('../store/public.js').Readable<T>} store
	 * @returns {T}
	 */
	function get_store_value(store) {
		let value;
		subscribe(store, (_) => (value = _))();
		return value;
	}

	/** @returns {void} */
	function component_subscribe(component, store, callback) {
		component.$$.on_destroy.push(subscribe(store, callback));
	}

	function create_slot(definition, ctx, $$scope, fn) {
		if (definition) {
			const slot_ctx = get_slot_context(definition, ctx, $$scope, fn);
			return definition[0](slot_ctx);
		}
	}

	function get_slot_context(definition, ctx, $$scope, fn) {
		return definition[1] && fn ? assign($$scope.ctx.slice(), definition[1](fn(ctx))) : $$scope.ctx;
	}

	function get_slot_changes(definition, $$scope, dirty, fn) {
		if (definition[2] && fn) {
			const lets = definition[2](fn(dirty));
			if ($$scope.dirty === undefined) {
				return lets;
			}
			if (typeof lets === 'object') {
				const merged = [];
				const len = Math.max($$scope.dirty.length, lets.length);
				for (let i = 0; i < len; i += 1) {
					merged[i] = $$scope.dirty[i] | lets[i];
				}
				return merged;
			}
			return $$scope.dirty | lets;
		}
		return $$scope.dirty;
	}

	/** @returns {void} */
	function update_slot_base(
		slot,
		slot_definition,
		ctx,
		$$scope,
		slot_changes,
		get_slot_context_fn
	) {
		if (slot_changes) {
			const slot_context = get_slot_context(slot_definition, ctx, $$scope, get_slot_context_fn);
			slot.p(slot_context, slot_changes);
		}
	}

	/** @returns {any[] | -1} */
	function get_all_dirty_from_scope($$scope) {
		if ($$scope.ctx.length > 32) {
			const dirty = [];
			const length = $$scope.ctx.length / 32;
			for (let i = 0; i < length; i++) {
				dirty[i] = -1;
			}
			return dirty;
		}
		return -1;
	}

	/** @returns {{}} */
	function exclude_internal_props(props) {
		const result = {};
		for (const k in props) if (k[0] !== '$') result[k] = props[k];
		return result;
	}

	/** @returns {{}} */
	function compute_rest_props(props, keys) {
		const rest = {};
		keys = new Set(keys);
		for (const k in props) if (!keys.has(k) && k[0] !== '$') rest[k] = props[k];
		return rest;
	}

	const is_client = typeof window !== 'undefined';

	/** @type {() => number} */
	let now = is_client ? () => window.performance.now() : () => Date.now();

	let raf = is_client ? (cb) => requestAnimationFrame(cb) : noop;

	const tasks = new Set();

	/**
	 * @param {number} now
	 * @returns {void}
	 */
	function run_tasks(now) {
		tasks.forEach((task) => {
			if (!task.c(now)) {
				tasks.delete(task);
				task.f();
			}
		});
		if (tasks.size !== 0) raf(run_tasks);
	}

	/**
	 * Creates a new task that runs on each raf frame
	 * until it returns a falsy value or is aborted
	 * @param {import('./private.js').TaskCallback} callback
	 * @returns {import('./private.js').Task}
	 */
	function loop(callback) {
		/** @type {import('./private.js').TaskEntry} */
		let task;
		if (tasks.size === 0) raf(run_tasks);
		return {
			promise: new Promise((fulfill) => {
				tasks.add((task = { c: callback, f: fulfill }));
			}),
			abort() {
				tasks.delete(task);
			}
		};
	}

	/** @type {typeof globalThis} */
	const globals =
		typeof window !== 'undefined'
			? window
			: typeof globalThis !== 'undefined'
			? globalThis
			: // @ts-ignore Node typings have this
			  global;

	/**
	 * @param {Node} target
	 * @param {Node} node
	 * @returns {void}
	 */
	function append(target, node) {
		target.appendChild(node);
	}

	/**
	 * @param {Node} node
	 * @returns {ShadowRoot | Document}
	 */
	function get_root_for_style(node) {
		if (!node) return document;
		const root = node.getRootNode ? node.getRootNode() : node.ownerDocument;
		if (root && /** @type {ShadowRoot} */ (root).host) {
			return /** @type {ShadowRoot} */ (root);
		}
		return node.ownerDocument;
	}

	/**
	 * @param {Node} node
	 * @returns {CSSStyleSheet}
	 */
	function append_empty_stylesheet(node) {
		const style_element = element('style');
		// For transitions to work without 'style-src: unsafe-inline' Content Security Policy,
		// these empty tags need to be allowed with a hash as a workaround until we move to the Web Animations API.
		// Using the hash for the empty string (for an empty tag) works in all browsers except Safari.
		// So as a workaround for the workaround, when we append empty style tags we set their content to /* empty */.
		// The hash 'sha256-9OlNO0DNEeaVzHL4RZwCLsBHA8WBQ8toBp/4F5XV2nc=' will then work even in Safari.
		style_element.textContent = '/* empty */';
		append_stylesheet(get_root_for_style(node), style_element);
		return style_element.sheet;
	}

	/**
	 * @param {ShadowRoot | Document} node
	 * @param {HTMLStyleElement} style
	 * @returns {CSSStyleSheet}
	 */
	function append_stylesheet(node, style) {
		append(/** @type {Document} */ (node).head || node, style);
		return style.sheet;
	}

	/**
	 * @param {Node} target
	 * @param {Node} node
	 * @param {Node} [anchor]
	 * @returns {void}
	 */
	function insert(target, node, anchor) {
		target.insertBefore(node, anchor || null);
	}

	/**
	 * @param {Node} node
	 * @returns {void}
	 */
	function detach(node) {
		if (node.parentNode) {
			node.parentNode.removeChild(node);
		}
	}

	/**
	 * @returns {void} */
	function destroy_each(iterations, detaching) {
		for (let i = 0; i < iterations.length; i += 1) {
			if (iterations[i]) iterations[i].d(detaching);
		}
	}

	/**
	 * @template {keyof HTMLElementTagNameMap} K
	 * @param {K} name
	 * @returns {HTMLElementTagNameMap[K]}
	 */
	function element(name) {
		return document.createElement(name);
	}

	/**
	 * @template {keyof SVGElementTagNameMap} K
	 * @param {K} name
	 * @returns {SVGElement}
	 */
	function svg_element(name) {
		return document.createElementNS('http://www.w3.org/2000/svg', name);
	}

	/**
	 * @param {string} data
	 * @returns {Text}
	 */
	function text(data) {
		return document.createTextNode(data);
	}

	/**
	 * @returns {Text} */
	function space() {
		return text(' ');
	}

	/**
	 * @returns {Text} */
	function empty() {
		return text('');
	}

	/**
	 * @param {EventTarget} node
	 * @param {string} event
	 * @param {EventListenerOrEventListenerObject} handler
	 * @param {boolean | AddEventListenerOptions | EventListenerOptions} [options]
	 * @returns {() => void}
	 */
	function listen(node, event, handler, options) {
		node.addEventListener(event, handler, options);
		return () => node.removeEventListener(event, handler, options);
	}

	/**
	 * @returns {(event: any) => any} */
	function prevent_default(fn) {
		return function (event) {
			event.preventDefault();
			// @ts-ignore
			return fn.call(this, event);
		};
	}

	/**
	 * @param {Element} node
	 * @param {string} attribute
	 * @param {string} [value]
	 * @returns {void}
	 */
	function attr(node, attribute, value) {
		if (value == null) node.removeAttribute(attribute);
		else if (node.getAttribute(attribute) !== value) node.setAttribute(attribute, value);
	}
	/**
	 * List of attributes that should always be set through the attr method,
	 * because updating them through the property setter doesn't work reliably.
	 * In the example of `width`/`height`, the problem is that the setter only
	 * accepts numeric values, but the attribute can also be set to a string like `50%`.
	 * If this list becomes too big, rethink this approach.
	 */
	const always_set_through_set_attribute = ['width', 'height'];

	/**
	 * @param {Element & ElementCSSInlineStyle} node
	 * @param {{ [x: string]: string }} attributes
	 * @returns {void}
	 */
	function set_attributes(node, attributes) {
		// @ts-ignore
		const descriptors = Object.getOwnPropertyDescriptors(node.__proto__);
		for (const key in attributes) {
			if (attributes[key] == null) {
				node.removeAttribute(key);
			} else if (key === 'style') {
				node.style.cssText = attributes[key];
			} else if (key === '__value') {
				/** @type {any} */ (node).value = node[key] = attributes[key];
			} else if (
				descriptors[key] &&
				descriptors[key].set &&
				always_set_through_set_attribute.indexOf(key) === -1
			) {
				node[key] = attributes[key];
			} else {
				attr(node, key, attributes[key]);
			}
		}
	}

	/**
	 * @param {Element & ElementCSSInlineStyle} node
	 * @param {{ [x: string]: string }} attributes
	 * @returns {void}
	 */
	function set_svg_attributes(node, attributes) {
		for (const key in attributes) {
			attr(node, key, attributes[key]);
		}
	}

	/**
	 * @param {Record<string, unknown>} data_map
	 * @returns {void}
	 */
	function set_custom_element_data_map(node, data_map) {
		Object.keys(data_map).forEach((key) => {
			set_custom_element_data(node, key, data_map[key]);
		});
	}

	/**
	 * @returns {void} */
	function set_custom_element_data(node, prop, value) {
		const lower = prop.toLowerCase(); // for backwards compatibility with existing behavior we do lowercase first
		if (lower in node) {
			node[lower] = typeof node[lower] === 'boolean' && value === '' ? true : value;
		} else if (prop in node) {
			node[prop] = typeof node[prop] === 'boolean' && value === '' ? true : value;
		} else {
			attr(node, prop, value);
		}
	}

	/**
	 * @param {string} tag
	 */
	function set_dynamic_element_data(tag) {
		return /-/.test(tag) ? set_custom_element_data_map : set_attributes;
	}

	/**
	 * @param {Element} element
	 * @returns {ChildNode[]}
	 */
	function children(element) {
		return Array.from(element.childNodes);
	}

	/**
	 * @returns {void} */
	function set_input_value(input, value) {
		input.value = value == null ? '' : value;
	}

	/**
	 * @returns {void} */
	function set_style(node, key, value, important) {
		if (value == null) {
			node.style.removeProperty(key);
		} else {
			node.style.setProperty(key, value, important ? 'important' : '');
		}
	}

	/**
	 * @returns {void} */
	function toggle_class(element, name, toggle) {
		// The `!!` is required because an `undefined` flag means flipping the current state.
		element.classList.toggle(name, !!toggle);
	}

	/**
	 * @template T
	 * @param {string} type
	 * @param {T} [detail]
	 * @param {{ bubbles?: boolean, cancelable?: boolean }} [options]
	 * @returns {CustomEvent<T>}
	 */
	function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
		return new CustomEvent(type, { detail, bubbles, cancelable });
	}

	/**
	 * @typedef {Node & {
	 * 	claim_order?: number;
	 * 	hydrate_init?: true;
	 * 	actual_end_child?: NodeEx;
	 * 	childNodes: NodeListOf<NodeEx>;
	 * }} NodeEx
	 */

	/** @typedef {ChildNode & NodeEx} ChildNodeEx */

	/** @typedef {NodeEx & { claim_order: number }} NodeEx2 */

	/**
	 * @typedef {ChildNodeEx[] & {
	 * 	claim_info?: {
	 * 		last_index: number;
	 * 		total_claimed: number;
	 * 	};
	 * }} ChildNodeArray
	 */

	// we need to store the information for multiple documents because a Svelte application could also contain iframes
	// https://github.com/sveltejs/svelte/issues/3624
	/** @type {Map<Document | ShadowRoot, import('./private.d.ts').StyleInformation>} */
	const managed_styles = new Map();

	let active = 0;

	// https://github.com/darkskyapp/string-hash/blob/master/index.js
	/**
	 * @param {string} str
	 * @returns {number}
	 */
	function hash(str) {
		let hash = 5381;
		let i = str.length;
		while (i--) hash = ((hash << 5) - hash) ^ str.charCodeAt(i);
		return hash >>> 0;
	}

	/**
	 * @param {Document | ShadowRoot} doc
	 * @param {Element & ElementCSSInlineStyle} node
	 * @returns {{ stylesheet: any; rules: {}; }}
	 */
	function create_style_information(doc, node) {
		const info = { stylesheet: append_empty_stylesheet(node), rules: {} };
		managed_styles.set(doc, info);
		return info;
	}

	/**
	 * @param {Element & ElementCSSInlineStyle} node
	 * @param {number} a
	 * @param {number} b
	 * @param {number} duration
	 * @param {number} delay
	 * @param {(t: number) => number} ease
	 * @param {(t: number, u: number) => string} fn
	 * @param {number} uid
	 * @returns {string}
	 */
	function create_rule(node, a, b, duration, delay, ease, fn, uid = 0) {
		const step = 16.666 / duration;
		let keyframes = '{\n';
		for (let p = 0; p <= 1; p += step) {
			const t = a + (b - a) * ease(p);
			keyframes += p * 100 + `%{${fn(t, 1 - t)}}\n`;
		}
		const rule = keyframes + `100% {${fn(b, 1 - b)}}\n}`;
		const name = `__svelte_${hash(rule)}_${uid}`;
		const doc = get_root_for_style(node);
		const { stylesheet, rules } = managed_styles.get(doc) || create_style_information(doc, node);
		if (!rules[name]) {
			rules[name] = true;
			stylesheet.insertRule(`@keyframes ${name} ${rule}`, stylesheet.cssRules.length);
		}
		const animation = node.style.animation || '';
		node.style.animation = `${
		animation ? `${animation}, ` : ''
	}${name} ${duration}ms linear ${delay}ms 1 both`;
		active += 1;
		return name;
	}

	/**
	 * @param {Element & ElementCSSInlineStyle} node
	 * @param {string} [name]
	 * @returns {void}
	 */
	function delete_rule(node, name) {
		const previous = (node.style.animation || '').split(', ');
		const next = previous.filter(
			name
				? (anim) => anim.indexOf(name) < 0 // remove specific animation
				: (anim) => anim.indexOf('__svelte') === -1 // remove all Svelte animations
		);
		const deleted = previous.length - next.length;
		if (deleted) {
			node.style.animation = next.join(', ');
			active -= deleted;
			if (!active) clear_rules();
		}
	}

	/** @returns {void} */
	function clear_rules() {
		raf(() => {
			if (active) return;
			managed_styles.forEach((info) => {
				const { ownerNode } = info.stylesheet;
				// there is no ownerNode if it runs on jsdom.
				if (ownerNode) detach(ownerNode);
			});
			managed_styles.clear();
		});
	}

	let current_component;

	/** @returns {void} */
	function set_current_component(component) {
		current_component = component;
	}

	function get_current_component() {
		if (!current_component) throw new Error('Function called outside component initialization');
		return current_component;
	}

	/**
	 * Schedules a callback to run immediately before the component is updated after any state change.
	 *
	 * The first time the callback runs will be before the initial `onMount`
	 *
	 * https://svelte.dev/docs/svelte#beforeupdate
	 * @param {() => any} fn
	 * @returns {void}
	 */
	function beforeUpdate(fn) {
		get_current_component().$$.before_update.push(fn);
	}

	/**
	 * Schedules a callback to run immediately before the component is unmounted.
	 *
	 * Out of `onMount`, `beforeUpdate`, `afterUpdate` and `onDestroy`, this is the
	 * only one that runs inside a server-side component.
	 *
	 * https://svelte.dev/docs/svelte#ondestroy
	 * @param {() => any} fn
	 * @returns {void}
	 */
	function onDestroy(fn) {
		get_current_component().$$.on_destroy.push(fn);
	}

	/**
	 * Creates an event dispatcher that can be used to dispatch [component events](https://svelte.dev/docs#template-syntax-component-directives-on-eventname).
	 * Event dispatchers are functions that can take two arguments: `name` and `detail`.
	 *
	 * Component events created with `createEventDispatcher` create a
	 * [CustomEvent](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent).
	 * These events do not [bubble](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#Event_bubbling_and_capture).
	 * The `detail` argument corresponds to the [CustomEvent.detail](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/detail)
	 * property and can contain any type of data.
	 *
	 * The event dispatcher can be typed to narrow the allowed event names and the type of the `detail` argument:
	 * ```ts
	 * const dispatch = createEventDispatcher<{
	 *  loaded: never; // does not take a detail argument
	 *  change: string; // takes a detail argument of type string, which is required
	 *  optional: number | null; // takes an optional detail argument of type number
	 * }>();
	 * ```
	 *
	 * https://svelte.dev/docs/svelte#createeventdispatcher
	 * @template {Record<string, any>} [EventMap=any]
	 * @returns {import('./public.js').EventDispatcher<EventMap>}
	 */
	function createEventDispatcher() {
		const component = get_current_component();
		return (type, detail, { cancelable = false } = {}) => {
			const callbacks = component.$$.callbacks[type];
			if (callbacks) {
				// TODO are there situations where events could be dispatched
				// in a server (non-DOM) environment?
				const event = custom_event(/** @type {string} */ (type), detail, { cancelable });
				callbacks.slice().forEach((fn) => {
					fn.call(component, event);
				});
				return !event.defaultPrevented;
			}
			return true;
		};
	}

	/**
	 * Associates an arbitrary `context` object with the current component and the specified `key`
	 * and returns that object. The context is then available to children of the component
	 * (including slotted content) with `getContext`.
	 *
	 * Like lifecycle functions, this must be called during component initialisation.
	 *
	 * https://svelte.dev/docs/svelte#setcontext
	 * @template T
	 * @param {any} key
	 * @param {T} context
	 * @returns {T}
	 */
	function setContext(key, context) {
		get_current_component().$$.context.set(key, context);
		return context;
	}

	/**
	 * Retrieves the context that belongs to the closest parent component with the specified `key`.
	 * Must be called during component initialisation.
	 *
	 * https://svelte.dev/docs/svelte#getcontext
	 * @template T
	 * @param {any} key
	 * @returns {T}
	 */
	function getContext(key) {
		return get_current_component().$$.context.get(key);
	}

	// TODO figure out if we still want to support
	// shorthand events, or if we want to implement
	// a real bubbling mechanism
	/**
	 * @param component
	 * @param event
	 * @returns {void}
	 */
	function bubble(component, event) {
		const callbacks = component.$$.callbacks[event.type];
		if (callbacks) {
			// @ts-ignore
			callbacks.slice().forEach((fn) => fn.call(this, event));
		}
	}

	const dirty_components = [];
	const binding_callbacks = [];

	let render_callbacks = [];

	const flush_callbacks = [];

	const resolved_promise = /* @__PURE__ */ Promise.resolve();

	let update_scheduled = false;

	/** @returns {void} */
	function schedule_update() {
		if (!update_scheduled) {
			update_scheduled = true;
			resolved_promise.then(flush);
		}
	}

	/** @returns {void} */
	function add_render_callback(fn) {
		render_callbacks.push(fn);
	}

	// flush() calls callbacks in this order:
	// 1. All beforeUpdate callbacks, in order: parents before children
	// 2. All bind:this callbacks, in reverse order: children before parents.
	// 3. All afterUpdate callbacks, in order: parents before children. EXCEPT
	//    for afterUpdates called during the initial onMount, which are called in
	//    reverse order: children before parents.
	// Since callbacks might update component values, which could trigger another
	// call to flush(), the following steps guard against this:
	// 1. During beforeUpdate, any updated components will be added to the
	//    dirty_components array and will cause a reentrant call to flush(). Because
	//    the flush index is kept outside the function, the reentrant call will pick
	//    up where the earlier call left off and go through all dirty components. The
	//    current_component value is saved and restored so that the reentrant call will
	//    not interfere with the "parent" flush() call.
	// 2. bind:this callbacks cannot trigger new flush() calls.
	// 3. During afterUpdate, any updated components will NOT have their afterUpdate
	//    callback called a second time; the seen_callbacks set, outside the flush()
	//    function, guarantees this behavior.
	const seen_callbacks = new Set();

	let flushidx = 0; // Do *not* move this inside the flush() function

	/** @returns {void} */
	function flush() {
		// Do not reenter flush while dirty components are updated, as this can
		// result in an infinite loop. Instead, let the inner flush handle it.
		// Reentrancy is ok afterwards for bindings etc.
		if (flushidx !== 0) {
			return;
		}
		const saved_component = current_component;
		do {
			// first, call beforeUpdate functions
			// and update components
			try {
				while (flushidx < dirty_components.length) {
					const component = dirty_components[flushidx];
					flushidx++;
					set_current_component(component);
					update(component.$$);
				}
			} catch (e) {
				// reset dirty state to not end up in a deadlocked state and then rethrow
				dirty_components.length = 0;
				flushidx = 0;
				throw e;
			}
			set_current_component(null);
			dirty_components.length = 0;
			flushidx = 0;
			while (binding_callbacks.length) binding_callbacks.pop()();
			// then, once components are updated, call
			// afterUpdate functions. This may cause
			// subsequent updates...
			for (let i = 0; i < render_callbacks.length; i += 1) {
				const callback = render_callbacks[i];
				if (!seen_callbacks.has(callback)) {
					// ...so guard against infinite loops
					seen_callbacks.add(callback);
					callback();
				}
			}
			render_callbacks.length = 0;
		} while (dirty_components.length);
		while (flush_callbacks.length) {
			flush_callbacks.pop()();
		}
		update_scheduled = false;
		seen_callbacks.clear();
		set_current_component(saved_component);
	}

	/** @returns {void} */
	function update($$) {
		if ($$.fragment !== null) {
			$$.update();
			run_all($$.before_update);
			const dirty = $$.dirty;
			$$.dirty = [-1];
			$$.fragment && $$.fragment.p($$.ctx, dirty);
			$$.after_update.forEach(add_render_callback);
		}
	}

	/**
	 * Useful for example to execute remaining `afterUpdate` callbacks before executing `destroy`.
	 * @param {Function[]} fns
	 * @returns {void}
	 */
	function flush_render_callbacks(fns) {
		const filtered = [];
		const targets = [];
		render_callbacks.forEach((c) => (fns.indexOf(c) === -1 ? filtered.push(c) : targets.push(c)));
		targets.forEach((c) => c());
		render_callbacks = filtered;
	}

	/**
	 * @type {Promise<void> | null}
	 */
	let promise;

	/**
	 * @returns {Promise<void>}
	 */
	function wait() {
		if (!promise) {
			promise = Promise.resolve();
			promise.then(() => {
				promise = null;
			});
		}
		return promise;
	}

	/**
	 * @param {Element} node
	 * @param {INTRO | OUTRO | boolean} direction
	 * @param {'start' | 'end'} kind
	 * @returns {void}
	 */
	function dispatch(node, direction, kind) {
		node.dispatchEvent(custom_event(`${direction ? 'intro' : 'outro'}${kind}`));
	}

	const outroing = new Set();

	/**
	 * @type {Outro}
	 */
	let outros;

	/**
	 * @returns {void} */
	function group_outros() {
		outros = {
			r: 0,
			c: [],
			p: outros // parent group
		};
	}

	/**
	 * @returns {void} */
	function check_outros() {
		if (!outros.r) {
			run_all(outros.c);
		}
		outros = outros.p;
	}

	/**
	 * @param {import('./private.js').Fragment} block
	 * @param {0 | 1} [local]
	 * @returns {void}
	 */
	function transition_in(block, local) {
		if (block && block.i) {
			outroing.delete(block);
			block.i(local);
		}
	}

	/**
	 * @param {import('./private.js').Fragment} block
	 * @param {0 | 1} local
	 * @param {0 | 1} [detach]
	 * @param {() => void} [callback]
	 * @returns {void}
	 */
	function transition_out(block, local, detach, callback) {
		if (block && block.o) {
			if (outroing.has(block)) return;
			outroing.add(block);
			outros.c.push(() => {
				outroing.delete(block);
				if (callback) {
					if (detach) block.d(1);
					callback();
				}
			});
			block.o(local);
		} else if (callback) {
			callback();
		}
	}

	/**
	 * @type {import('../transition/public.js').TransitionConfig}
	 */
	const null_transition = { duration: 0 };

	/**
	 * @param {Element & ElementCSSInlineStyle} node
	 * @param {TransitionFn} fn
	 * @param {any} params
	 * @returns {{ start(): void; invalidate(): void; end(): void; }}
	 */
	function create_in_transition(node, fn, params) {
		/**
		 * @type {TransitionOptions} */
		const options = { direction: 'in' };
		let config = fn(node, params, options);
		let running = false;
		let animation_name;
		let task;
		let uid = 0;

		/**
		 * @returns {void} */
		function cleanup() {
			if (animation_name) delete_rule(node, animation_name);
		}

		/**
		 * @returns {void} */
		function go() {
			const {
				delay = 0,
				duration = 300,
				easing = identity,
				tick = noop,
				css
			} = config || null_transition;
			if (css) animation_name = create_rule(node, 0, 1, duration, delay, easing, css, uid++);
			tick(0, 1);
			const start_time = now() + delay;
			const end_time = start_time + duration;
			if (task) task.abort();
			running = true;
			add_render_callback(() => dispatch(node, true, 'start'));
			task = loop((now) => {
				if (running) {
					if (now >= end_time) {
						tick(1, 0);
						dispatch(node, true, 'end');
						cleanup();
						return (running = false);
					}
					if (now >= start_time) {
						const t = easing((now - start_time) / duration);
						tick(t, 1 - t);
					}
				}
				return running;
			});
		}
		let started = false;
		return {
			start() {
				if (started) return;
				started = true;
				delete_rule(node);
				if (is_function(config)) {
					config = config(options);
					wait().then(go);
				} else {
					go();
				}
			},
			invalidate() {
				started = false;
			},
			end() {
				if (running) {
					cleanup();
					running = false;
				}
			}
		};
	}

	/**
	 * @param {Element & ElementCSSInlineStyle} node
	 * @param {TransitionFn} fn
	 * @param {any} params
	 * @returns {{ end(reset: any): void; }}
	 */
	function create_out_transition(node, fn, params) {
		/** @type {TransitionOptions} */
		const options = { direction: 'out' };
		let config = fn(node, params, options);
		let running = true;
		let animation_name;
		const group = outros;
		group.r += 1;
		/** @type {boolean} */
		let original_inert_value;

		/**
		 * @returns {void} */
		function go() {
			const {
				delay = 0,
				duration = 300,
				easing = identity,
				tick = noop,
				css
			} = config || null_transition;

			if (css) animation_name = create_rule(node, 1, 0, duration, delay, easing, css);

			const start_time = now() + delay;
			const end_time = start_time + duration;
			add_render_callback(() => dispatch(node, false, 'start'));

			if ('inert' in node) {
				original_inert_value = /** @type {HTMLElement} */ (node).inert;
				node.inert = true;
			}

			loop((now) => {
				if (running) {
					if (now >= end_time) {
						tick(0, 1);
						dispatch(node, false, 'end');
						if (!--group.r) {
							// this will result in `end()` being called,
							// so we don't need to clean up here
							run_all(group.c);
						}
						return false;
					}
					if (now >= start_time) {
						const t = easing((now - start_time) / duration);
						tick(1 - t, t);
					}
				}
				return running;
			});
		}

		if (is_function(config)) {
			wait().then(() => {
				// @ts-ignore
				config = config(options);
				go();
			});
		} else {
			go();
		}

		return {
			end(reset) {
				if (reset && 'inert' in node) {
					node.inert = original_inert_value;
				}
				if (reset && config.tick) {
					config.tick(1, 0);
				}
				if (running) {
					if (animation_name) delete_rule(node, animation_name);
					running = false;
				}
			}
		};
	}

	/** @typedef {1} INTRO */
	/** @typedef {0} OUTRO */
	/** @typedef {{ direction: 'in' | 'out' | 'both' }} TransitionOptions */
	/** @typedef {(node: Element, params: any, options: TransitionOptions) => import('../transition/public.js').TransitionConfig} TransitionFn */

	/**
	 * @typedef {Object} Outro
	 * @property {number} r
	 * @property {Function[]} c
	 * @property {Object} p
	 */

	/**
	 * @typedef {Object} PendingProgram
	 * @property {number} start
	 * @property {INTRO|OUTRO} b
	 * @property {Outro} [group]
	 */

	/**
	 * @typedef {Object} Program
	 * @property {number} a
	 * @property {INTRO|OUTRO} b
	 * @property {1|-1} d
	 * @property {number} duration
	 * @property {number} start
	 * @property {number} end
	 * @property {Outro} [group]
	 */

	// general each functions:

	function ensure_array_like(array_like_or_iterator) {
		return array_like_or_iterator?.length !== undefined
			? array_like_or_iterator
			: Array.from(array_like_or_iterator);
	}

	/** @returns {{}} */
	function get_spread_update(levels, updates) {
		const update = {};
		const to_null_out = {};
		const accounted_for = { $$scope: 1 };
		let i = levels.length;
		while (i--) {
			const o = levels[i];
			const n = updates[i];
			if (n) {
				for (const key in o) {
					if (!(key in n)) to_null_out[key] = 1;
				}
				for (const key in n) {
					if (!accounted_for[key]) {
						update[key] = n[key];
						accounted_for[key] = 1;
					}
				}
				levels[i] = n;
			} else {
				for (const key in o) {
					accounted_for[key] = 1;
				}
			}
		}
		for (const key in to_null_out) {
			if (!(key in update)) update[key] = undefined;
		}
		return update;
	}

	/** regex of all html void element names */
	const void_element_names =
		/^(?:area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|source|track|wbr)$/;

	/**
	 * @param {string} name
	 * @returns {boolean}
	 */
	function is_void(name) {
		return void_element_names.test(name) || name.toLowerCase() === '!doctype';
	}

	/** @returns {void} */
	function create_component(block) {
		block && block.c();
	}

	/** @returns {void} */
	function mount_component(component, target, anchor) {
		const { fragment, after_update } = component.$$;
		fragment && fragment.m(target, anchor);
		// onMount happens before the initial afterUpdate
		add_render_callback(() => {
			const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
			// if the component was destroyed immediately
			// it will update the `$$.on_destroy` reference to `null`.
			// the destructured on_destroy may still reference to the old array
			if (component.$$.on_destroy) {
				component.$$.on_destroy.push(...new_on_destroy);
			} else {
				// Edge case - component was destroyed immediately,
				// most likely as a result of a binding initialising
				run_all(new_on_destroy);
			}
			component.$$.on_mount = [];
		});
		after_update.forEach(add_render_callback);
	}

	/** @returns {void} */
	function destroy_component(component, detaching) {
		const $$ = component.$$;
		if ($$.fragment !== null) {
			flush_render_callbacks($$.after_update);
			run_all($$.on_destroy);
			$$.fragment && $$.fragment.d(detaching);
			// TODO null out other refs, including component.$$ (but need to
			// preserve final state?)
			$$.on_destroy = $$.fragment = null;
			$$.ctx = [];
		}
	}

	/** @returns {void} */
	function make_dirty(component, i) {
		if (component.$$.dirty[0] === -1) {
			dirty_components.push(component);
			schedule_update();
			component.$$.dirty.fill(0);
		}
		component.$$.dirty[(i / 31) | 0] |= 1 << i % 31;
	}

	// TODO: Document the other params
	/**
	 * @param {SvelteComponent} component
	 * @param {import('./public.js').ComponentConstructorOptions} options
	 *
	 * @param {import('./utils.js')['not_equal']} not_equal Used to compare props and state values.
	 * @param {(target: Element | ShadowRoot) => void} [append_styles] Function that appends styles to the DOM when the component is first initialised.
	 * This will be the `add_css` function from the compiled component.
	 *
	 * @returns {void}
	 */
	function init(
		component,
		options,
		instance,
		create_fragment,
		not_equal,
		props,
		append_styles = null,
		dirty = [-1]
	) {
		const parent_component = current_component;
		set_current_component(component);
		/** @type {import('./private.js').T$$} */
		const $$ = (component.$$ = {
			fragment: null,
			ctx: [],
			// state
			props,
			update: noop,
			not_equal,
			bound: blank_object(),
			// lifecycle
			on_mount: [],
			on_destroy: [],
			on_disconnect: [],
			before_update: [],
			after_update: [],
			context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
			// everything else
			callbacks: blank_object(),
			dirty,
			skip_bound: false,
			root: options.target || parent_component.$$.root
		});
		append_styles && append_styles($$.root);
		let ready = false;
		$$.ctx = instance
			? instance(component, options.props || {}, (i, ret, ...rest) => {
					const value = rest.length ? rest[0] : ret;
					if ($$.ctx && not_equal($$.ctx[i], ($$.ctx[i] = value))) {
						if (!$$.skip_bound && $$.bound[i]) $$.bound[i](value);
						if (ready) make_dirty(component, i);
					}
					return ret;
			  })
			: [];
		$$.update();
		ready = true;
		run_all($$.before_update);
		// `false` as a special case of no DOM component
		$$.fragment = create_fragment ? create_fragment($$.ctx) : false;
		if (options.target) {
			if (options.hydrate) {
				// TODO: what is the correct type here?
				// @ts-expect-error
				const nodes = children(options.target);
				$$.fragment && $$.fragment.l(nodes);
				nodes.forEach(detach);
			} else {
				// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
				$$.fragment && $$.fragment.c();
			}
			if (options.intro) transition_in(component.$$.fragment);
			mount_component(component, options.target, options.anchor);
			flush();
		}
		set_current_component(parent_component);
	}

	/**
	 * Base class for Svelte components. Used when dev=false.
	 *
	 * @template {Record<string, any>} [Props=any]
	 * @template {Record<string, any>} [Events=any]
	 */
	class SvelteComponent {
		/**
		 * ### PRIVATE API
		 *
		 * Do not use, may change at any time
		 *
		 * @type {any}
		 */
		$$ = undefined;
		/**
		 * ### PRIVATE API
		 *
		 * Do not use, may change at any time
		 *
		 * @type {any}
		 */
		$$set = undefined;

		/** @returns {void} */
		$destroy() {
			destroy_component(this, 1);
			this.$destroy = noop;
		}

		/**
		 * @template {Extract<keyof Events, string>} K
		 * @param {K} type
		 * @param {((e: Events[K]) => void) | null | undefined} callback
		 * @returns {() => void}
		 */
		$on(type, callback) {
			if (!is_function(callback)) {
				return noop;
			}
			const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
			callbacks.push(callback);
			return () => {
				const index = callbacks.indexOf(callback);
				if (index !== -1) callbacks.splice(index, 1);
			};
		}

		/**
		 * @param {Partial<Props>} props
		 * @returns {void}
		 */
		$set(props) {
			if (this.$$set && !is_empty(props)) {
				this.$$.skip_bound = true;
				this.$$set(props);
				this.$$.skip_bound = false;
			}
		}
	}

	/**
	 * @typedef {Object} CustomElementPropDefinition
	 * @property {string} [attribute]
	 * @property {boolean} [reflect]
	 * @property {'String'|'Boolean'|'Number'|'Array'|'Object'} [type]
	 */

	// generated during release, do not modify

	/**
	 * The current version, as set in package.json.
	 *
	 * https://svelte.dev/docs/svelte-compiler#svelte-version
	 * @type {string}
	 */
	const VERSION = '4.2.17';
	const PUBLIC_VERSION = '4';

	/**
	 * @template T
	 * @param {string} type
	 * @param {T} [detail]
	 * @returns {void}
	 */
	function dispatch_dev(type, detail) {
		document.dispatchEvent(custom_event(type, { version: VERSION, ...detail }, { bubbles: true }));
	}

	/**
	 * @param {Node} target
	 * @param {Node} node
	 * @returns {void}
	 */
	function append_dev(target, node) {
		dispatch_dev('SvelteDOMInsert', { target, node });
		append(target, node);
	}

	/**
	 * @param {Node} target
	 * @param {Node} node
	 * @param {Node} [anchor]
	 * @returns {void}
	 */
	function insert_dev(target, node, anchor) {
		dispatch_dev('SvelteDOMInsert', { target, node, anchor });
		insert(target, node, anchor);
	}

	/**
	 * @param {Node} node
	 * @returns {void}
	 */
	function detach_dev(node) {
		dispatch_dev('SvelteDOMRemove', { node });
		detach(node);
	}

	/**
	 * @param {Node} node
	 * @param {string} event
	 * @param {EventListenerOrEventListenerObject} handler
	 * @param {boolean | AddEventListenerOptions | EventListenerOptions} [options]
	 * @param {boolean} [has_prevent_default]
	 * @param {boolean} [has_stop_propagation]
	 * @param {boolean} [has_stop_immediate_propagation]
	 * @returns {() => void}
	 */
	function listen_dev(
		node,
		event,
		handler,
		options,
		has_prevent_default,
		has_stop_propagation,
		has_stop_immediate_propagation
	) {
		const modifiers =
			options === true ? ['capture'] : options ? Array.from(Object.keys(options)) : [];
		if (has_prevent_default) modifiers.push('preventDefault');
		if (has_stop_propagation) modifiers.push('stopPropagation');
		if (has_stop_immediate_propagation) modifiers.push('stopImmediatePropagation');
		dispatch_dev('SvelteDOMAddEventListener', { node, event, handler, modifiers });
		const dispose = listen(node, event, handler, options);
		return () => {
			dispatch_dev('SvelteDOMRemoveEventListener', { node, event, handler, modifiers });
			dispose();
		};
	}

	/**
	 * @param {Element} node
	 * @param {string} attribute
	 * @param {string} [value]
	 * @returns {void}
	 */
	function attr_dev(node, attribute, value) {
		attr(node, attribute, value);
		if (value == null) dispatch_dev('SvelteDOMRemoveAttribute', { node, attribute });
		else dispatch_dev('SvelteDOMSetAttribute', { node, attribute, value });
	}

	/**
	 * @param {Element} node
	 * @param {string} property
	 * @param {any} [value]
	 * @returns {void}
	 */
	function prop_dev(node, property, value) {
		node[property] = value;
		dispatch_dev('SvelteDOMSetProperty', { node, property, value });
	}

	/**
	 * @param {Text} text
	 * @param {unknown} data
	 * @returns {void}
	 */
	function set_data_dev(text, data) {
		data = '' + data;
		if (text.data === data) return;
		dispatch_dev('SvelteDOMSetData', { node: text, data });
		text.data = /** @type {string} */ (data);
	}

	function ensure_array_like_dev(arg) {
		if (
			typeof arg !== 'string' &&
			!(arg && typeof arg === 'object' && 'length' in arg) &&
			!(typeof Symbol === 'function' && arg && Symbol.iterator in arg)
		) {
			throw new Error('{#each} only works with iterable values.');
		}
		return ensure_array_like(arg);
	}

	/**
	 * @returns {void} */
	function validate_slots(name, slot, keys) {
		for (const slot_key of Object.keys(slot)) {
			if (!~keys.indexOf(slot_key)) {
				console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
			}
		}
	}

	/**
	 * @param {unknown} tag
	 * @returns {void}
	 */
	function validate_dynamic_element(tag) {
		const is_string = typeof tag === 'string';
		if (tag && !is_string) {
			throw new Error('<svelte:element> expects "this" attribute to be a string.');
		}
	}

	/**
	 * @param {undefined | string} tag
	 * @returns {void}
	 */
	function validate_void_dynamic_element(tag) {
		if (tag && is_void(tag)) {
			console.warn(`<svelte:element this="${tag}"> is self-closing and cannot have content.`);
		}
	}

	/**
	 * Base class for Svelte components with some minor dev-enhancements. Used when dev=true.
	 *
	 * Can be used to create strongly typed Svelte components.
	 *
	 * #### Example:
	 *
	 * You have component library on npm called `component-library`, from which
	 * you export a component called `MyComponent`. For Svelte+TypeScript users,
	 * you want to provide typings. Therefore you create a `index.d.ts`:
	 * ```ts
	 * import { SvelteComponent } from "svelte";
	 * export class MyComponent extends SvelteComponent<{foo: string}> {}
	 * ```
	 * Typing this makes it possible for IDEs like VS Code with the Svelte extension
	 * to provide intellisense and to use the component like this in a Svelte file
	 * with TypeScript:
	 * ```svelte
	 * <script lang="ts">
	 * 	import { MyComponent } from "component-library";
	 * </script>
	 * <MyComponent foo={'bar'} />
	 * ```
	 * @template {Record<string, any>} [Props=any]
	 * @template {Record<string, any>} [Events=any]
	 * @template {Record<string, any>} [Slots=any]
	 * @extends {SvelteComponent<Props, Events>}
	 */
	class SvelteComponentDev extends SvelteComponent {
		/**
		 * For type checking capabilities only.
		 * Does not exist at runtime.
		 * ### DO NOT USE!
		 *
		 * @type {Props}
		 */
		$$prop_def;
		/**
		 * For type checking capabilities only.
		 * Does not exist at runtime.
		 * ### DO NOT USE!
		 *
		 * @type {Events}
		 */
		$$events_def;
		/**
		 * For type checking capabilities only.
		 * Does not exist at runtime.
		 * ### DO NOT USE!
		 *
		 * @type {Slots}
		 */
		$$slot_def;

		/** @param {import('./public.js').ComponentConstructorOptions<Props>} options */
		constructor(options) {
			if (!options || (!options.target && !options.$$inline)) {
				throw new Error("'target' is a required option");
			}
			super();
		}

		/** @returns {void} */
		$destroy() {
			super.$destroy();
			this.$destroy = () => {
				console.warn('Component was already destroyed'); // eslint-disable-line no-console
			};
		}

		/** @returns {void} */
		$capture_state() {}

		/** @returns {void} */
		$inject_state() {}
	}

	if (typeof window !== 'undefined')
		// @ts-ignore
		(window.__svelte || (window.__svelte = { v: new Set() })).v.add(PUBLIC_VERSION);

	/* src/components/Navbar.svelte generated by Svelte v4.2.17 */

	const { console: console_1$2 } = globals;
	const file$b = "src/components/Navbar.svelte";

	function create_fragment$b(ctx) {
		let nav;
		let ul;
		let li0;
		let button0;
		let t1;
		let li1;
		let button1;
		let t3;
		let li2;
		let button2;
		let mounted;
		let dispose;

		const block = {
			c: function create() {
				nav = element("nav");
				ul = element("ul");
				li0 = element("li");
				button0 = element("button");
				button0.textContent = "Home";
				t1 = space();
				li1 = element("li");
				button1 = element("button");
				button1.textContent = "About";
				t3 = space();
				li2 = element("li");
				button2 = element("button");
				button2.textContent = "Contact";
				attr_dev(button0, "class", "svelte-19f3ijy");
				toggle_class(button0, "selected", /*activeTab*/ ctx[0] === 'Home');
				add_location(button0, file$b, 19, 4, 312);
				attr_dev(li0, "class", "svelte-19f3ijy");
				add_location(li0, file$b, 18, 2, 303);
				attr_dev(button1, "class", "svelte-19f3ijy");
				toggle_class(button1, "selected", /*activeTab*/ ctx[0] === 'About');
				add_location(button1, file$b, 25, 4, 446);
				attr_dev(li1, "class", "svelte-19f3ijy");
				add_location(li1, file$b, 24, 2, 437);
				attr_dev(button2, "class", "svelte-19f3ijy");
				toggle_class(button2, "selected", /*activeTab*/ ctx[0] === 'Contact');
				add_location(button2, file$b, 31, 4, 583);
				attr_dev(li2, "class", "svelte-19f3ijy");
				add_location(li2, file$b, 30, 2, 574);
				attr_dev(ul, "class", "svelte-19f3ijy");
				add_location(ul, file$b, 17, 0, 296);
				attr_dev(nav, "class", "svelte-19f3ijy");
				add_location(nav, file$b, 16, 0, 290);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				insert_dev(target, nav, anchor);
				append_dev(nav, ul);
				append_dev(ul, li0);
				append_dev(li0, button0);
				append_dev(ul, t1);
				append_dev(ul, li1);
				append_dev(li1, button1);
				append_dev(ul, t3);
				append_dev(ul, li2);
				append_dev(li2, button2);

				if (!mounted) {
					dispose = [
						listen_dev(button0, "click", /*click_handler*/ ctx[2], false, false, false, false),
						listen_dev(button1, "click", /*click_handler_1*/ ctx[3], false, false, false, false),
						listen_dev(button2, "click", /*click_handler_2*/ ctx[4], false, false, false, false)
					];

					mounted = true;
				}
			},
			p: function update(ctx, [dirty]) {
				if (dirty & /*activeTab*/ 1) {
					toggle_class(button0, "selected", /*activeTab*/ ctx[0] === 'Home');
				}

				if (dirty & /*activeTab*/ 1) {
					toggle_class(button1, "selected", /*activeTab*/ ctx[0] === 'About');
				}

				if (dirty & /*activeTab*/ 1) {
					toggle_class(button2, "selected", /*activeTab*/ ctx[0] === 'Contact');
				}
			},
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(nav);
				}

				mounted = false;
				run_all(dispose);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$b.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$b($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('Navbar', slots, []);
		const dispatch = createEventDispatcher();
		let activeTab = 'Home';

		function setActiveTab(tab) {
			$$invalidate(0, activeTab = tab);
			console.log(activeTab);
			dispatch('tabChange', { tab });
		}

		console.log(activeTab);
		const writable_props = [];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1$2.warn(`<Navbar> was created with unknown prop '${key}'`);
		});

		const click_handler = () => setActiveTab('Home');
		const click_handler_1 = () => setActiveTab('About');
		const click_handler_2 = () => setActiveTab('Contact');

		$$self.$capture_state = () => ({
			createEventDispatcher,
			dispatch,
			activeTab,
			setActiveTab
		});

		$$self.$inject_state = $$props => {
			if ('activeTab' in $$props) $$invalidate(0, activeTab = $$props.activeTab);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		return [activeTab, setActiveTab, click_handler, click_handler_1, click_handler_2];
	}

	class Navbar extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$b, create_fragment$b, safe_not_equal, {});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "Navbar",
				options,
				id: create_fragment$b.name
			});
		}
	}

	/* src/components/About.svelte generated by Svelte v4.2.17 */

	const { console: console_1$1 } = globals;
	const file$a = "src/components/About.svelte";

	// (67:8) {#if subscribed}
	function create_if_block$6(ctx) {
		let p;

		const block = {
			c: function create() {
				p = element("p");
				p.textContent = "Thank you for subscribing!";
				attr_dev(p, "class", "success-message svelte-mbp4rq");
				add_location(p, file$a, 67, 10, 2785);
			},
			m: function mount(target, anchor) {
				insert_dev(target, p, anchor);
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(p);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block$6.name,
			type: "if",
			source: "(67:8) {#if subscribed}",
			ctx
		});

		return block;
	}

	function create_fragment$a(ctx) {
		let div6;
		let div5;
		let h1;
		let t1;
		let p0;
		let t3;
		let p1;
		let t5;
		let p2;
		let t7;
		let div0;
		let button0;
		let t9;
		let button1;
		let t11;
		let div4;
		let div1;
		let h20;
		let t13;
		let p3;
		let t15;
		let div3;
		let h21;
		let t17;
		let p4;
		let t19;
		let div2;
		let input;
		let t20;
		let button2;
		let t21_value = (/*subscribed*/ ctx[1] ? 'Subscribed!' : 'Subscribe') + "";
		let t21;
		let t22;
		let t23;
		let p5;
		let mounted;
		let dispose;
		let if_block = /*subscribed*/ ctx[1] && create_if_block$6(ctx);

		const block = {
			c: function create() {
				div6 = element("div");
				div5 = element("div");
				h1 = element("h1");
				h1.textContent = "What is this all about?";
				t1 = space();
				p0 = element("p");
				p0.textContent = "Are you ready for a future where AI outpaces human intelligence, where your kids' tech-savvy isn't just about mastering the latest app, but surviving in a world that looks more like The Matrix and Blade Runner had a mutant baby with the Terminator?";
				t3 = space();
				p1 = element("p");
				p1.textContent = "This book isn't just about understanding technology; it's about preparing you and your family for the rapid changes ahead.";
				t5 = space();
				p2 = element("p");
				p2.textContent = "What will you do when machines can think, feel, and even outsmart us? How will you protect your family in a world where the lines between human and machine are increasingly blurred? \"Surviving the Singularity\" provides the insights and strategies to help you navigate the cognitive dissonance ahead as you learn to survive AND thrive in this new era.";
				t7 = space();
				div0 = element("div");
				button0 = element("button");
				button0.textContent = "Read a Sample";
				t9 = space();
				button1 = element("button");
				button1.textContent = "Buy the Book";
				t11 = space();
				div4 = element("div");
				div1 = element("div");
				h20 = element("h2");
				h20.textContent = "Our Mission";
				t13 = space();
				p3 = element("p");
				p3.textContent = "Our mission is to help you understand the Singularity and its impact on our lives. Join our community of forward-thinkers, researchers, and innovators to navigate the challenges and opportunities of this rapidly changing world.";
				t15 = space();
				div3 = element("div");
				h21 = element("h2");
				h21.textContent = "Stay Updated";
				t17 = space();
				p4 = element("p");
				p4.textContent = "Subscribe to our newsletter for regular updates, insights, and exclusive content about the technological Singularity.";
				t19 = space();
				div2 = element("div");
				input = element("input");
				t20 = space();
				button2 = element("button");
				t21 = text(t21_value);
				t22 = space();
				if (if_block) if_block.c();
				t23 = space();
				p5 = element("p");
				p5.textContent = "\"Surviving the Singularity\" is sponsored by AIECO, a humanity-focused organization.";
				attr_dev(h1, "class", "title svelte-mbp4rq");
				add_location(h1, file$a, 19, 4, 391);
				attr_dev(p0, "class", "description svelte-mbp4rq");
				add_location(p0, file$a, 20, 4, 442);
				attr_dev(p1, "class", "description svelte-mbp4rq");
				add_location(p1, file$a, 23, 4, 734);
				attr_dev(p2, "class", "description svelte-mbp4rq");
				add_location(p2, file$a, 26, 4, 900);
				attr_dev(button0, "class", "sample-button svelte-mbp4rq");
				add_location(button0, file$a, 31, 6, 1328);
				attr_dev(button1, "class", "buy-button svelte-mbp4rq");
				add_location(button1, file$a, 34, 6, 1542);
				attr_dev(div0, "class", "button-group svelte-mbp4rq");
				add_location(div0, file$a, 30, 4, 1295);
				attr_dev(h20, "class", "section-title svelte-mbp4rq");
				add_location(h20, file$a, 41, 8, 1717);
				attr_dev(p3, "class", "section-description svelte-mbp4rq");
				add_location(p3, file$a, 42, 8, 1768);
				attr_dev(div1, "class", "section svelte-mbp4rq");
				add_location(div1, file$a, 40, 6, 1687);
				attr_dev(h21, "class", "section-title svelte-mbp4rq");
				add_location(h21, file$a, 48, 8, 2101);
				attr_dev(p4, "class", "section-description svelte-mbp4rq");
				add_location(p4, file$a, 49, 8, 2153);
				attr_dev(input, "type", "email");
				attr_dev(input, "placeholder", "Enter your email");
				attr_dev(input, "class", "newsletter-input svelte-mbp4rq");
				add_location(input, file$a, 53, 10, 2374);
				attr_dev(button2, "class", "newsletter-button svelte-mbp4rq");
				button2.disabled = /*subscribed*/ ctx[1];
				add_location(button2, file$a, 59, 10, 2540);
				attr_dev(div2, "class", "newsletter-form svelte-mbp4rq");
				add_location(div2, file$a, 52, 8, 2334);
				attr_dev(div3, "class", "section svelte-mbp4rq");
				add_location(div3, file$a, 47, 6, 2071);
				attr_dev(p5, "class", "section-description svelte-mbp4rq");
				add_location(p5, file$a, 70, 8, 2878);
				attr_dev(div4, "class", "additional-content svelte-mbp4rq");
				add_location(div4, file$a, 39, 4, 1648);
				attr_dev(div5, "class", "content svelte-mbp4rq");
				add_location(div5, file$a, 18, 2, 365);
				attr_dev(div6, "class", "container svelte-mbp4rq");
				add_location(div6, file$a, 17, 0, 339);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				insert_dev(target, div6, anchor);
				append_dev(div6, div5);
				append_dev(div5, h1);
				append_dev(div5, t1);
				append_dev(div5, p0);
				append_dev(div5, t3);
				append_dev(div5, p1);
				append_dev(div5, t5);
				append_dev(div5, p2);
				append_dev(div5, t7);
				append_dev(div5, div0);
				append_dev(div0, button0);
				append_dev(div0, t9);
				append_dev(div0, button1);
				append_dev(div5, t11);
				append_dev(div5, div4);
				append_dev(div4, div1);
				append_dev(div1, h20);
				append_dev(div1, t13);
				append_dev(div1, p3);
				append_dev(div4, t15);
				append_dev(div4, div3);
				append_dev(div3, h21);
				append_dev(div3, t17);
				append_dev(div3, p4);
				append_dev(div3, t19);
				append_dev(div3, div2);
				append_dev(div2, input);
				set_input_value(input, /*email*/ ctx[0]);
				append_dev(div2, t20);
				append_dev(div2, button2);
				append_dev(button2, t21);
				append_dev(div3, t22);
				if (if_block) if_block.m(div3, null);
				append_dev(div4, t23);
				append_dev(div4, p5);

				if (!mounted) {
					dispose = [
						listen_dev(button0, "click", /*click_handler*/ ctx[3], false, false, false, false),
						listen_dev(button1, "click", handleBuyBook, false, false, false, false),
						listen_dev(input, "input", /*input_input_handler*/ ctx[4]),
						listen_dev(button2, "click", /*handleSubscribe*/ ctx[2], false, false, false, false)
					];

					mounted = true;
				}
			},
			p: function update(ctx, [dirty]) {
				if (dirty & /*email*/ 1 && input.value !== /*email*/ ctx[0]) {
					set_input_value(input, /*email*/ ctx[0]);
				}

				if (dirty & /*subscribed*/ 2 && t21_value !== (t21_value = (/*subscribed*/ ctx[1] ? 'Subscribed!' : 'Subscribe') + "")) set_data_dev(t21, t21_value);

				if (dirty & /*subscribed*/ 2) {
					prop_dev(button2, "disabled", /*subscribed*/ ctx[1]);
				}

				if (/*subscribed*/ ctx[1]) {
					if (if_block) ; else {
						if_block = create_if_block$6(ctx);
						if_block.c();
						if_block.m(div3, null);
					}
				} else if (if_block) {
					if_block.d(1);
					if_block = null;
				}
			},
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div6);
				}

				if (if_block) if_block.d();
				mounted = false;
				run_all(dispose);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$a.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function handleBuyBook() {
		alert("The book is still under development and will be available in November 2023.");
	}

	function instance$a($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('About', slots, []);
		let email = '';
		let subscribed = false;

		function handleSubscribe() {
			if (email) {
				console.log(`New subscription: ${email}`);
				$$invalidate(1, subscribed = true);
				$$invalidate(0, email = '');
			}
		}

		const writable_props = [];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1$1.warn(`<About> was created with unknown prop '${key}'`);
		});

		const click_handler = () => window.open('https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit?usp=sharing', '_blank');

		function input_input_handler() {
			email = this.value;
			$$invalidate(0, email);
		}

		$$self.$capture_state = () => ({
			email,
			subscribed,
			handleSubscribe,
			handleBuyBook
		});

		$$self.$inject_state = $$props => {
			if ('email' in $$props) $$invalidate(0, email = $$props.email);
			if ('subscribed' in $$props) $$invalidate(1, subscribed = $$props.subscribed);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		return [email, subscribed, handleSubscribe, click_handler, input_input_handler];
	}

	class About extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$a, create_fragment$a, safe_not_equal, {});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "About",
				options,
				id: create_fragment$a.name
			});
		}
	}

	/* src/components/Contact.svelte generated by Svelte v4.2.17 */
	const file$9 = "src/components/Contact.svelte";

	function create_fragment$9(ctx) {
		let div5;
		let div4;
		let h1;
		let t1;
		let form;
		let div0;
		let label0;
		let t3;
		let input0;
		let t4;
		let div1;
		let label1;
		let t6;
		let input1;
		let t7;
		let div2;
		let label2;
		let t9;
		let textarea;
		let t10;
		let div3;
		let button;
		let mounted;
		let dispose;

		const block = {
			c: function create() {
				div5 = element("div");
				div4 = element("div");
				h1 = element("h1");
				h1.textContent = "Contact Us";
				t1 = space();
				form = element("form");
				div0 = element("div");
				label0 = element("label");
				label0.textContent = "Your Name";
				t3 = space();
				input0 = element("input");
				t4 = space();
				div1 = element("div");
				label1 = element("label");
				label1.textContent = "Your Email";
				t6 = space();
				input1 = element("input");
				t7 = space();
				div2 = element("div");
				label2 = element("label");
				label2.textContent = "Message";
				t9 = space();
				textarea = element("textarea");
				t10 = space();
				div3 = element("div");
				button = element("button");
				button.textContent = "Send Message";
				attr_dev(h1, "class", "form-title svelte-a8x9g3");
				add_location(h1, file$9, 10, 8, 239);
				attr_dev(label0, "for", "name");
				attr_dev(label0, "class", "svelte-a8x9g3");
				add_location(label0, file$9, 13, 16, 386);
				attr_dev(input0, "type", "text");
				attr_dev(input0, "id", "name");
				attr_dev(input0, "name", "name");
				input0.required = true;
				attr_dev(input0, "class", "svelte-a8x9g3");
				add_location(input0, file$9, 14, 16, 438);
				attr_dev(div0, "class", "form-group svelte-a8x9g3");
				add_location(div0, file$9, 12, 12, 345);
				attr_dev(label1, "for", "email");
				attr_dev(label1, "class", "svelte-a8x9g3");
				add_location(label1, file$9, 17, 16, 561);
				attr_dev(input1, "type", "email");
				attr_dev(input1, "id", "email");
				attr_dev(input1, "name", "email");
				input1.required = true;
				attr_dev(input1, "class", "svelte-a8x9g3");
				add_location(input1, file$9, 18, 16, 615);
				attr_dev(div1, "class", "form-group svelte-a8x9g3");
				add_location(div1, file$9, 16, 12, 520);
				attr_dev(label2, "for", "message");
				attr_dev(label2, "class", "svelte-a8x9g3");
				add_location(label2, file$9, 21, 16, 741);
				attr_dev(textarea, "id", "message");
				attr_dev(textarea, "name", "message");
				attr_dev(textarea, "rows", "4");
				textarea.required = true;
				attr_dev(textarea, "class", "svelte-a8x9g3");
				add_location(textarea, file$9, 22, 16, 794);
				attr_dev(div2, "class", "form-group svelte-a8x9g3");
				add_location(div2, file$9, 20, 12, 700);
				attr_dev(button, "type", "submit");
				attr_dev(button, "class", "submit-btn svelte-a8x9g3");
				add_location(button, file$9, 25, 16, 946);
				attr_dev(div3, "class", "form-group text-center svelte-a8x9g3");
				add_location(div3, file$9, 24, 12, 893);
				add_location(form, file$9, 11, 8, 286);
				attr_dev(div4, "class", "form-wrapper svelte-a8x9g3");
				add_location(div4, file$9, 9, 4, 204);
				attr_dev(div5, "class", "container svelte-a8x9g3");
				add_location(div5, file$9, 8, 0, 176);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				insert_dev(target, div5, anchor);
				append_dev(div5, div4);
				append_dev(div4, h1);
				append_dev(div4, t1);
				append_dev(div4, form);
				append_dev(form, div0);
				append_dev(div0, label0);
				append_dev(div0, t3);
				append_dev(div0, input0);
				append_dev(form, t4);
				append_dev(form, div1);
				append_dev(div1, label1);
				append_dev(div1, t6);
				append_dev(div1, input1);
				append_dev(form, t7);
				append_dev(form, div2);
				append_dev(div2, label2);
				append_dev(div2, t9);
				append_dev(div2, textarea);
				append_dev(form, t10);
				append_dev(form, div3);
				append_dev(div3, button);

				if (!mounted) {
					dispose = listen_dev(form, "submit", prevent_default(handleSubmit), false, true, false, false);
					mounted = true;
				}
			},
			p: noop,
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div5);
				}

				mounted = false;
				dispose();
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$9.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function handleSubmit() {
		alert('Submission received');

		// Prevent form from actually submitting to a page.
		return false;
	}

	function instance$9($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('Contact', slots, []);
		const writable_props = [];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Contact> was created with unknown prop '${key}'`);
		});

		$$self.$capture_state = () => ({ handleSubmit });
		return [];
	}

	class Contact extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$9, create_fragment$9, safe_not_equal, {});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "Contact",
				options,
				id: create_fragment$9.name
			});
		}
	}

	const subscriber_queue = [];

	/**
	 * Creates a `Readable` store that allows reading by subscription.
	 *
	 * https://svelte.dev/docs/svelte-store#readable
	 * @template T
	 * @param {T} [value] initial value
	 * @param {import('./public.js').StartStopNotifier<T>} [start]
	 * @returns {import('./public.js').Readable<T>}
	 */
	function readable(value, start) {
		return {
			subscribe: writable(value, start).subscribe
		};
	}

	/**
	 * Create a `Writable` store that allows both updating and reading by subscription.
	 *
	 * https://svelte.dev/docs/svelte-store#writable
	 * @template T
	 * @param {T} [value] initial value
	 * @param {import('./public.js').StartStopNotifier<T>} [start]
	 * @returns {import('./public.js').Writable<T>}
	 */
	function writable(value, start = noop) {
		/** @type {import('./public.js').Unsubscriber} */
		let stop;
		/** @type {Set<import('./private.js').SubscribeInvalidateTuple<T>>} */
		const subscribers = new Set();
		/** @param {T} new_value
		 * @returns {void}
		 */
		function set(new_value) {
			if (safe_not_equal(value, new_value)) {
				value = new_value;
				if (stop) {
					// store is ready
					const run_queue = !subscriber_queue.length;
					for (const subscriber of subscribers) {
						subscriber[1]();
						subscriber_queue.push(subscriber, value);
					}
					if (run_queue) {
						for (let i = 0; i < subscriber_queue.length; i += 2) {
							subscriber_queue[i][0](subscriber_queue[i + 1]);
						}
						subscriber_queue.length = 0;
					}
				}
			}
		}

		/**
		 * @param {import('./public.js').Updater<T>} fn
		 * @returns {void}
		 */
		function update(fn) {
			set(fn(value));
		}

		/**
		 * @param {import('./public.js').Subscriber<T>} run
		 * @param {import('./private.js').Invalidator<T>} [invalidate]
		 * @returns {import('./public.js').Unsubscriber}
		 */
		function subscribe(run, invalidate = noop) {
			/** @type {import('./private.js').SubscribeInvalidateTuple<T>} */
			const subscriber = [run, invalidate];
			subscribers.add(subscriber);
			if (subscribers.size === 1) {
				stop = start(set, update) || noop;
			}
			run(value);
			return () => {
				subscribers.delete(subscriber);
				if (subscribers.size === 0 && stop) {
					stop();
					stop = null;
				}
			};
		}
		return { set, update, subscribe };
	}

	/**
	 * Derived value store by synchronizing one or more readable stores and
	 * applying an aggregation function over its input values.
	 *
	 * https://svelte.dev/docs/svelte-store#derived
	 * @template {import('./private.js').Stores} S
	 * @template T
	 * @overload
	 * @param {S} stores - input stores
	 * @param {(values: import('./private.js').StoresValues<S>, set: (value: T) => void, update: (fn: import('./public.js').Updater<T>) => void) => import('./public.js').Unsubscriber | void} fn - function callback that aggregates the values
	 * @param {T} [initial_value] - initial value
	 * @returns {import('./public.js').Readable<T>}
	 */

	/**
	 * Derived value store by synchronizing one or more readable stores and
	 * applying an aggregation function over its input values.
	 *
	 * https://svelte.dev/docs/svelte-store#derived
	 * @template {import('./private.js').Stores} S
	 * @template T
	 * @overload
	 * @param {S} stores - input stores
	 * @param {(values: import('./private.js').StoresValues<S>) => T} fn - function callback that aggregates the values
	 * @param {T} [initial_value] - initial value
	 * @returns {import('./public.js').Readable<T>}
	 */

	/**
	 * @template {import('./private.js').Stores} S
	 * @template T
	 * @param {S} stores
	 * @param {Function} fn
	 * @param {T} [initial_value]
	 * @returns {import('./public.js').Readable<T>}
	 */
	function derived(stores, fn, initial_value) {
		const single = !Array.isArray(stores);
		/** @type {Array<import('./public.js').Readable<any>>} */
		const stores_array = single ? [stores] : stores;
		if (!stores_array.every(Boolean)) {
			throw new Error('derived() expects stores as input, got a falsy value');
		}
		const auto = fn.length < 2;
		return readable(initial_value, (set, update) => {
			let started = false;
			const values = [];
			let pending = 0;
			let cleanup = noop;
			const sync = () => {
				if (pending) {
					return;
				}
				cleanup();
				const result = fn(single ? values[0] : values, set, update);
				if (auto) {
					set(result);
				} else {
					cleanup = is_function(result) ? result : noop;
				}
			};
			const unsubscribers = stores_array.map((store, i) =>
				subscribe(
					store,
					(value) => {
						values[i] = value;
						pending &= ~(1 << i);
						if (started) {
							sync();
						}
					},
					() => {
						pending |= 1 << i;
					}
				)
			);
			started = true;
			sync();
			return function stop() {
				run_all(unsubscribers);
				cleanup();
				// We need to set this to false because callbacks can still happen despite having unsubscribed:
				// Callbacks might already be placed in the queue which doesn't know it should no longer
				// invoke this derived store.
				started = false;
			};
		});
	}

	const CLASS_PART_SEPARATOR = '-';
	function createClassUtils(config) {
	  const classMap = createClassMap(config);
	  const {
	    conflictingClassGroups,
	    conflictingClassGroupModifiers
	  } = config;
	  function getClassGroupId(className) {
	    const classParts = className.split(CLASS_PART_SEPARATOR);
	    // Classes like `-inset-1` produce an empty string as first classPart. We assume that classes for negative values are used correctly and remove it from classParts.
	    if (classParts[0] === '' && classParts.length !== 1) {
	      classParts.shift();
	    }
	    return getGroupRecursive(classParts, classMap) || getGroupIdForArbitraryProperty(className);
	  }
	  function getConflictingClassGroupIds(classGroupId, hasPostfixModifier) {
	    const conflicts = conflictingClassGroups[classGroupId] || [];
	    if (hasPostfixModifier && conflictingClassGroupModifiers[classGroupId]) {
	      return [...conflicts, ...conflictingClassGroupModifiers[classGroupId]];
	    }
	    return conflicts;
	  }
	  return {
	    getClassGroupId,
	    getConflictingClassGroupIds
	  };
	}
	function getGroupRecursive(classParts, classPartObject) {
	  if (classParts.length === 0) {
	    return classPartObject.classGroupId;
	  }
	  const currentClassPart = classParts[0];
	  const nextClassPartObject = classPartObject.nextPart.get(currentClassPart);
	  const classGroupFromNextClassPart = nextClassPartObject ? getGroupRecursive(classParts.slice(1), nextClassPartObject) : undefined;
	  if (classGroupFromNextClassPart) {
	    return classGroupFromNextClassPart;
	  }
	  if (classPartObject.validators.length === 0) {
	    return undefined;
	  }
	  const classRest = classParts.join(CLASS_PART_SEPARATOR);
	  return classPartObject.validators.find(({
	    validator
	  }) => validator(classRest))?.classGroupId;
	}
	const arbitraryPropertyRegex = /^\[(.+)\]$/;
	function getGroupIdForArbitraryProperty(className) {
	  if (arbitraryPropertyRegex.test(className)) {
	    const arbitraryPropertyClassName = arbitraryPropertyRegex.exec(className)[1];
	    const property = arbitraryPropertyClassName?.substring(0, arbitraryPropertyClassName.indexOf(':'));
	    if (property) {
	      // I use two dots here because one dot is used as prefix for class groups in plugins
	      return 'arbitrary..' + property;
	    }
	  }
	}
	/**
	 * Exported for testing only
	 */
	function createClassMap(config) {
	  const {
	    theme,
	    prefix
	  } = config;
	  const classMap = {
	    nextPart: new Map(),
	    validators: []
	  };
	  const prefixedClassGroupEntries = getPrefixedClassGroupEntries(Object.entries(config.classGroups), prefix);
	  prefixedClassGroupEntries.forEach(([classGroupId, classGroup]) => {
	    processClassesRecursively(classGroup, classMap, classGroupId, theme);
	  });
	  return classMap;
	}
	function processClassesRecursively(classGroup, classPartObject, classGroupId, theme) {
	  classGroup.forEach(classDefinition => {
	    if (typeof classDefinition === 'string') {
	      const classPartObjectToEdit = classDefinition === '' ? classPartObject : getPart(classPartObject, classDefinition);
	      classPartObjectToEdit.classGroupId = classGroupId;
	      return;
	    }
	    if (typeof classDefinition === 'function') {
	      if (isThemeGetter(classDefinition)) {
	        processClassesRecursively(classDefinition(theme), classPartObject, classGroupId, theme);
	        return;
	      }
	      classPartObject.validators.push({
	        validator: classDefinition,
	        classGroupId
	      });
	      return;
	    }
	    Object.entries(classDefinition).forEach(([key, classGroup]) => {
	      processClassesRecursively(classGroup, getPart(classPartObject, key), classGroupId, theme);
	    });
	  });
	}
	function getPart(classPartObject, path) {
	  let currentClassPartObject = classPartObject;
	  path.split(CLASS_PART_SEPARATOR).forEach(pathPart => {
	    if (!currentClassPartObject.nextPart.has(pathPart)) {
	      currentClassPartObject.nextPart.set(pathPart, {
	        nextPart: new Map(),
	        validators: []
	      });
	    }
	    currentClassPartObject = currentClassPartObject.nextPart.get(pathPart);
	  });
	  return currentClassPartObject;
	}
	function isThemeGetter(func) {
	  return func.isThemeGetter;
	}
	function getPrefixedClassGroupEntries(classGroupEntries, prefix) {
	  if (!prefix) {
	    return classGroupEntries;
	  }
	  return classGroupEntries.map(([classGroupId, classGroup]) => {
	    const prefixedClassGroup = classGroup.map(classDefinition => {
	      if (typeof classDefinition === 'string') {
	        return prefix + classDefinition;
	      }
	      if (typeof classDefinition === 'object') {
	        return Object.fromEntries(Object.entries(classDefinition).map(([key, value]) => [prefix + key, value]));
	      }
	      return classDefinition;
	    });
	    return [classGroupId, prefixedClassGroup];
	  });
	}

	// LRU cache inspired from hashlru (https://github.com/dominictarr/hashlru/blob/v1.0.4/index.js) but object replaced with Map to improve performance
	function createLruCache(maxCacheSize) {
	  if (maxCacheSize < 1) {
	    return {
	      get: () => undefined,
	      set: () => {}
	    };
	  }
	  let cacheSize = 0;
	  let cache = new Map();
	  let previousCache = new Map();
	  function update(key, value) {
	    cache.set(key, value);
	    cacheSize++;
	    if (cacheSize > maxCacheSize) {
	      cacheSize = 0;
	      previousCache = cache;
	      cache = new Map();
	    }
	  }
	  return {
	    get(key) {
	      let value = cache.get(key);
	      if (value !== undefined) {
	        return value;
	      }
	      if ((value = previousCache.get(key)) !== undefined) {
	        update(key, value);
	        return value;
	      }
	    },
	    set(key, value) {
	      if (cache.has(key)) {
	        cache.set(key, value);
	      } else {
	        update(key, value);
	      }
	    }
	  };
	}
	const IMPORTANT_MODIFIER = '!';
	function createSplitModifiers(config) {
	  const separator = config.separator;
	  const isSeparatorSingleCharacter = separator.length === 1;
	  const firstSeparatorCharacter = separator[0];
	  const separatorLength = separator.length;
	  // splitModifiers inspired by https://github.com/tailwindlabs/tailwindcss/blob/v3.2.2/src/util/splitAtTopLevelOnly.js
	  return function splitModifiers(className) {
	    const modifiers = [];
	    let bracketDepth = 0;
	    let modifierStart = 0;
	    let postfixModifierPosition;
	    for (let index = 0; index < className.length; index++) {
	      let currentCharacter = className[index];
	      if (bracketDepth === 0) {
	        if (currentCharacter === firstSeparatorCharacter && (isSeparatorSingleCharacter || className.slice(index, index + separatorLength) === separator)) {
	          modifiers.push(className.slice(modifierStart, index));
	          modifierStart = index + separatorLength;
	          continue;
	        }
	        if (currentCharacter === '/') {
	          postfixModifierPosition = index;
	          continue;
	        }
	      }
	      if (currentCharacter === '[') {
	        bracketDepth++;
	      } else if (currentCharacter === ']') {
	        bracketDepth--;
	      }
	    }
	    const baseClassNameWithImportantModifier = modifiers.length === 0 ? className : className.substring(modifierStart);
	    const hasImportantModifier = baseClassNameWithImportantModifier.startsWith(IMPORTANT_MODIFIER);
	    const baseClassName = hasImportantModifier ? baseClassNameWithImportantModifier.substring(1) : baseClassNameWithImportantModifier;
	    const maybePostfixModifierPosition = postfixModifierPosition && postfixModifierPosition > modifierStart ? postfixModifierPosition - modifierStart : undefined;
	    return {
	      modifiers,
	      hasImportantModifier,
	      baseClassName,
	      maybePostfixModifierPosition
	    };
	  };
	}
	/**
	 * Sorts modifiers according to following schema:
	 * - Predefined modifiers are sorted alphabetically
	 * - When an arbitrary variant appears, it must be preserved which modifiers are before and after it
	 */
	function sortModifiers(modifiers) {
	  if (modifiers.length <= 1) {
	    return modifiers;
	  }
	  const sortedModifiers = [];
	  let unsortedModifiers = [];
	  modifiers.forEach(modifier => {
	    const isArbitraryVariant = modifier[0] === '[';
	    if (isArbitraryVariant) {
	      sortedModifiers.push(...unsortedModifiers.sort(), modifier);
	      unsortedModifiers = [];
	    } else {
	      unsortedModifiers.push(modifier);
	    }
	  });
	  sortedModifiers.push(...unsortedModifiers.sort());
	  return sortedModifiers;
	}
	function createConfigUtils(config) {
	  return {
	    cache: createLruCache(config.cacheSize),
	    splitModifiers: createSplitModifiers(config),
	    ...createClassUtils(config)
	  };
	}
	const SPLIT_CLASSES_REGEX = /\s+/;
	function mergeClassList(classList, configUtils) {
	  const {
	    splitModifiers,
	    getClassGroupId,
	    getConflictingClassGroupIds
	  } = configUtils;
	  /**
	   * Set of classGroupIds in following format:
	   * `{importantModifier}{variantModifiers}{classGroupId}`
	   * @example 'float'
	   * @example 'hover:focus:bg-color'
	   * @example 'md:!pr'
	   */
	  const classGroupsInConflict = new Set();
	  return classList.trim().split(SPLIT_CLASSES_REGEX).map(originalClassName => {
	    const {
	      modifiers,
	      hasImportantModifier,
	      baseClassName,
	      maybePostfixModifierPosition
	    } = splitModifiers(originalClassName);
	    let classGroupId = getClassGroupId(maybePostfixModifierPosition ? baseClassName.substring(0, maybePostfixModifierPosition) : baseClassName);
	    let hasPostfixModifier = Boolean(maybePostfixModifierPosition);
	    if (!classGroupId) {
	      if (!maybePostfixModifierPosition) {
	        return {
	          isTailwindClass: false,
	          originalClassName
	        };
	      }
	      classGroupId = getClassGroupId(baseClassName);
	      if (!classGroupId) {
	        return {
	          isTailwindClass: false,
	          originalClassName
	        };
	      }
	      hasPostfixModifier = false;
	    }
	    const variantModifier = sortModifiers(modifiers).join(':');
	    const modifierId = hasImportantModifier ? variantModifier + IMPORTANT_MODIFIER : variantModifier;
	    return {
	      isTailwindClass: true,
	      modifierId,
	      classGroupId,
	      originalClassName,
	      hasPostfixModifier
	    };
	  }).reverse()
	  // Last class in conflict wins, so we need to filter conflicting classes in reverse order.
	  .filter(parsed => {
	    if (!parsed.isTailwindClass) {
	      return true;
	    }
	    const {
	      modifierId,
	      classGroupId,
	      hasPostfixModifier
	    } = parsed;
	    const classId = modifierId + classGroupId;
	    if (classGroupsInConflict.has(classId)) {
	      return false;
	    }
	    classGroupsInConflict.add(classId);
	    getConflictingClassGroupIds(classGroupId, hasPostfixModifier).forEach(group => classGroupsInConflict.add(modifierId + group));
	    return true;
	  }).reverse().map(parsed => parsed.originalClassName).join(' ');
	}

	/**
	 * The code in this file is copied from https://github.com/lukeed/clsx and modified to suit the needs of tailwind-merge better.
	 *
	 * Specifically:
	 * - Runtime code from https://github.com/lukeed/clsx/blob/v1.2.1/src/index.js
	 * - TypeScript types from https://github.com/lukeed/clsx/blob/v1.2.1/clsx.d.ts
	 *
	 * Original code has MIT license: Copyright (c) Luke Edwards <luke.edwards05@gmail.com> (lukeed.com)
	 */
	function twJoin() {
	  let index = 0;
	  let argument;
	  let resolvedValue;
	  let string = '';
	  while (index < arguments.length) {
	    if (argument = arguments[index++]) {
	      if (resolvedValue = toValue(argument)) {
	        string && (string += ' ');
	        string += resolvedValue;
	      }
	    }
	  }
	  return string;
	}
	function toValue(mix) {
	  if (typeof mix === 'string') {
	    return mix;
	  }
	  let resolvedValue;
	  let string = '';
	  for (let k = 0; k < mix.length; k++) {
	    if (mix[k]) {
	      if (resolvedValue = toValue(mix[k])) {
	        string && (string += ' ');
	        string += resolvedValue;
	      }
	    }
	  }
	  return string;
	}
	function createTailwindMerge(createConfigFirst, ...createConfigRest) {
	  let configUtils;
	  let cacheGet;
	  let cacheSet;
	  let functionToCall = initTailwindMerge;
	  function initTailwindMerge(classList) {
	    const config = createConfigRest.reduce((previousConfig, createConfigCurrent) => createConfigCurrent(previousConfig), createConfigFirst());
	    configUtils = createConfigUtils(config);
	    cacheGet = configUtils.cache.get;
	    cacheSet = configUtils.cache.set;
	    functionToCall = tailwindMerge;
	    return tailwindMerge(classList);
	  }
	  function tailwindMerge(classList) {
	    const cachedResult = cacheGet(classList);
	    if (cachedResult) {
	      return cachedResult;
	    }
	    const result = mergeClassList(classList, configUtils);
	    cacheSet(classList, result);
	    return result;
	  }
	  return function callTailwindMerge() {
	    return functionToCall(twJoin.apply(null, arguments));
	  };
	}
	function fromTheme(key) {
	  const themeGetter = theme => theme[key] || [];
	  themeGetter.isThemeGetter = true;
	  return themeGetter;
	}
	const arbitraryValueRegex = /^\[(?:([a-z-]+):)?(.+)\]$/i;
	const fractionRegex = /^\d+\/\d+$/;
	const stringLengths = /*#__PURE__*/new Set(['px', 'full', 'screen']);
	const tshirtUnitRegex = /^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$/;
	const lengthUnitRegex = /\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)|^0$/;
	const colorFunctionRegex = /^(rgba?|hsla?|hwb|(ok)?(lab|lch))\(.+\)$/;
	// Shadow always begins with x and y offset separated by underscore optionally prepended by inset
	const shadowRegex = /^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)/;
	const imageRegex = /^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$/;
	function isLength(value) {
	  return isNumber(value) || stringLengths.has(value) || fractionRegex.test(value);
	}
	function isArbitraryLength(value) {
	  return getIsArbitraryValue(value, 'length', isLengthOnly);
	}
	function isNumber(value) {
	  return Boolean(value) && !Number.isNaN(Number(value));
	}
	function isArbitraryNumber(value) {
	  return getIsArbitraryValue(value, 'number', isNumber);
	}
	function isInteger(value) {
	  return Boolean(value) && Number.isInteger(Number(value));
	}
	function isPercent(value) {
	  return value.endsWith('%') && isNumber(value.slice(0, -1));
	}
	function isArbitraryValue(value) {
	  return arbitraryValueRegex.test(value);
	}
	function isTshirtSize(value) {
	  return tshirtUnitRegex.test(value);
	}
	const sizeLabels = /*#__PURE__*/new Set(['length', 'size', 'percentage']);
	function isArbitrarySize(value) {
	  return getIsArbitraryValue(value, sizeLabels, isNever);
	}
	function isArbitraryPosition(value) {
	  return getIsArbitraryValue(value, 'position', isNever);
	}
	const imageLabels = /*#__PURE__*/new Set(['image', 'url']);
	function isArbitraryImage(value) {
	  return getIsArbitraryValue(value, imageLabels, isImage);
	}
	function isArbitraryShadow(value) {
	  return getIsArbitraryValue(value, '', isShadow);
	}
	function isAny() {
	  return true;
	}
	function getIsArbitraryValue(value, label, testValue) {
	  const result = arbitraryValueRegex.exec(value);
	  if (result) {
	    if (result[1]) {
	      return typeof label === 'string' ? result[1] === label : label.has(result[1]);
	    }
	    return testValue(result[2]);
	  }
	  return false;
	}
	function isLengthOnly(value) {
	  // `colorFunctionRegex` check is necessary because color functions can have percentages in them which which would be incorrectly classified as lengths.
	  // For example, `hsl(0 0% 0%)` would be classified as a length without this check.
	  // I could also use lookbehind assertion in `lengthUnitRegex` but that isn't supported widely enough.
	  return lengthUnitRegex.test(value) && !colorFunctionRegex.test(value);
	}
	function isNever() {
	  return false;
	}
	function isShadow(value) {
	  return shadowRegex.test(value);
	}
	function isImage(value) {
	  return imageRegex.test(value);
	}
	function getDefaultConfig() {
	  const colors = fromTheme('colors');
	  const spacing = fromTheme('spacing');
	  const blur = fromTheme('blur');
	  const brightness = fromTheme('brightness');
	  const borderColor = fromTheme('borderColor');
	  const borderRadius = fromTheme('borderRadius');
	  const borderSpacing = fromTheme('borderSpacing');
	  const borderWidth = fromTheme('borderWidth');
	  const contrast = fromTheme('contrast');
	  const grayscale = fromTheme('grayscale');
	  const hueRotate = fromTheme('hueRotate');
	  const invert = fromTheme('invert');
	  const gap = fromTheme('gap');
	  const gradientColorStops = fromTheme('gradientColorStops');
	  const gradientColorStopPositions = fromTheme('gradientColorStopPositions');
	  const inset = fromTheme('inset');
	  const margin = fromTheme('margin');
	  const opacity = fromTheme('opacity');
	  const padding = fromTheme('padding');
	  const saturate = fromTheme('saturate');
	  const scale = fromTheme('scale');
	  const sepia = fromTheme('sepia');
	  const skew = fromTheme('skew');
	  const space = fromTheme('space');
	  const translate = fromTheme('translate');
	  const getOverscroll = () => ['auto', 'contain', 'none'];
	  const getOverflow = () => ['auto', 'hidden', 'clip', 'visible', 'scroll'];
	  const getSpacingWithAutoAndArbitrary = () => ['auto', isArbitraryValue, spacing];
	  const getSpacingWithArbitrary = () => [isArbitraryValue, spacing];
	  const getLengthWithEmptyAndArbitrary = () => ['', isLength, isArbitraryLength];
	  const getNumberWithAutoAndArbitrary = () => ['auto', isNumber, isArbitraryValue];
	  const getPositions = () => ['bottom', 'center', 'left', 'left-bottom', 'left-top', 'right', 'right-bottom', 'right-top', 'top'];
	  const getLineStyles = () => ['solid', 'dashed', 'dotted', 'double', 'none'];
	  const getBlendModes = () => ['normal', 'multiply', 'screen', 'overlay', 'darken', 'lighten', 'color-dodge', 'color-burn', 'hard-light', 'soft-light', 'difference', 'exclusion', 'hue', 'saturation', 'color', 'luminosity'];
	  const getAlign = () => ['start', 'end', 'center', 'between', 'around', 'evenly', 'stretch'];
	  const getZeroAndEmpty = () => ['', '0', isArbitraryValue];
	  const getBreaks = () => ['auto', 'avoid', 'all', 'avoid-page', 'page', 'left', 'right', 'column'];
	  const getNumber = () => [isNumber, isArbitraryNumber];
	  const getNumberAndArbitrary = () => [isNumber, isArbitraryValue];
	  return {
	    cacheSize: 500,
	    separator: ':',
	    theme: {
	      colors: [isAny],
	      spacing: [isLength, isArbitraryLength],
	      blur: ['none', '', isTshirtSize, isArbitraryValue],
	      brightness: getNumber(),
	      borderColor: [colors],
	      borderRadius: ['none', '', 'full', isTshirtSize, isArbitraryValue],
	      borderSpacing: getSpacingWithArbitrary(),
	      borderWidth: getLengthWithEmptyAndArbitrary(),
	      contrast: getNumber(),
	      grayscale: getZeroAndEmpty(),
	      hueRotate: getNumberAndArbitrary(),
	      invert: getZeroAndEmpty(),
	      gap: getSpacingWithArbitrary(),
	      gradientColorStops: [colors],
	      gradientColorStopPositions: [isPercent, isArbitraryLength],
	      inset: getSpacingWithAutoAndArbitrary(),
	      margin: getSpacingWithAutoAndArbitrary(),
	      opacity: getNumber(),
	      padding: getSpacingWithArbitrary(),
	      saturate: getNumber(),
	      scale: getNumber(),
	      sepia: getZeroAndEmpty(),
	      skew: getNumberAndArbitrary(),
	      space: getSpacingWithArbitrary(),
	      translate: getSpacingWithArbitrary()
	    },
	    classGroups: {
	      // Layout
	      /**
	       * Aspect Ratio
	       * @see https://tailwindcss.com/docs/aspect-ratio
	       */
	      aspect: [{
	        aspect: ['auto', 'square', 'video', isArbitraryValue]
	      }],
	      /**
	       * Container
	       * @see https://tailwindcss.com/docs/container
	       */
	      container: ['container'],
	      /**
	       * Columns
	       * @see https://tailwindcss.com/docs/columns
	       */
	      columns: [{
	        columns: [isTshirtSize]
	      }],
	      /**
	       * Break After
	       * @see https://tailwindcss.com/docs/break-after
	       */
	      'break-after': [{
	        'break-after': getBreaks()
	      }],
	      /**
	       * Break Before
	       * @see https://tailwindcss.com/docs/break-before
	       */
	      'break-before': [{
	        'break-before': getBreaks()
	      }],
	      /**
	       * Break Inside
	       * @see https://tailwindcss.com/docs/break-inside
	       */
	      'break-inside': [{
	        'break-inside': ['auto', 'avoid', 'avoid-page', 'avoid-column']
	      }],
	      /**
	       * Box Decoration Break
	       * @see https://tailwindcss.com/docs/box-decoration-break
	       */
	      'box-decoration': [{
	        'box-decoration': ['slice', 'clone']
	      }],
	      /**
	       * Box Sizing
	       * @see https://tailwindcss.com/docs/box-sizing
	       */
	      box: [{
	        box: ['border', 'content']
	      }],
	      /**
	       * Display
	       * @see https://tailwindcss.com/docs/display
	       */
	      display: ['block', 'inline-block', 'inline', 'flex', 'inline-flex', 'table', 'inline-table', 'table-caption', 'table-cell', 'table-column', 'table-column-group', 'table-footer-group', 'table-header-group', 'table-row-group', 'table-row', 'flow-root', 'grid', 'inline-grid', 'contents', 'list-item', 'hidden'],
	      /**
	       * Floats
	       * @see https://tailwindcss.com/docs/float
	       */
	      float: [{
	        float: ['right', 'left', 'none', 'start', 'end']
	      }],
	      /**
	       * Clear
	       * @see https://tailwindcss.com/docs/clear
	       */
	      clear: [{
	        clear: ['left', 'right', 'both', 'none', 'start', 'end']
	      }],
	      /**
	       * Isolation
	       * @see https://tailwindcss.com/docs/isolation
	       */
	      isolation: ['isolate', 'isolation-auto'],
	      /**
	       * Object Fit
	       * @see https://tailwindcss.com/docs/object-fit
	       */
	      'object-fit': [{
	        object: ['contain', 'cover', 'fill', 'none', 'scale-down']
	      }],
	      /**
	       * Object Position
	       * @see https://tailwindcss.com/docs/object-position
	       */
	      'object-position': [{
	        object: [...getPositions(), isArbitraryValue]
	      }],
	      /**
	       * Overflow
	       * @see https://tailwindcss.com/docs/overflow
	       */
	      overflow: [{
	        overflow: getOverflow()
	      }],
	      /**
	       * Overflow X
	       * @see https://tailwindcss.com/docs/overflow
	       */
	      'overflow-x': [{
	        'overflow-x': getOverflow()
	      }],
	      /**
	       * Overflow Y
	       * @see https://tailwindcss.com/docs/overflow
	       */
	      'overflow-y': [{
	        'overflow-y': getOverflow()
	      }],
	      /**
	       * Overscroll Behavior
	       * @see https://tailwindcss.com/docs/overscroll-behavior
	       */
	      overscroll: [{
	        overscroll: getOverscroll()
	      }],
	      /**
	       * Overscroll Behavior X
	       * @see https://tailwindcss.com/docs/overscroll-behavior
	       */
	      'overscroll-x': [{
	        'overscroll-x': getOverscroll()
	      }],
	      /**
	       * Overscroll Behavior Y
	       * @see https://tailwindcss.com/docs/overscroll-behavior
	       */
	      'overscroll-y': [{
	        'overscroll-y': getOverscroll()
	      }],
	      /**
	       * Position
	       * @see https://tailwindcss.com/docs/position
	       */
	      position: ['static', 'fixed', 'absolute', 'relative', 'sticky'],
	      /**
	       * Top / Right / Bottom / Left
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      inset: [{
	        inset: [inset]
	      }],
	      /**
	       * Right / Left
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      'inset-x': [{
	        'inset-x': [inset]
	      }],
	      /**
	       * Top / Bottom
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      'inset-y': [{
	        'inset-y': [inset]
	      }],
	      /**
	       * Start
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      start: [{
	        start: [inset]
	      }],
	      /**
	       * End
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      end: [{
	        end: [inset]
	      }],
	      /**
	       * Top
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      top: [{
	        top: [inset]
	      }],
	      /**
	       * Right
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      right: [{
	        right: [inset]
	      }],
	      /**
	       * Bottom
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      bottom: [{
	        bottom: [inset]
	      }],
	      /**
	       * Left
	       * @see https://tailwindcss.com/docs/top-right-bottom-left
	       */
	      left: [{
	        left: [inset]
	      }],
	      /**
	       * Visibility
	       * @see https://tailwindcss.com/docs/visibility
	       */
	      visibility: ['visible', 'invisible', 'collapse'],
	      /**
	       * Z-Index
	       * @see https://tailwindcss.com/docs/z-index
	       */
	      z: [{
	        z: ['auto', isInteger, isArbitraryValue]
	      }],
	      // Flexbox and Grid
	      /**
	       * Flex Basis
	       * @see https://tailwindcss.com/docs/flex-basis
	       */
	      basis: [{
	        basis: getSpacingWithAutoAndArbitrary()
	      }],
	      /**
	       * Flex Direction
	       * @see https://tailwindcss.com/docs/flex-direction
	       */
	      'flex-direction': [{
	        flex: ['row', 'row-reverse', 'col', 'col-reverse']
	      }],
	      /**
	       * Flex Wrap
	       * @see https://tailwindcss.com/docs/flex-wrap
	       */
	      'flex-wrap': [{
	        flex: ['wrap', 'wrap-reverse', 'nowrap']
	      }],
	      /**
	       * Flex
	       * @see https://tailwindcss.com/docs/flex
	       */
	      flex: [{
	        flex: ['1', 'auto', 'initial', 'none', isArbitraryValue]
	      }],
	      /**
	       * Flex Grow
	       * @see https://tailwindcss.com/docs/flex-grow
	       */
	      grow: [{
	        grow: getZeroAndEmpty()
	      }],
	      /**
	       * Flex Shrink
	       * @see https://tailwindcss.com/docs/flex-shrink
	       */
	      shrink: [{
	        shrink: getZeroAndEmpty()
	      }],
	      /**
	       * Order
	       * @see https://tailwindcss.com/docs/order
	       */
	      order: [{
	        order: ['first', 'last', 'none', isInteger, isArbitraryValue]
	      }],
	      /**
	       * Grid Template Columns
	       * @see https://tailwindcss.com/docs/grid-template-columns
	       */
	      'grid-cols': [{
	        'grid-cols': [isAny]
	      }],
	      /**
	       * Grid Column Start / End
	       * @see https://tailwindcss.com/docs/grid-column
	       */
	      'col-start-end': [{
	        col: ['auto', {
	          span: ['full', isInteger, isArbitraryValue]
	        }, isArbitraryValue]
	      }],
	      /**
	       * Grid Column Start
	       * @see https://tailwindcss.com/docs/grid-column
	       */
	      'col-start': [{
	        'col-start': getNumberWithAutoAndArbitrary()
	      }],
	      /**
	       * Grid Column End
	       * @see https://tailwindcss.com/docs/grid-column
	       */
	      'col-end': [{
	        'col-end': getNumberWithAutoAndArbitrary()
	      }],
	      /**
	       * Grid Template Rows
	       * @see https://tailwindcss.com/docs/grid-template-rows
	       */
	      'grid-rows': [{
	        'grid-rows': [isAny]
	      }],
	      /**
	       * Grid Row Start / End
	       * @see https://tailwindcss.com/docs/grid-row
	       */
	      'row-start-end': [{
	        row: ['auto', {
	          span: [isInteger, isArbitraryValue]
	        }, isArbitraryValue]
	      }],
	      /**
	       * Grid Row Start
	       * @see https://tailwindcss.com/docs/grid-row
	       */
	      'row-start': [{
	        'row-start': getNumberWithAutoAndArbitrary()
	      }],
	      /**
	       * Grid Row End
	       * @see https://tailwindcss.com/docs/grid-row
	       */
	      'row-end': [{
	        'row-end': getNumberWithAutoAndArbitrary()
	      }],
	      /**
	       * Grid Auto Flow
	       * @see https://tailwindcss.com/docs/grid-auto-flow
	       */
	      'grid-flow': [{
	        'grid-flow': ['row', 'col', 'dense', 'row-dense', 'col-dense']
	      }],
	      /**
	       * Grid Auto Columns
	       * @see https://tailwindcss.com/docs/grid-auto-columns
	       */
	      'auto-cols': [{
	        'auto-cols': ['auto', 'min', 'max', 'fr', isArbitraryValue]
	      }],
	      /**
	       * Grid Auto Rows
	       * @see https://tailwindcss.com/docs/grid-auto-rows
	       */
	      'auto-rows': [{
	        'auto-rows': ['auto', 'min', 'max', 'fr', isArbitraryValue]
	      }],
	      /**
	       * Gap
	       * @see https://tailwindcss.com/docs/gap
	       */
	      gap: [{
	        gap: [gap]
	      }],
	      /**
	       * Gap X
	       * @see https://tailwindcss.com/docs/gap
	       */
	      'gap-x': [{
	        'gap-x': [gap]
	      }],
	      /**
	       * Gap Y
	       * @see https://tailwindcss.com/docs/gap
	       */
	      'gap-y': [{
	        'gap-y': [gap]
	      }],
	      /**
	       * Justify Content
	       * @see https://tailwindcss.com/docs/justify-content
	       */
	      'justify-content': [{
	        justify: ['normal', ...getAlign()]
	      }],
	      /**
	       * Justify Items
	       * @see https://tailwindcss.com/docs/justify-items
	       */
	      'justify-items': [{
	        'justify-items': ['start', 'end', 'center', 'stretch']
	      }],
	      /**
	       * Justify Self
	       * @see https://tailwindcss.com/docs/justify-self
	       */
	      'justify-self': [{
	        'justify-self': ['auto', 'start', 'end', 'center', 'stretch']
	      }],
	      /**
	       * Align Content
	       * @see https://tailwindcss.com/docs/align-content
	       */
	      'align-content': [{
	        content: ['normal', ...getAlign(), 'baseline']
	      }],
	      /**
	       * Align Items
	       * @see https://tailwindcss.com/docs/align-items
	       */
	      'align-items': [{
	        items: ['start', 'end', 'center', 'baseline', 'stretch']
	      }],
	      /**
	       * Align Self
	       * @see https://tailwindcss.com/docs/align-self
	       */
	      'align-self': [{
	        self: ['auto', 'start', 'end', 'center', 'stretch', 'baseline']
	      }],
	      /**
	       * Place Content
	       * @see https://tailwindcss.com/docs/place-content
	       */
	      'place-content': [{
	        'place-content': [...getAlign(), 'baseline']
	      }],
	      /**
	       * Place Items
	       * @see https://tailwindcss.com/docs/place-items
	       */
	      'place-items': [{
	        'place-items': ['start', 'end', 'center', 'baseline', 'stretch']
	      }],
	      /**
	       * Place Self
	       * @see https://tailwindcss.com/docs/place-self
	       */
	      'place-self': [{
	        'place-self': ['auto', 'start', 'end', 'center', 'stretch']
	      }],
	      // Spacing
	      /**
	       * Padding
	       * @see https://tailwindcss.com/docs/padding
	       */
	      p: [{
	        p: [padding]
	      }],
	      /**
	       * Padding X
	       * @see https://tailwindcss.com/docs/padding
	       */
	      px: [{
	        px: [padding]
	      }],
	      /**
	       * Padding Y
	       * @see https://tailwindcss.com/docs/padding
	       */
	      py: [{
	        py: [padding]
	      }],
	      /**
	       * Padding Start
	       * @see https://tailwindcss.com/docs/padding
	       */
	      ps: [{
	        ps: [padding]
	      }],
	      /**
	       * Padding End
	       * @see https://tailwindcss.com/docs/padding
	       */
	      pe: [{
	        pe: [padding]
	      }],
	      /**
	       * Padding Top
	       * @see https://tailwindcss.com/docs/padding
	       */
	      pt: [{
	        pt: [padding]
	      }],
	      /**
	       * Padding Right
	       * @see https://tailwindcss.com/docs/padding
	       */
	      pr: [{
	        pr: [padding]
	      }],
	      /**
	       * Padding Bottom
	       * @see https://tailwindcss.com/docs/padding
	       */
	      pb: [{
	        pb: [padding]
	      }],
	      /**
	       * Padding Left
	       * @see https://tailwindcss.com/docs/padding
	       */
	      pl: [{
	        pl: [padding]
	      }],
	      /**
	       * Margin
	       * @see https://tailwindcss.com/docs/margin
	       */
	      m: [{
	        m: [margin]
	      }],
	      /**
	       * Margin X
	       * @see https://tailwindcss.com/docs/margin
	       */
	      mx: [{
	        mx: [margin]
	      }],
	      /**
	       * Margin Y
	       * @see https://tailwindcss.com/docs/margin
	       */
	      my: [{
	        my: [margin]
	      }],
	      /**
	       * Margin Start
	       * @see https://tailwindcss.com/docs/margin
	       */
	      ms: [{
	        ms: [margin]
	      }],
	      /**
	       * Margin End
	       * @see https://tailwindcss.com/docs/margin
	       */
	      me: [{
	        me: [margin]
	      }],
	      /**
	       * Margin Top
	       * @see https://tailwindcss.com/docs/margin
	       */
	      mt: [{
	        mt: [margin]
	      }],
	      /**
	       * Margin Right
	       * @see https://tailwindcss.com/docs/margin
	       */
	      mr: [{
	        mr: [margin]
	      }],
	      /**
	       * Margin Bottom
	       * @see https://tailwindcss.com/docs/margin
	       */
	      mb: [{
	        mb: [margin]
	      }],
	      /**
	       * Margin Left
	       * @see https://tailwindcss.com/docs/margin
	       */
	      ml: [{
	        ml: [margin]
	      }],
	      /**
	       * Space Between X
	       * @see https://tailwindcss.com/docs/space
	       */
	      'space-x': [{
	        'space-x': [space]
	      }],
	      /**
	       * Space Between X Reverse
	       * @see https://tailwindcss.com/docs/space
	       */
	      'space-x-reverse': ['space-x-reverse'],
	      /**
	       * Space Between Y
	       * @see https://tailwindcss.com/docs/space
	       */
	      'space-y': [{
	        'space-y': [space]
	      }],
	      /**
	       * Space Between Y Reverse
	       * @see https://tailwindcss.com/docs/space
	       */
	      'space-y-reverse': ['space-y-reverse'],
	      // Sizing
	      /**
	       * Width
	       * @see https://tailwindcss.com/docs/width
	       */
	      w: [{
	        w: ['auto', 'min', 'max', 'fit', 'svw', 'lvw', 'dvw', isArbitraryValue, spacing]
	      }],
	      /**
	       * Min-Width
	       * @see https://tailwindcss.com/docs/min-width
	       */
	      'min-w': [{
	        'min-w': [isArbitraryValue, spacing, 'min', 'max', 'fit']
	      }],
	      /**
	       * Max-Width
	       * @see https://tailwindcss.com/docs/max-width
	       */
	      'max-w': [{
	        'max-w': [isArbitraryValue, spacing, 'none', 'full', 'min', 'max', 'fit', 'prose', {
	          screen: [isTshirtSize]
	        }, isTshirtSize]
	      }],
	      /**
	       * Height
	       * @see https://tailwindcss.com/docs/height
	       */
	      h: [{
	        h: [isArbitraryValue, spacing, 'auto', 'min', 'max', 'fit', 'svh', 'lvh', 'dvh']
	      }],
	      /**
	       * Min-Height
	       * @see https://tailwindcss.com/docs/min-height
	       */
	      'min-h': [{
	        'min-h': [isArbitraryValue, spacing, 'min', 'max', 'fit', 'svh', 'lvh', 'dvh']
	      }],
	      /**
	       * Max-Height
	       * @see https://tailwindcss.com/docs/max-height
	       */
	      'max-h': [{
	        'max-h': [isArbitraryValue, spacing, 'min', 'max', 'fit', 'svh', 'lvh', 'dvh']
	      }],
	      /**
	       * Size
	       * @see https://tailwindcss.com/docs/size
	       */
	      size: [{
	        size: [isArbitraryValue, spacing, 'auto', 'min', 'max', 'fit']
	      }],
	      // Typography
	      /**
	       * Font Size
	       * @see https://tailwindcss.com/docs/font-size
	       */
	      'font-size': [{
	        text: ['base', isTshirtSize, isArbitraryLength]
	      }],
	      /**
	       * Font Smoothing
	       * @see https://tailwindcss.com/docs/font-smoothing
	       */
	      'font-smoothing': ['antialiased', 'subpixel-antialiased'],
	      /**
	       * Font Style
	       * @see https://tailwindcss.com/docs/font-style
	       */
	      'font-style': ['italic', 'not-italic'],
	      /**
	       * Font Weight
	       * @see https://tailwindcss.com/docs/font-weight
	       */
	      'font-weight': [{
	        font: ['thin', 'extralight', 'light', 'normal', 'medium', 'semibold', 'bold', 'extrabold', 'black', isArbitraryNumber]
	      }],
	      /**
	       * Font Family
	       * @see https://tailwindcss.com/docs/font-family
	       */
	      'font-family': [{
	        font: [isAny]
	      }],
	      /**
	       * Font Variant Numeric
	       * @see https://tailwindcss.com/docs/font-variant-numeric
	       */
	      'fvn-normal': ['normal-nums'],
	      /**
	       * Font Variant Numeric
	       * @see https://tailwindcss.com/docs/font-variant-numeric
	       */
	      'fvn-ordinal': ['ordinal'],
	      /**
	       * Font Variant Numeric
	       * @see https://tailwindcss.com/docs/font-variant-numeric
	       */
	      'fvn-slashed-zero': ['slashed-zero'],
	      /**
	       * Font Variant Numeric
	       * @see https://tailwindcss.com/docs/font-variant-numeric
	       */
	      'fvn-figure': ['lining-nums', 'oldstyle-nums'],
	      /**
	       * Font Variant Numeric
	       * @see https://tailwindcss.com/docs/font-variant-numeric
	       */
	      'fvn-spacing': ['proportional-nums', 'tabular-nums'],
	      /**
	       * Font Variant Numeric
	       * @see https://tailwindcss.com/docs/font-variant-numeric
	       */
	      'fvn-fraction': ['diagonal-fractions', 'stacked-fractons'],
	      /**
	       * Letter Spacing
	       * @see https://tailwindcss.com/docs/letter-spacing
	       */
	      tracking: [{
	        tracking: ['tighter', 'tight', 'normal', 'wide', 'wider', 'widest', isArbitraryValue]
	      }],
	      /**
	       * Line Clamp
	       * @see https://tailwindcss.com/docs/line-clamp
	       */
	      'line-clamp': [{
	        'line-clamp': ['none', isNumber, isArbitraryNumber]
	      }],
	      /**
	       * Line Height
	       * @see https://tailwindcss.com/docs/line-height
	       */
	      leading: [{
	        leading: ['none', 'tight', 'snug', 'normal', 'relaxed', 'loose', isLength, isArbitraryValue]
	      }],
	      /**
	       * List Style Image
	       * @see https://tailwindcss.com/docs/list-style-image
	       */
	      'list-image': [{
	        'list-image': ['none', isArbitraryValue]
	      }],
	      /**
	       * List Style Type
	       * @see https://tailwindcss.com/docs/list-style-type
	       */
	      'list-style-type': [{
	        list: ['none', 'disc', 'decimal', isArbitraryValue]
	      }],
	      /**
	       * List Style Position
	       * @see https://tailwindcss.com/docs/list-style-position
	       */
	      'list-style-position': [{
	        list: ['inside', 'outside']
	      }],
	      /**
	       * Placeholder Color
	       * @deprecated since Tailwind CSS v3.0.0
	       * @see https://tailwindcss.com/docs/placeholder-color
	       */
	      'placeholder-color': [{
	        placeholder: [colors]
	      }],
	      /**
	       * Placeholder Opacity
	       * @see https://tailwindcss.com/docs/placeholder-opacity
	       */
	      'placeholder-opacity': [{
	        'placeholder-opacity': [opacity]
	      }],
	      /**
	       * Text Alignment
	       * @see https://tailwindcss.com/docs/text-align
	       */
	      'text-alignment': [{
	        text: ['left', 'center', 'right', 'justify', 'start', 'end']
	      }],
	      /**
	       * Text Color
	       * @see https://tailwindcss.com/docs/text-color
	       */
	      'text-color': [{
	        text: [colors]
	      }],
	      /**
	       * Text Opacity
	       * @see https://tailwindcss.com/docs/text-opacity
	       */
	      'text-opacity': [{
	        'text-opacity': [opacity]
	      }],
	      /**
	       * Text Decoration
	       * @see https://tailwindcss.com/docs/text-decoration
	       */
	      'text-decoration': ['underline', 'overline', 'line-through', 'no-underline'],
	      /**
	       * Text Decoration Style
	       * @see https://tailwindcss.com/docs/text-decoration-style
	       */
	      'text-decoration-style': [{
	        decoration: [...getLineStyles(), 'wavy']
	      }],
	      /**
	       * Text Decoration Thickness
	       * @see https://tailwindcss.com/docs/text-decoration-thickness
	       */
	      'text-decoration-thickness': [{
	        decoration: ['auto', 'from-font', isLength, isArbitraryLength]
	      }],
	      /**
	       * Text Underline Offset
	       * @see https://tailwindcss.com/docs/text-underline-offset
	       */
	      'underline-offset': [{
	        'underline-offset': ['auto', isLength, isArbitraryValue]
	      }],
	      /**
	       * Text Decoration Color
	       * @see https://tailwindcss.com/docs/text-decoration-color
	       */
	      'text-decoration-color': [{
	        decoration: [colors]
	      }],
	      /**
	       * Text Transform
	       * @see https://tailwindcss.com/docs/text-transform
	       */
	      'text-transform': ['uppercase', 'lowercase', 'capitalize', 'normal-case'],
	      /**
	       * Text Overflow
	       * @see https://tailwindcss.com/docs/text-overflow
	       */
	      'text-overflow': ['truncate', 'text-ellipsis', 'text-clip'],
	      /**
	       * Text Wrap
	       * @see https://tailwindcss.com/docs/text-wrap
	       */
	      'text-wrap': [{
	        text: ['wrap', 'nowrap', 'balance', 'pretty']
	      }],
	      /**
	       * Text Indent
	       * @see https://tailwindcss.com/docs/text-indent
	       */
	      indent: [{
	        indent: getSpacingWithArbitrary()
	      }],
	      /**
	       * Vertical Alignment
	       * @see https://tailwindcss.com/docs/vertical-align
	       */
	      'vertical-align': [{
	        align: ['baseline', 'top', 'middle', 'bottom', 'text-top', 'text-bottom', 'sub', 'super', isArbitraryValue]
	      }],
	      /**
	       * Whitespace
	       * @see https://tailwindcss.com/docs/whitespace
	       */
	      whitespace: [{
	        whitespace: ['normal', 'nowrap', 'pre', 'pre-line', 'pre-wrap', 'break-spaces']
	      }],
	      /**
	       * Word Break
	       * @see https://tailwindcss.com/docs/word-break
	       */
	      break: [{
	        break: ['normal', 'words', 'all', 'keep']
	      }],
	      /**
	       * Hyphens
	       * @see https://tailwindcss.com/docs/hyphens
	       */
	      hyphens: [{
	        hyphens: ['none', 'manual', 'auto']
	      }],
	      /**
	       * Content
	       * @see https://tailwindcss.com/docs/content
	       */
	      content: [{
	        content: ['none', isArbitraryValue]
	      }],
	      // Backgrounds
	      /**
	       * Background Attachment
	       * @see https://tailwindcss.com/docs/background-attachment
	       */
	      'bg-attachment': [{
	        bg: ['fixed', 'local', 'scroll']
	      }],
	      /**
	       * Background Clip
	       * @see https://tailwindcss.com/docs/background-clip
	       */
	      'bg-clip': [{
	        'bg-clip': ['border', 'padding', 'content', 'text']
	      }],
	      /**
	       * Background Opacity
	       * @deprecated since Tailwind CSS v3.0.0
	       * @see https://tailwindcss.com/docs/background-opacity
	       */
	      'bg-opacity': [{
	        'bg-opacity': [opacity]
	      }],
	      /**
	       * Background Origin
	       * @see https://tailwindcss.com/docs/background-origin
	       */
	      'bg-origin': [{
	        'bg-origin': ['border', 'padding', 'content']
	      }],
	      /**
	       * Background Position
	       * @see https://tailwindcss.com/docs/background-position
	       */
	      'bg-position': [{
	        bg: [...getPositions(), isArbitraryPosition]
	      }],
	      /**
	       * Background Repeat
	       * @see https://tailwindcss.com/docs/background-repeat
	       */
	      'bg-repeat': [{
	        bg: ['no-repeat', {
	          repeat: ['', 'x', 'y', 'round', 'space']
	        }]
	      }],
	      /**
	       * Background Size
	       * @see https://tailwindcss.com/docs/background-size
	       */
	      'bg-size': [{
	        bg: ['auto', 'cover', 'contain', isArbitrarySize]
	      }],
	      /**
	       * Background Image
	       * @see https://tailwindcss.com/docs/background-image
	       */
	      'bg-image': [{
	        bg: ['none', {
	          'gradient-to': ['t', 'tr', 'r', 'br', 'b', 'bl', 'l', 'tl']
	        }, isArbitraryImage]
	      }],
	      /**
	       * Background Color
	       * @see https://tailwindcss.com/docs/background-color
	       */
	      'bg-color': [{
	        bg: [colors]
	      }],
	      /**
	       * Gradient Color Stops From Position
	       * @see https://tailwindcss.com/docs/gradient-color-stops
	       */
	      'gradient-from-pos': [{
	        from: [gradientColorStopPositions]
	      }],
	      /**
	       * Gradient Color Stops Via Position
	       * @see https://tailwindcss.com/docs/gradient-color-stops
	       */
	      'gradient-via-pos': [{
	        via: [gradientColorStopPositions]
	      }],
	      /**
	       * Gradient Color Stops To Position
	       * @see https://tailwindcss.com/docs/gradient-color-stops
	       */
	      'gradient-to-pos': [{
	        to: [gradientColorStopPositions]
	      }],
	      /**
	       * Gradient Color Stops From
	       * @see https://tailwindcss.com/docs/gradient-color-stops
	       */
	      'gradient-from': [{
	        from: [gradientColorStops]
	      }],
	      /**
	       * Gradient Color Stops Via
	       * @see https://tailwindcss.com/docs/gradient-color-stops
	       */
	      'gradient-via': [{
	        via: [gradientColorStops]
	      }],
	      /**
	       * Gradient Color Stops To
	       * @see https://tailwindcss.com/docs/gradient-color-stops
	       */
	      'gradient-to': [{
	        to: [gradientColorStops]
	      }],
	      // Borders
	      /**
	       * Border Radius
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      rounded: [{
	        rounded: [borderRadius]
	      }],
	      /**
	       * Border Radius Start
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-s': [{
	        'rounded-s': [borderRadius]
	      }],
	      /**
	       * Border Radius End
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-e': [{
	        'rounded-e': [borderRadius]
	      }],
	      /**
	       * Border Radius Top
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-t': [{
	        'rounded-t': [borderRadius]
	      }],
	      /**
	       * Border Radius Right
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-r': [{
	        'rounded-r': [borderRadius]
	      }],
	      /**
	       * Border Radius Bottom
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-b': [{
	        'rounded-b': [borderRadius]
	      }],
	      /**
	       * Border Radius Left
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-l': [{
	        'rounded-l': [borderRadius]
	      }],
	      /**
	       * Border Radius Start Start
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-ss': [{
	        'rounded-ss': [borderRadius]
	      }],
	      /**
	       * Border Radius Start End
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-se': [{
	        'rounded-se': [borderRadius]
	      }],
	      /**
	       * Border Radius End End
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-ee': [{
	        'rounded-ee': [borderRadius]
	      }],
	      /**
	       * Border Radius End Start
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-es': [{
	        'rounded-es': [borderRadius]
	      }],
	      /**
	       * Border Radius Top Left
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-tl': [{
	        'rounded-tl': [borderRadius]
	      }],
	      /**
	       * Border Radius Top Right
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-tr': [{
	        'rounded-tr': [borderRadius]
	      }],
	      /**
	       * Border Radius Bottom Right
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-br': [{
	        'rounded-br': [borderRadius]
	      }],
	      /**
	       * Border Radius Bottom Left
	       * @see https://tailwindcss.com/docs/border-radius
	       */
	      'rounded-bl': [{
	        'rounded-bl': [borderRadius]
	      }],
	      /**
	       * Border Width
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w': [{
	        border: [borderWidth]
	      }],
	      /**
	       * Border Width X
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-x': [{
	        'border-x': [borderWidth]
	      }],
	      /**
	       * Border Width Y
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-y': [{
	        'border-y': [borderWidth]
	      }],
	      /**
	       * Border Width Start
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-s': [{
	        'border-s': [borderWidth]
	      }],
	      /**
	       * Border Width End
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-e': [{
	        'border-e': [borderWidth]
	      }],
	      /**
	       * Border Width Top
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-t': [{
	        'border-t': [borderWidth]
	      }],
	      /**
	       * Border Width Right
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-r': [{
	        'border-r': [borderWidth]
	      }],
	      /**
	       * Border Width Bottom
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-b': [{
	        'border-b': [borderWidth]
	      }],
	      /**
	       * Border Width Left
	       * @see https://tailwindcss.com/docs/border-width
	       */
	      'border-w-l': [{
	        'border-l': [borderWidth]
	      }],
	      /**
	       * Border Opacity
	       * @see https://tailwindcss.com/docs/border-opacity
	       */
	      'border-opacity': [{
	        'border-opacity': [opacity]
	      }],
	      /**
	       * Border Style
	       * @see https://tailwindcss.com/docs/border-style
	       */
	      'border-style': [{
	        border: [...getLineStyles(), 'hidden']
	      }],
	      /**
	       * Divide Width X
	       * @see https://tailwindcss.com/docs/divide-width
	       */
	      'divide-x': [{
	        'divide-x': [borderWidth]
	      }],
	      /**
	       * Divide Width X Reverse
	       * @see https://tailwindcss.com/docs/divide-width
	       */
	      'divide-x-reverse': ['divide-x-reverse'],
	      /**
	       * Divide Width Y
	       * @see https://tailwindcss.com/docs/divide-width
	       */
	      'divide-y': [{
	        'divide-y': [borderWidth]
	      }],
	      /**
	       * Divide Width Y Reverse
	       * @see https://tailwindcss.com/docs/divide-width
	       */
	      'divide-y-reverse': ['divide-y-reverse'],
	      /**
	       * Divide Opacity
	       * @see https://tailwindcss.com/docs/divide-opacity
	       */
	      'divide-opacity': [{
	        'divide-opacity': [opacity]
	      }],
	      /**
	       * Divide Style
	       * @see https://tailwindcss.com/docs/divide-style
	       */
	      'divide-style': [{
	        divide: getLineStyles()
	      }],
	      /**
	       * Border Color
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color': [{
	        border: [borderColor]
	      }],
	      /**
	       * Border Color X
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color-x': [{
	        'border-x': [borderColor]
	      }],
	      /**
	       * Border Color Y
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color-y': [{
	        'border-y': [borderColor]
	      }],
	      /**
	       * Border Color Top
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color-t': [{
	        'border-t': [borderColor]
	      }],
	      /**
	       * Border Color Right
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color-r': [{
	        'border-r': [borderColor]
	      }],
	      /**
	       * Border Color Bottom
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color-b': [{
	        'border-b': [borderColor]
	      }],
	      /**
	       * Border Color Left
	       * @see https://tailwindcss.com/docs/border-color
	       */
	      'border-color-l': [{
	        'border-l': [borderColor]
	      }],
	      /**
	       * Divide Color
	       * @see https://tailwindcss.com/docs/divide-color
	       */
	      'divide-color': [{
	        divide: [borderColor]
	      }],
	      /**
	       * Outline Style
	       * @see https://tailwindcss.com/docs/outline-style
	       */
	      'outline-style': [{
	        outline: ['', ...getLineStyles()]
	      }],
	      /**
	       * Outline Offset
	       * @see https://tailwindcss.com/docs/outline-offset
	       */
	      'outline-offset': [{
	        'outline-offset': [isLength, isArbitraryValue]
	      }],
	      /**
	       * Outline Width
	       * @see https://tailwindcss.com/docs/outline-width
	       */
	      'outline-w': [{
	        outline: [isLength, isArbitraryLength]
	      }],
	      /**
	       * Outline Color
	       * @see https://tailwindcss.com/docs/outline-color
	       */
	      'outline-color': [{
	        outline: [colors]
	      }],
	      /**
	       * Ring Width
	       * @see https://tailwindcss.com/docs/ring-width
	       */
	      'ring-w': [{
	        ring: getLengthWithEmptyAndArbitrary()
	      }],
	      /**
	       * Ring Width Inset
	       * @see https://tailwindcss.com/docs/ring-width
	       */
	      'ring-w-inset': ['ring-inset'],
	      /**
	       * Ring Color
	       * @see https://tailwindcss.com/docs/ring-color
	       */
	      'ring-color': [{
	        ring: [colors]
	      }],
	      /**
	       * Ring Opacity
	       * @see https://tailwindcss.com/docs/ring-opacity
	       */
	      'ring-opacity': [{
	        'ring-opacity': [opacity]
	      }],
	      /**
	       * Ring Offset Width
	       * @see https://tailwindcss.com/docs/ring-offset-width
	       */
	      'ring-offset-w': [{
	        'ring-offset': [isLength, isArbitraryLength]
	      }],
	      /**
	       * Ring Offset Color
	       * @see https://tailwindcss.com/docs/ring-offset-color
	       */
	      'ring-offset-color': [{
	        'ring-offset': [colors]
	      }],
	      // Effects
	      /**
	       * Box Shadow
	       * @see https://tailwindcss.com/docs/box-shadow
	       */
	      shadow: [{
	        shadow: ['', 'inner', 'none', isTshirtSize, isArbitraryShadow]
	      }],
	      /**
	       * Box Shadow Color
	       * @see https://tailwindcss.com/docs/box-shadow-color
	       */
	      'shadow-color': [{
	        shadow: [isAny]
	      }],
	      /**
	       * Opacity
	       * @see https://tailwindcss.com/docs/opacity
	       */
	      opacity: [{
	        opacity: [opacity]
	      }],
	      /**
	       * Mix Blend Mode
	       * @see https://tailwindcss.com/docs/mix-blend-mode
	       */
	      'mix-blend': [{
	        'mix-blend': [...getBlendModes(), 'plus-lighter', 'plus-darker']
	      }],
	      /**
	       * Background Blend Mode
	       * @see https://tailwindcss.com/docs/background-blend-mode
	       */
	      'bg-blend': [{
	        'bg-blend': getBlendModes()
	      }],
	      // Filters
	      /**
	       * Filter
	       * @deprecated since Tailwind CSS v3.0.0
	       * @see https://tailwindcss.com/docs/filter
	       */
	      filter: [{
	        filter: ['', 'none']
	      }],
	      /**
	       * Blur
	       * @see https://tailwindcss.com/docs/blur
	       */
	      blur: [{
	        blur: [blur]
	      }],
	      /**
	       * Brightness
	       * @see https://tailwindcss.com/docs/brightness
	       */
	      brightness: [{
	        brightness: [brightness]
	      }],
	      /**
	       * Contrast
	       * @see https://tailwindcss.com/docs/contrast
	       */
	      contrast: [{
	        contrast: [contrast]
	      }],
	      /**
	       * Drop Shadow
	       * @see https://tailwindcss.com/docs/drop-shadow
	       */
	      'drop-shadow': [{
	        'drop-shadow': ['', 'none', isTshirtSize, isArbitraryValue]
	      }],
	      /**
	       * Grayscale
	       * @see https://tailwindcss.com/docs/grayscale
	       */
	      grayscale: [{
	        grayscale: [grayscale]
	      }],
	      /**
	       * Hue Rotate
	       * @see https://tailwindcss.com/docs/hue-rotate
	       */
	      'hue-rotate': [{
	        'hue-rotate': [hueRotate]
	      }],
	      /**
	       * Invert
	       * @see https://tailwindcss.com/docs/invert
	       */
	      invert: [{
	        invert: [invert]
	      }],
	      /**
	       * Saturate
	       * @see https://tailwindcss.com/docs/saturate
	       */
	      saturate: [{
	        saturate: [saturate]
	      }],
	      /**
	       * Sepia
	       * @see https://tailwindcss.com/docs/sepia
	       */
	      sepia: [{
	        sepia: [sepia]
	      }],
	      /**
	       * Backdrop Filter
	       * @deprecated since Tailwind CSS v3.0.0
	       * @see https://tailwindcss.com/docs/backdrop-filter
	       */
	      'backdrop-filter': [{
	        'backdrop-filter': ['', 'none']
	      }],
	      /**
	       * Backdrop Blur
	       * @see https://tailwindcss.com/docs/backdrop-blur
	       */
	      'backdrop-blur': [{
	        'backdrop-blur': [blur]
	      }],
	      /**
	       * Backdrop Brightness
	       * @see https://tailwindcss.com/docs/backdrop-brightness
	       */
	      'backdrop-brightness': [{
	        'backdrop-brightness': [brightness]
	      }],
	      /**
	       * Backdrop Contrast
	       * @see https://tailwindcss.com/docs/backdrop-contrast
	       */
	      'backdrop-contrast': [{
	        'backdrop-contrast': [contrast]
	      }],
	      /**
	       * Backdrop Grayscale
	       * @see https://tailwindcss.com/docs/backdrop-grayscale
	       */
	      'backdrop-grayscale': [{
	        'backdrop-grayscale': [grayscale]
	      }],
	      /**
	       * Backdrop Hue Rotate
	       * @see https://tailwindcss.com/docs/backdrop-hue-rotate
	       */
	      'backdrop-hue-rotate': [{
	        'backdrop-hue-rotate': [hueRotate]
	      }],
	      /**
	       * Backdrop Invert
	       * @see https://tailwindcss.com/docs/backdrop-invert
	       */
	      'backdrop-invert': [{
	        'backdrop-invert': [invert]
	      }],
	      /**
	       * Backdrop Opacity
	       * @see https://tailwindcss.com/docs/backdrop-opacity
	       */
	      'backdrop-opacity': [{
	        'backdrop-opacity': [opacity]
	      }],
	      /**
	       * Backdrop Saturate
	       * @see https://tailwindcss.com/docs/backdrop-saturate
	       */
	      'backdrop-saturate': [{
	        'backdrop-saturate': [saturate]
	      }],
	      /**
	       * Backdrop Sepia
	       * @see https://tailwindcss.com/docs/backdrop-sepia
	       */
	      'backdrop-sepia': [{
	        'backdrop-sepia': [sepia]
	      }],
	      // Tables
	      /**
	       * Border Collapse
	       * @see https://tailwindcss.com/docs/border-collapse
	       */
	      'border-collapse': [{
	        border: ['collapse', 'separate']
	      }],
	      /**
	       * Border Spacing
	       * @see https://tailwindcss.com/docs/border-spacing
	       */
	      'border-spacing': [{
	        'border-spacing': [borderSpacing]
	      }],
	      /**
	       * Border Spacing X
	       * @see https://tailwindcss.com/docs/border-spacing
	       */
	      'border-spacing-x': [{
	        'border-spacing-x': [borderSpacing]
	      }],
	      /**
	       * Border Spacing Y
	       * @see https://tailwindcss.com/docs/border-spacing
	       */
	      'border-spacing-y': [{
	        'border-spacing-y': [borderSpacing]
	      }],
	      /**
	       * Table Layout
	       * @see https://tailwindcss.com/docs/table-layout
	       */
	      'table-layout': [{
	        table: ['auto', 'fixed']
	      }],
	      /**
	       * Caption Side
	       * @see https://tailwindcss.com/docs/caption-side
	       */
	      caption: [{
	        caption: ['top', 'bottom']
	      }],
	      // Transitions and Animation
	      /**
	       * Tranisition Property
	       * @see https://tailwindcss.com/docs/transition-property
	       */
	      transition: [{
	        transition: ['none', 'all', '', 'colors', 'opacity', 'shadow', 'transform', isArbitraryValue]
	      }],
	      /**
	       * Transition Duration
	       * @see https://tailwindcss.com/docs/transition-duration
	       */
	      duration: [{
	        duration: getNumberAndArbitrary()
	      }],
	      /**
	       * Transition Timing Function
	       * @see https://tailwindcss.com/docs/transition-timing-function
	       */
	      ease: [{
	        ease: ['linear', 'in', 'out', 'in-out', isArbitraryValue]
	      }],
	      /**
	       * Transition Delay
	       * @see https://tailwindcss.com/docs/transition-delay
	       */
	      delay: [{
	        delay: getNumberAndArbitrary()
	      }],
	      /**
	       * Animation
	       * @see https://tailwindcss.com/docs/animation
	       */
	      animate: [{
	        animate: ['none', 'spin', 'ping', 'pulse', 'bounce', isArbitraryValue]
	      }],
	      // Transforms
	      /**
	       * Transform
	       * @see https://tailwindcss.com/docs/transform
	       */
	      transform: [{
	        transform: ['', 'gpu', 'none']
	      }],
	      /**
	       * Scale
	       * @see https://tailwindcss.com/docs/scale
	       */
	      scale: [{
	        scale: [scale]
	      }],
	      /**
	       * Scale X
	       * @see https://tailwindcss.com/docs/scale
	       */
	      'scale-x': [{
	        'scale-x': [scale]
	      }],
	      /**
	       * Scale Y
	       * @see https://tailwindcss.com/docs/scale
	       */
	      'scale-y': [{
	        'scale-y': [scale]
	      }],
	      /**
	       * Rotate
	       * @see https://tailwindcss.com/docs/rotate
	       */
	      rotate: [{
	        rotate: [isInteger, isArbitraryValue]
	      }],
	      /**
	       * Translate X
	       * @see https://tailwindcss.com/docs/translate
	       */
	      'translate-x': [{
	        'translate-x': [translate]
	      }],
	      /**
	       * Translate Y
	       * @see https://tailwindcss.com/docs/translate
	       */
	      'translate-y': [{
	        'translate-y': [translate]
	      }],
	      /**
	       * Skew X
	       * @see https://tailwindcss.com/docs/skew
	       */
	      'skew-x': [{
	        'skew-x': [skew]
	      }],
	      /**
	       * Skew Y
	       * @see https://tailwindcss.com/docs/skew
	       */
	      'skew-y': [{
	        'skew-y': [skew]
	      }],
	      /**
	       * Transform Origin
	       * @see https://tailwindcss.com/docs/transform-origin
	       */
	      'transform-origin': [{
	        origin: ['center', 'top', 'top-right', 'right', 'bottom-right', 'bottom', 'bottom-left', 'left', 'top-left', isArbitraryValue]
	      }],
	      // Interactivity
	      /**
	       * Accent Color
	       * @see https://tailwindcss.com/docs/accent-color
	       */
	      accent: [{
	        accent: ['auto', colors]
	      }],
	      /**
	       * Appearance
	       * @see https://tailwindcss.com/docs/appearance
	       */
	      appearance: [{
	        appearance: ['none', 'auto']
	      }],
	      /**
	       * Cursor
	       * @see https://tailwindcss.com/docs/cursor
	       */
	      cursor: [{
	        cursor: ['auto', 'default', 'pointer', 'wait', 'text', 'move', 'help', 'not-allowed', 'none', 'context-menu', 'progress', 'cell', 'crosshair', 'vertical-text', 'alias', 'copy', 'no-drop', 'grab', 'grabbing', 'all-scroll', 'col-resize', 'row-resize', 'n-resize', 'e-resize', 's-resize', 'w-resize', 'ne-resize', 'nw-resize', 'se-resize', 'sw-resize', 'ew-resize', 'ns-resize', 'nesw-resize', 'nwse-resize', 'zoom-in', 'zoom-out', isArbitraryValue]
	      }],
	      /**
	       * Caret Color
	       * @see https://tailwindcss.com/docs/just-in-time-mode#caret-color-utilities
	       */
	      'caret-color': [{
	        caret: [colors]
	      }],
	      /**
	       * Pointer Events
	       * @see https://tailwindcss.com/docs/pointer-events
	       */
	      'pointer-events': [{
	        'pointer-events': ['none', 'auto']
	      }],
	      /**
	       * Resize
	       * @see https://tailwindcss.com/docs/resize
	       */
	      resize: [{
	        resize: ['none', 'y', 'x', '']
	      }],
	      /**
	       * Scroll Behavior
	       * @see https://tailwindcss.com/docs/scroll-behavior
	       */
	      'scroll-behavior': [{
	        scroll: ['auto', 'smooth']
	      }],
	      /**
	       * Scroll Margin
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-m': [{
	        'scroll-m': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin X
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-mx': [{
	        'scroll-mx': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin Y
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-my': [{
	        'scroll-my': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin Start
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-ms': [{
	        'scroll-ms': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin End
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-me': [{
	        'scroll-me': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin Top
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-mt': [{
	        'scroll-mt': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin Right
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-mr': [{
	        'scroll-mr': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin Bottom
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-mb': [{
	        'scroll-mb': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Margin Left
	       * @see https://tailwindcss.com/docs/scroll-margin
	       */
	      'scroll-ml': [{
	        'scroll-ml': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-p': [{
	        'scroll-p': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding X
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-px': [{
	        'scroll-px': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding Y
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-py': [{
	        'scroll-py': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding Start
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-ps': [{
	        'scroll-ps': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding End
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-pe': [{
	        'scroll-pe': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding Top
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-pt': [{
	        'scroll-pt': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding Right
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-pr': [{
	        'scroll-pr': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding Bottom
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-pb': [{
	        'scroll-pb': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Padding Left
	       * @see https://tailwindcss.com/docs/scroll-padding
	       */
	      'scroll-pl': [{
	        'scroll-pl': getSpacingWithArbitrary()
	      }],
	      /**
	       * Scroll Snap Align
	       * @see https://tailwindcss.com/docs/scroll-snap-align
	       */
	      'snap-align': [{
	        snap: ['start', 'end', 'center', 'align-none']
	      }],
	      /**
	       * Scroll Snap Stop
	       * @see https://tailwindcss.com/docs/scroll-snap-stop
	       */
	      'snap-stop': [{
	        snap: ['normal', 'always']
	      }],
	      /**
	       * Scroll Snap Type
	       * @see https://tailwindcss.com/docs/scroll-snap-type
	       */
	      'snap-type': [{
	        snap: ['none', 'x', 'y', 'both']
	      }],
	      /**
	       * Scroll Snap Type Strictness
	       * @see https://tailwindcss.com/docs/scroll-snap-type
	       */
	      'snap-strictness': [{
	        snap: ['mandatory', 'proximity']
	      }],
	      /**
	       * Touch Action
	       * @see https://tailwindcss.com/docs/touch-action
	       */
	      touch: [{
	        touch: ['auto', 'none', 'manipulation']
	      }],
	      /**
	       * Touch Action X
	       * @see https://tailwindcss.com/docs/touch-action
	       */
	      'touch-x': [{
	        'touch-pan': ['x', 'left', 'right']
	      }],
	      /**
	       * Touch Action Y
	       * @see https://tailwindcss.com/docs/touch-action
	       */
	      'touch-y': [{
	        'touch-pan': ['y', 'up', 'down']
	      }],
	      /**
	       * Touch Action Pinch Zoom
	       * @see https://tailwindcss.com/docs/touch-action
	       */
	      'touch-pz': ['touch-pinch-zoom'],
	      /**
	       * User Select
	       * @see https://tailwindcss.com/docs/user-select
	       */
	      select: [{
	        select: ['none', 'text', 'all', 'auto']
	      }],
	      /**
	       * Will Change
	       * @see https://tailwindcss.com/docs/will-change
	       */
	      'will-change': [{
	        'will-change': ['auto', 'scroll', 'contents', 'transform', isArbitraryValue]
	      }],
	      // SVG
	      /**
	       * Fill
	       * @see https://tailwindcss.com/docs/fill
	       */
	      fill: [{
	        fill: [colors, 'none']
	      }],
	      /**
	       * Stroke Width
	       * @see https://tailwindcss.com/docs/stroke-width
	       */
	      'stroke-w': [{
	        stroke: [isLength, isArbitraryLength, isArbitraryNumber]
	      }],
	      /**
	       * Stroke
	       * @see https://tailwindcss.com/docs/stroke
	       */
	      stroke: [{
	        stroke: [colors, 'none']
	      }],
	      // Accessibility
	      /**
	       * Screen Readers
	       * @see https://tailwindcss.com/docs/screen-readers
	       */
	      sr: ['sr-only', 'not-sr-only'],
	      /**
	       * Forced Color Adjust
	       * @see https://tailwindcss.com/docs/forced-color-adjust
	       */
	      'forced-color-adjust': [{
	        'forced-color-adjust': ['auto', 'none']
	      }]
	    },
	    conflictingClassGroups: {
	      overflow: ['overflow-x', 'overflow-y'],
	      overscroll: ['overscroll-x', 'overscroll-y'],
	      inset: ['inset-x', 'inset-y', 'start', 'end', 'top', 'right', 'bottom', 'left'],
	      'inset-x': ['right', 'left'],
	      'inset-y': ['top', 'bottom'],
	      flex: ['basis', 'grow', 'shrink'],
	      gap: ['gap-x', 'gap-y'],
	      p: ['px', 'py', 'ps', 'pe', 'pt', 'pr', 'pb', 'pl'],
	      px: ['pr', 'pl'],
	      py: ['pt', 'pb'],
	      m: ['mx', 'my', 'ms', 'me', 'mt', 'mr', 'mb', 'ml'],
	      mx: ['mr', 'ml'],
	      my: ['mt', 'mb'],
	      size: ['w', 'h'],
	      'font-size': ['leading'],
	      'fvn-normal': ['fvn-ordinal', 'fvn-slashed-zero', 'fvn-figure', 'fvn-spacing', 'fvn-fraction'],
	      'fvn-ordinal': ['fvn-normal'],
	      'fvn-slashed-zero': ['fvn-normal'],
	      'fvn-figure': ['fvn-normal'],
	      'fvn-spacing': ['fvn-normal'],
	      'fvn-fraction': ['fvn-normal'],
	      'line-clamp': ['display', 'overflow'],
	      rounded: ['rounded-s', 'rounded-e', 'rounded-t', 'rounded-r', 'rounded-b', 'rounded-l', 'rounded-ss', 'rounded-se', 'rounded-ee', 'rounded-es', 'rounded-tl', 'rounded-tr', 'rounded-br', 'rounded-bl'],
	      'rounded-s': ['rounded-ss', 'rounded-es'],
	      'rounded-e': ['rounded-se', 'rounded-ee'],
	      'rounded-t': ['rounded-tl', 'rounded-tr'],
	      'rounded-r': ['rounded-tr', 'rounded-br'],
	      'rounded-b': ['rounded-br', 'rounded-bl'],
	      'rounded-l': ['rounded-tl', 'rounded-bl'],
	      'border-spacing': ['border-spacing-x', 'border-spacing-y'],
	      'border-w': ['border-w-s', 'border-w-e', 'border-w-t', 'border-w-r', 'border-w-b', 'border-w-l'],
	      'border-w-x': ['border-w-r', 'border-w-l'],
	      'border-w-y': ['border-w-t', 'border-w-b'],
	      'border-color': ['border-color-t', 'border-color-r', 'border-color-b', 'border-color-l'],
	      'border-color-x': ['border-color-r', 'border-color-l'],
	      'border-color-y': ['border-color-t', 'border-color-b'],
	      'scroll-m': ['scroll-mx', 'scroll-my', 'scroll-ms', 'scroll-me', 'scroll-mt', 'scroll-mr', 'scroll-mb', 'scroll-ml'],
	      'scroll-mx': ['scroll-mr', 'scroll-ml'],
	      'scroll-my': ['scroll-mt', 'scroll-mb'],
	      'scroll-p': ['scroll-px', 'scroll-py', 'scroll-ps', 'scroll-pe', 'scroll-pt', 'scroll-pr', 'scroll-pb', 'scroll-pl'],
	      'scroll-px': ['scroll-pr', 'scroll-pl'],
	      'scroll-py': ['scroll-pt', 'scroll-pb'],
	      touch: ['touch-x', 'touch-y', 'touch-pz'],
	      'touch-x': ['touch'],
	      'touch-y': ['touch'],
	      'touch-pz': ['touch']
	    },
	    conflictingClassGroupModifiers: {
	      'font-size': ['leading']
	    }
	  };
	}
	const twMerge = /*#__PURE__*/createTailwindMerge(getDefaultConfig);

	/**
	 * Animates the opacity of an element from 0 to the current opacity for `in` transitions and from the current opacity to 0 for `out` transitions.
	 *
	 * https://svelte.dev/docs/svelte-transition#fade
	 * @param {Element} node
	 * @param {import('./public').FadeParams} [params]
	 * @returns {import('./public').TransitionConfig}
	 */
	function fade(node, { delay = 0, duration = 400, easing = identity } = {}) {
		const o = +getComputedStyle(node).opacity;
		return {
			delay,
			duration,
			easing,
			css: (t) => `opacity: ${t * o}`
		};
	}

	/* node_modules/.pnpm/flowbite-svelte@0.46.1_svelte@4.2.17/node_modules/flowbite-svelte/dist/buttons/Button.svelte generated by Svelte v4.2.17 */
	const file$8 = "node_modules/.pnpm/flowbite-svelte@0.46.1_svelte@4.2.17/node_modules/flowbite-svelte/dist/buttons/Button.svelte";

	// (94:0) {:else}
	function create_else_block$2(ctx) {
		let previous_tag = /*tag*/ ctx[2];
		let svelte_element_anchor;
		let current;
		validate_dynamic_element(/*tag*/ ctx[2]);
		validate_void_dynamic_element(/*tag*/ ctx[2]);
		let svelte_element = /*tag*/ ctx[2] && create_dynamic_element(ctx);

		const block = {
			c: function create() {
				if (svelte_element) svelte_element.c();
				svelte_element_anchor = empty();
			},
			m: function mount(target, anchor) {
				if (svelte_element) svelte_element.m(target, anchor);
				insert_dev(target, svelte_element_anchor, anchor);
				current = true;
			},
			p: function update(ctx, dirty) {
				if (/*tag*/ ctx[2]) {
					if (!previous_tag) {
						svelte_element = create_dynamic_element(ctx);
						previous_tag = /*tag*/ ctx[2];
						svelte_element.c();
						svelte_element.m(svelte_element_anchor.parentNode, svelte_element_anchor);
					} else if (safe_not_equal(previous_tag, /*tag*/ ctx[2])) {
						svelte_element.d(1);
						validate_dynamic_element(/*tag*/ ctx[2]);
						validate_void_dynamic_element(/*tag*/ ctx[2]);
						svelte_element = create_dynamic_element(ctx);
						previous_tag = /*tag*/ ctx[2];
						svelte_element.c();
						svelte_element.m(svelte_element_anchor.parentNode, svelte_element_anchor);
					} else {
						svelte_element.p(ctx, dirty);
					}
				} else if (previous_tag) {
					svelte_element.d(1);
					svelte_element = null;
					previous_tag = /*tag*/ ctx[2];
				}
			},
			i: function intro(local) {
				if (current) return;
				transition_in(svelte_element, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(svelte_element, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(svelte_element_anchor);
				}

				if (svelte_element) svelte_element.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_else_block$2.name,
			type: "else",
			source: "(94:0) {:else}",
			ctx
		});

		return block;
	}

	// (90:53) 
	function create_if_block_1$3(ctx) {
		let button;
		let current;
		let mounted;
		let dispose;
		const default_slot_template = /*#slots*/ ctx[12].default;
		const default_slot = create_slot(default_slot_template, ctx, /*$$scope*/ ctx[11], null);

		let button_levels = [
			{ type: /*type*/ ctx[1] },
			/*$$restProps*/ ctx[4],
			{ class: /*buttonClass*/ ctx[3] }
		];

		let button_data = {};

		for (let i = 0; i < button_levels.length; i += 1) {
			button_data = assign(button_data, button_levels[i]);
		}

		const block = {
			c: function create() {
				button = element("button");
				if (default_slot) default_slot.c();
				set_attributes(button, button_data);
				add_location(button, file$8, 90, 2, 7718);
			},
			m: function mount(target, anchor) {
				insert_dev(target, button, anchor);

				if (default_slot) {
					default_slot.m(button, null);
				}

				if (button.autofocus) button.focus();
				current = true;

				if (!mounted) {
					dispose = [
						listen_dev(button, "click", /*click_handler_1*/ ctx[22], false, false, false, false),
						listen_dev(button, "change", /*change_handler_1*/ ctx[23], false, false, false, false),
						listen_dev(button, "keydown", /*keydown_handler_1*/ ctx[24], false, false, false, false),
						listen_dev(button, "keyup", /*keyup_handler_1*/ ctx[25], false, false, false, false),
						listen_dev(button, "touchstart", /*touchstart_handler_1*/ ctx[26], { passive: true }, false, false, false),
						listen_dev(button, "touchend", /*touchend_handler_1*/ ctx[27], false, false, false, false),
						listen_dev(button, "touchcancel", /*touchcancel_handler_1*/ ctx[28], false, false, false, false),
						listen_dev(button, "mouseenter", /*mouseenter_handler_1*/ ctx[29], false, false, false, false),
						listen_dev(button, "mouseleave", /*mouseleave_handler_1*/ ctx[30], false, false, false, false)
					];

					mounted = true;
				}
			},
			p: function update(ctx, dirty) {
				if (default_slot) {
					if (default_slot.p && (!current || dirty[0] & /*$$scope*/ 2048)) {
						update_slot_base(
							default_slot,
							default_slot_template,
							ctx,
							/*$$scope*/ ctx[11],
							!current
							? get_all_dirty_from_scope(/*$$scope*/ ctx[11])
							: get_slot_changes(default_slot_template, /*$$scope*/ ctx[11], dirty, null),
							null
						);
					}
				}

				set_attributes(button, button_data = get_spread_update(button_levels, [
					(!current || dirty[0] & /*type*/ 2) && { type: /*type*/ ctx[1] },
					dirty[0] & /*$$restProps*/ 16 && /*$$restProps*/ ctx[4],
					(!current || dirty[0] & /*buttonClass*/ 8) && { class: /*buttonClass*/ ctx[3] }
				]));
			},
			i: function intro(local) {
				if (current) return;
				transition_in(default_slot, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(default_slot, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(button);
				}

				if (default_slot) default_slot.d(detaching);
				mounted = false;
				run_all(dispose);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_1$3.name,
			type: "if",
			source: "(90:53) ",
			ctx
		});

		return block;
	}

	// (86:0) {#if href && !$$restProps.disabled}
	function create_if_block$5(ctx) {
		let a;
		let current;
		let mounted;
		let dispose;
		const default_slot_template = /*#slots*/ ctx[12].default;
		const default_slot = create_slot(default_slot_template, ctx, /*$$scope*/ ctx[11], null);

		let a_levels = [
			{ href: /*href*/ ctx[0] },
			/*$$restProps*/ ctx[4],
			{ class: /*buttonClass*/ ctx[3] },
			{ role: "button" }
		];

		let a_data = {};

		for (let i = 0; i < a_levels.length; i += 1) {
			a_data = assign(a_data, a_levels[i]);
		}

		const block = {
			c: function create() {
				a = element("a");
				if (default_slot) default_slot.c();
				set_attributes(a, a_data);
				add_location(a, file$8, 86, 2, 7464);
			},
			m: function mount(target, anchor) {
				insert_dev(target, a, anchor);

				if (default_slot) {
					default_slot.m(a, null);
				}

				current = true;

				if (!mounted) {
					dispose = [
						listen_dev(a, "click", /*click_handler*/ ctx[13], false, false, false, false),
						listen_dev(a, "change", /*change_handler*/ ctx[14], false, false, false, false),
						listen_dev(a, "keydown", /*keydown_handler*/ ctx[15], false, false, false, false),
						listen_dev(a, "keyup", /*keyup_handler*/ ctx[16], false, false, false, false),
						listen_dev(a, "touchstart", /*touchstart_handler*/ ctx[17], { passive: true }, false, false, false),
						listen_dev(a, "touchend", /*touchend_handler*/ ctx[18], false, false, false, false),
						listen_dev(a, "touchcancel", /*touchcancel_handler*/ ctx[19], false, false, false, false),
						listen_dev(a, "mouseenter", /*mouseenter_handler*/ ctx[20], false, false, false, false),
						listen_dev(a, "mouseleave", /*mouseleave_handler*/ ctx[21], false, false, false, false)
					];

					mounted = true;
				}
			},
			p: function update(ctx, dirty) {
				if (default_slot) {
					if (default_slot.p && (!current || dirty[0] & /*$$scope*/ 2048)) {
						update_slot_base(
							default_slot,
							default_slot_template,
							ctx,
							/*$$scope*/ ctx[11],
							!current
							? get_all_dirty_from_scope(/*$$scope*/ ctx[11])
							: get_slot_changes(default_slot_template, /*$$scope*/ ctx[11], dirty, null),
							null
						);
					}
				}

				set_attributes(a, a_data = get_spread_update(a_levels, [
					(!current || dirty[0] & /*href*/ 1) && { href: /*href*/ ctx[0] },
					dirty[0] & /*$$restProps*/ 16 && /*$$restProps*/ ctx[4],
					(!current || dirty[0] & /*buttonClass*/ 8) && { class: /*buttonClass*/ ctx[3] },
					{ role: "button" }
				]));
			},
			i: function intro(local) {
				if (current) return;
				transition_in(default_slot, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(default_slot, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(a);
				}

				if (default_slot) default_slot.d(detaching);
				mounted = false;
				run_all(dispose);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block$5.name,
			type: "if",
			source: "(86:0) {#if href && !$$restProps.disabled}",
			ctx
		});

		return block;
	}

	// (95:2) <svelte:element this={tag} class={buttonClass}>
	function create_dynamic_element(ctx) {
		let svelte_element;
		let current;
		const default_slot_template = /*#slots*/ ctx[12].default;
		const default_slot = create_slot(default_slot_template, ctx, /*$$scope*/ ctx[11], null);
		let svelte_element_levels = [{ class: /*buttonClass*/ ctx[3] }];
		let svelte_element_data = {};

		for (let i = 0; i < svelte_element_levels.length; i += 1) {
			svelte_element_data = assign(svelte_element_data, svelte_element_levels[i]);
		}

		const block = {
			c: function create() {
				svelte_element = element(/*tag*/ ctx[2]);
				if (default_slot) default_slot.c();
				set_dynamic_element_data(/*tag*/ ctx[2])(svelte_element, svelte_element_data);
				add_location(svelte_element, file$8, 94, 2, 7922);
			},
			m: function mount(target, anchor) {
				insert_dev(target, svelte_element, anchor);

				if (default_slot) {
					default_slot.m(svelte_element, null);
				}

				current = true;
			},
			p: function update(ctx, dirty) {
				if (default_slot) {
					if (default_slot.p && (!current || dirty[0] & /*$$scope*/ 2048)) {
						update_slot_base(
							default_slot,
							default_slot_template,
							ctx,
							/*$$scope*/ ctx[11],
							!current
							? get_all_dirty_from_scope(/*$$scope*/ ctx[11])
							: get_slot_changes(default_slot_template, /*$$scope*/ ctx[11], dirty, null),
							null
						);
					}
				}

				set_dynamic_element_data(/*tag*/ ctx[2])(svelte_element, svelte_element_data = get_spread_update(svelte_element_levels, [
					(!current || dirty[0] & /*buttonClass*/ 8) && { class: /*buttonClass*/ ctx[3] }
				]));
			},
			i: function intro(local) {
				if (current) return;
				transition_in(default_slot, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(default_slot, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(svelte_element);
				}

				if (default_slot) default_slot.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_dynamic_element.name,
			type: "child_dynamic_element",
			source: "(95:2) <svelte:element this={tag} class={buttonClass}>",
			ctx
		});

		return block;
	}

	function create_fragment$8(ctx) {
		let current_block_type_index;
		let if_block;
		let if_block_anchor;
		let current;
		const if_block_creators = [create_if_block$5, create_if_block_1$3, create_else_block$2];
		const if_blocks = [];

		function select_block_type(ctx, dirty) {
			if (/*href*/ ctx[0] && !/*$$restProps*/ ctx[4].disabled) return 0;
			if (/*tag*/ ctx[2] === 'button' && !/*$$restProps*/ ctx[4].disabled) return 1;
			return 2;
		}

		current_block_type_index = select_block_type(ctx);
		if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);

		const block = {
			c: function create() {
				if_block.c();
				if_block_anchor = empty();
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				if_blocks[current_block_type_index].m(target, anchor);
				insert_dev(target, if_block_anchor, anchor);
				current = true;
			},
			p: function update(ctx, dirty) {
				let previous_block_index = current_block_type_index;
				current_block_type_index = select_block_type(ctx);

				if (current_block_type_index === previous_block_index) {
					if_blocks[current_block_type_index].p(ctx, dirty);
				} else {
					group_outros();

					transition_out(if_blocks[previous_block_index], 1, 1, () => {
						if_blocks[previous_block_index] = null;
					});

					check_outros();
					if_block = if_blocks[current_block_type_index];

					if (!if_block) {
						if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
						if_block.c();
					} else {
						if_block.p(ctx, dirty);
					}

					transition_in(if_block, 1);
					if_block.m(if_block_anchor.parentNode, if_block_anchor);
				}
			},
			i: function intro(local) {
				if (current) return;
				transition_in(if_block);
				current = true;
			},
			o: function outro(local) {
				transition_out(if_block);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(if_block_anchor);
				}

				if_blocks[current_block_type_index].d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$8.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$8($$self, $$props, $$invalidate) {
		const omit_props_names = ["pill","outline","size","href","type","color","shadow","tag","checked"];
		let $$restProps = compute_rest_props($$props, omit_props_names);
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('Button', slots, ['default']);
		const group = getContext('group');
		let { pill = false } = $$props;
		let { outline = false } = $$props;
		let { size = group ? 'sm' : 'md' } = $$props;
		let { href = undefined } = $$props;
		let { type = 'button' } = $$props;
		let { color = group ? outline ? 'dark' : 'alternative' : 'primary' } = $$props;
		let { shadow = false } = $$props;
		let { tag = 'button' } = $$props;
		let { checked = undefined } = $$props;

		// export let disabled: boolean = false;
		const colorClasses = {
			alternative: 'text-gray-900 bg-white border border-gray-200 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-400 hover:text-primary-700 focus-within:text-primary-700 dark:focus-within:text-white dark:hover:text-white dark:hover:bg-gray-700',
			blue: 'text-white bg-blue-700 hover:bg-blue-800 dark:bg-blue-600 dark:hover:bg-blue-700',
			dark: 'text-white bg-gray-800 hover:bg-gray-900 dark:bg-gray-800 dark:hover:bg-gray-700',
			green: 'text-white bg-green-700 hover:bg-green-800 dark:bg-green-600 dark:hover:bg-green-700',
			light: 'text-gray-900 bg-white border border-gray-300 hover:bg-gray-100 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600',
			primary: 'text-white bg-primary-700 hover:bg-primary-800 dark:bg-primary-600 dark:hover:bg-primary-700',
			purple: 'text-white bg-purple-700 hover:bg-purple-800 dark:bg-purple-600 dark:hover:bg-purple-700',
			red: 'text-white bg-red-700 hover:bg-red-800 dark:bg-red-600 dark:hover:bg-red-700',
			yellow: 'text-white bg-yellow-400 hover:bg-yellow-500 ',
			none: ''
		};

		const colorCheckedClasses = {
			alternative: 'text-primary-700 border dark:text-primary-500 bg-gray-100 dark:bg-gray-700 border-gray-300 shadow-gray-300 dark:shadow-gray-800 shadow-inner',
			blue: 'text-blue-900 bg-blue-400 dark:bg-blue-500 shadow-blue-700 dark:shadow-blue-800 shadow-inner',
			dark: 'text-white bg-gray-500 dark:bg-gray-600 shadow-gray-800 dark:shadow-gray-900 shadow-inner',
			green: 'text-green-900 bg-green-400 dark:bg-green-500 shadow-green-700 dark:shadow-green-800 shadow-inner',
			light: 'text-gray-900 bg-gray-100 border border-gray-300 dark:bg-gray-500 dark:text-gray-900 dark:border-gray-700 shadow-gray-300 dark:shadow-gray-700 shadow-inner',
			primary: 'text-primary-900 bg-primary-400 dark:bg-primary-500 shadow-primary-700 dark:shadow-primary-800 shadow-inner',
			purple: 'text-purple-900 bg-purple-400 dark:bg-purple-500 shadow-purple-700 dark:shadow-purple-800 shadow-inner',
			red: 'text-red-900 bg-red-400 dark:bg-red-500 shadow-red-700 dark:shadow-red-800 shadow-inner',
			yellow: 'text-yellow-900 bg-yellow-300 dark:bg-yellow-400 shadow-yellow-500 dark:shadow-yellow-700 shadow-inner',
			none: ''
		};

		const coloredFocusClasses = {
			alternative: 'focus-within:ring-gray-200 dark:focus-within:ring-gray-700',
			blue: 'focus-within:ring-blue-300 dark:focus-within:ring-blue-800',
			dark: 'focus-within:ring-gray-300 dark:focus-within:ring-gray-700',
			green: 'focus-within:ring-green-300 dark:focus-within:ring-green-800',
			light: 'focus-within:ring-gray-200 dark:focus-within:ring-gray-700',
			primary: 'focus-within:ring-primary-300 dark:focus-within:ring-primary-800',
			purple: 'focus-within:ring-purple-300 dark:focus-within:ring-purple-900',
			red: 'focus-within:ring-red-300 dark:focus-within:ring-red-900',
			yellow: 'focus-within:ring-yellow-300 dark:focus-within:ring-yellow-900',
			none: ''
		};

		const coloredShadowClasses = {
			alternative: 'shadow-gray-500/50 dark:shadow-gray-800/80',
			blue: 'shadow-blue-500/50 dark:shadow-blue-800/80',
			dark: 'shadow-gray-500/50 dark:shadow-gray-800/80',
			green: 'shadow-green-500/50 dark:shadow-green-800/80',
			light: 'shadow-gray-500/50 dark:shadow-gray-800/80',
			primary: 'shadow-primary-500/50 dark:shadow-primary-800/80',
			purple: 'shadow-purple-500/50 dark:shadow-purple-800/80',
			red: 'shadow-red-500/50 dark:shadow-red-800/80 ',
			yellow: 'shadow-yellow-500/50 dark:shadow-yellow-800/80 ',
			none: ''
		};

		const outlineClasses = {
			alternative: 'text-gray-900 dark:text-gray-400 hover:text-white border border-gray-800 hover:bg-gray-900 focus-within:bg-gray-900 focus-within:text-white focus-within:ring-gray-300 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-600 dark:focus-within:ring-gray-800',
			blue: 'text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-600',
			dark: 'text-gray-900 hover:text-white border border-gray-800 hover:bg-gray-900 focus-within:bg-gray-900 focus-within:text-white dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-600',
			green: 'text-green-700 hover:text-white border border-green-700 hover:bg-green-800 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600',
			light: 'text-gray-500 hover:text-gray-900 bg-white border border-gray-200 dark:border-gray-600 dark:hover:text-white dark:text-gray-400 hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-600',
			primary: 'text-primary-700 hover:text-white border border-primary-700 hover:bg-primary-700 dark:border-primary-500 dark:text-primary-500 dark:hover:text-white dark:hover:bg-primary-600',
			purple: 'text-purple-700 hover:text-white border border-purple-700 hover:bg-purple-800 dark:border-purple-400 dark:text-purple-400 dark:hover:text-white dark:hover:bg-purple-500',
			red: 'text-red-700 hover:text-white border border-red-700 hover:bg-red-800 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600',
			yellow: 'text-yellow-400 hover:text-white border border-yellow-400 hover:bg-yellow-500 dark:border-yellow-300 dark:text-yellow-300 dark:hover:text-white dark:hover:bg-yellow-400',
			none: ''
		};

		const sizeClasses = {
			xs: 'px-3 py-2 text-xs',
			sm: 'px-4 py-2 text-sm',
			md: 'px-5 py-2.5 text-sm',
			lg: 'px-5 py-3 text-base',
			xl: 'px-6 py-3.5 text-base'
		};

		const hasBorder = () => outline || color === 'alternative' || color === 'light';
		let buttonClass;

		function click_handler(event) {
			bubble.call(this, $$self, event);
		}

		function change_handler(event) {
			bubble.call(this, $$self, event);
		}

		function keydown_handler(event) {
			bubble.call(this, $$self, event);
		}

		function keyup_handler(event) {
			bubble.call(this, $$self, event);
		}

		function touchstart_handler(event) {
			bubble.call(this, $$self, event);
		}

		function touchend_handler(event) {
			bubble.call(this, $$self, event);
		}

		function touchcancel_handler(event) {
			bubble.call(this, $$self, event);
		}

		function mouseenter_handler(event) {
			bubble.call(this, $$self, event);
		}

		function mouseleave_handler(event) {
			bubble.call(this, $$self, event);
		}

		function click_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function change_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function keydown_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function keyup_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function touchstart_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function touchend_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function touchcancel_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function mouseenter_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		function mouseleave_handler_1(event) {
			bubble.call(this, $$self, event);
		}

		$$self.$$set = $$new_props => {
			$$invalidate(39, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
			$$invalidate(4, $$restProps = compute_rest_props($$props, omit_props_names));
			if ('pill' in $$new_props) $$invalidate(5, pill = $$new_props.pill);
			if ('outline' in $$new_props) $$invalidate(6, outline = $$new_props.outline);
			if ('size' in $$new_props) $$invalidate(7, size = $$new_props.size);
			if ('href' in $$new_props) $$invalidate(0, href = $$new_props.href);
			if ('type' in $$new_props) $$invalidate(1, type = $$new_props.type);
			if ('color' in $$new_props) $$invalidate(8, color = $$new_props.color);
			if ('shadow' in $$new_props) $$invalidate(9, shadow = $$new_props.shadow);
			if ('tag' in $$new_props) $$invalidate(2, tag = $$new_props.tag);
			if ('checked' in $$new_props) $$invalidate(10, checked = $$new_props.checked);
			if ('$$scope' in $$new_props) $$invalidate(11, $$scope = $$new_props.$$scope);
		};

		$$self.$capture_state = () => ({
			twMerge,
			getContext,
			group,
			pill,
			outline,
			size,
			href,
			type,
			color,
			shadow,
			tag,
			checked,
			colorClasses,
			colorCheckedClasses,
			coloredFocusClasses,
			coloredShadowClasses,
			outlineClasses,
			sizeClasses,
			hasBorder,
			buttonClass
		});

		$$self.$inject_state = $$new_props => {
			$$invalidate(39, $$props = assign(assign({}, $$props), $$new_props));
			if ('pill' in $$props) $$invalidate(5, pill = $$new_props.pill);
			if ('outline' in $$props) $$invalidate(6, outline = $$new_props.outline);
			if ('size' in $$props) $$invalidate(7, size = $$new_props.size);
			if ('href' in $$props) $$invalidate(0, href = $$new_props.href);
			if ('type' in $$props) $$invalidate(1, type = $$new_props.type);
			if ('color' in $$props) $$invalidate(8, color = $$new_props.color);
			if ('shadow' in $$props) $$invalidate(9, shadow = $$new_props.shadow);
			if ('tag' in $$props) $$invalidate(2, tag = $$new_props.tag);
			if ('checked' in $$props) $$invalidate(10, checked = $$new_props.checked);
			if ('buttonClass' in $$props) $$invalidate(3, buttonClass = $$new_props.buttonClass);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		$$self.$$.update = () => {
			$$invalidate(3, buttonClass = twMerge(
				'text-center font-medium',
				group ? 'focus-within:ring-2' : 'focus-within:ring-4',
				group && 'focus-within:z-10',
				group || 'focus-within:outline-none',
				'inline-flex items-center justify-center ' + sizeClasses[size],
				outline && checked && 'border dark:border-gray-900',
				outline && checked && colorCheckedClasses[color],
				outline && !checked && outlineClasses[color],
				!outline && checked && colorCheckedClasses[color],
				!outline && !checked && colorClasses[color],
				color === 'alternative' && (group && !checked
				? 'dark:bg-gray-700 dark:text-white dark:border-gray-700 dark:hover:border-gray-600 dark:hover:bg-gray-600'
				: 'dark:bg-transparent dark:border-gray-600 dark:hover:border-gray-600'),
				outline && color === 'dark' && (group
				? checked
					? 'bg-gray-900 border-gray-800 dark:border-white dark:bg-gray-600'
					: 'dark:text-white border-gray-800 dark:border-white'
				: 'dark:text-gray-400 dark:border-gray-700'),
				coloredFocusClasses[color],
				hasBorder() && group && 'border-s-0 first:border-s',
				group
				? pill && 'first:rounded-s-full last:rounded-e-full' || 'first:rounded-s-lg last:rounded-e-lg'
				: pill && 'rounded-full' || 'rounded-lg',
				shadow && 'shadow-lg',
				shadow && coloredShadowClasses[color],
				$$restProps.disabled && 'cursor-not-allowed opacity-50',
				$$props.class
			));
		};

		$$props = exclude_internal_props($$props);

		return [
			href,
			type,
			tag,
			buttonClass,
			$$restProps,
			pill,
			outline,
			size,
			color,
			shadow,
			checked,
			$$scope,
			slots,
			click_handler,
			change_handler,
			keydown_handler,
			keyup_handler,
			touchstart_handler,
			touchend_handler,
			touchcancel_handler,
			mouseenter_handler,
			mouseleave_handler,
			click_handler_1,
			change_handler_1,
			keydown_handler_1,
			keyup_handler_1,
			touchstart_handler_1,
			touchend_handler_1,
			touchcancel_handler_1,
			mouseenter_handler_1,
			mouseleave_handler_1
		];
	}

	class Button extends SvelteComponentDev {
		constructor(options) {
			super(options);

			init(
				this,
				options,
				instance$8,
				create_fragment$8,
				safe_not_equal,
				{
					pill: 5,
					outline: 6,
					size: 7,
					href: 0,
					type: 1,
					color: 8,
					shadow: 9,
					tag: 2,
					checked: 10
				},
				null,
				[-1, -1]
			);

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "Button",
				options,
				id: create_fragment$8.name
			});
		}

		get pill() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set pill(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get outline() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set outline(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get size() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set size(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get href() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set href(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get type() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set type(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get color() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set color(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get shadow() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set shadow(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get tag() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set tag(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get checked() {
			throw new Error("<Button>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set checked(value) {
			throw new Error("<Button>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}
	}

	/* node_modules/.pnpm/flowbite-svelte@0.46.1_svelte@4.2.17/node_modules/flowbite-svelte/dist/timeline/Timeline.svelte generated by Svelte v4.2.17 */
	const file$7 = "node_modules/.pnpm/flowbite-svelte@0.46.1_svelte@4.2.17/node_modules/flowbite-svelte/dist/timeline/Timeline.svelte";

	function create_fragment$7(ctx) {
		let ol;
		let ol_class_value;
		let current;
		const default_slot_template = /*#slots*/ ctx[4].default;
		const default_slot = create_slot(default_slot_template, ctx, /*$$scope*/ ctx[3], null);

		const block = {
			c: function create() {
				ol = element("ol");
				if (default_slot) default_slot.c();
				attr_dev(ol, "class", ol_class_value = twMerge(/*olClasses*/ ctx[1][/*order*/ ctx[0]], /*$$props*/ ctx[2].class));
				add_location(ol, file$7, 13, 0, 524);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				insert_dev(target, ol, anchor);

				if (default_slot) {
					default_slot.m(ol, null);
				}

				current = true;
			},
			p: function update(ctx, [dirty]) {
				if (default_slot) {
					if (default_slot.p && (!current || dirty & /*$$scope*/ 8)) {
						update_slot_base(
							default_slot,
							default_slot_template,
							ctx,
							/*$$scope*/ ctx[3],
							!current
							? get_all_dirty_from_scope(/*$$scope*/ ctx[3])
							: get_slot_changes(default_slot_template, /*$$scope*/ ctx[3], dirty, null),
							null
						);
					}
				}

				if (!current || dirty & /*order, $$props*/ 5 && ol_class_value !== (ol_class_value = twMerge(/*olClasses*/ ctx[1][/*order*/ ctx[0]], /*$$props*/ ctx[2].class))) {
					attr_dev(ol, "class", ol_class_value);
				}
			},
			i: function intro(local) {
				if (current) return;
				transition_in(default_slot, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(default_slot, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(ol);
				}

				if (default_slot) default_slot.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$7.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$7($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('Timeline', slots, ['default']);
		let { order = 'default' } = $$props;
		setContext('order', order);

		let olClasses = {
			group: 'p-5 mb-4 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700',
			horizontal: 'sm:flex',
			activity: 'relative border-s border-gray-200 dark:border-gray-700',
			vertical: 'relative border-s border-gray-200 dark:border-gray-700',
			default: 'relative border-s border-gray-200 dark:border-gray-700'
		};

		$$self.$$set = $$new_props => {
			$$invalidate(2, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
			if ('order' in $$new_props) $$invalidate(0, order = $$new_props.order);
			if ('$$scope' in $$new_props) $$invalidate(3, $$scope = $$new_props.$$scope);
		};

		$$self.$capture_state = () => ({ twMerge, setContext, order, olClasses });

		$$self.$inject_state = $$new_props => {
			$$invalidate(2, $$props = assign(assign({}, $$props), $$new_props));
			if ('order' in $$props) $$invalidate(0, order = $$new_props.order);
			if ('olClasses' in $$props) $$invalidate(1, olClasses = $$new_props.olClasses);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		$$props = exclude_internal_props($$props);
		return [order, olClasses, $$props, $$scope, slots];
	}

	class Timeline extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$7, create_fragment$7, safe_not_equal, { order: 0 });

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "Timeline",
				options,
				id: create_fragment$7.name
			});
		}

		get order() {
			throw new Error("<Timeline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set order(value) {
			throw new Error("<Timeline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}
	}

	/* node_modules/.pnpm/flowbite-svelte@0.46.1_svelte@4.2.17/node_modules/flowbite-svelte/dist/timeline/TimelineItem.svelte generated by Svelte v4.2.17 */
	const file$6 = "node_modules/.pnpm/flowbite-svelte@0.46.1_svelte@4.2.17/node_modules/flowbite-svelte/dist/timeline/TimelineItem.svelte";
	const get_icon_slot_changes = dirty => ({});
	const get_icon_slot_context = ctx => ({});

	// (43:17) 
	function create_if_block_4$1(ctx) {
		let time;
		let t;

		const block = {
			c: function create() {
				time = element("time");
				t = text(/*date*/ ctx[1]);
				attr_dev(time, "class", /*timeCls*/ ctx[6]);
				add_location(time, file$6, 43, 4, 2346);
			},
			m: function mount(target, anchor) {
				insert_dev(target, time, anchor);
				append_dev(time, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*date*/ 2) set_data_dev(t, /*date*/ ctx[1]);
			},
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(time);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_4$1.name,
			type: "if",
			source: "(43:17) ",
			ctx
		});

		return block;
	}

	// (37:2) {#if order !== 'default'}
	function create_if_block_3$2(ctx) {
		let current;
		const icon_slot_template = /*#slots*/ ctx[9].icon;
		const icon_slot = create_slot(icon_slot_template, ctx, /*$$scope*/ ctx[8], get_icon_slot_context);
		const icon_slot_or_fallback = icon_slot || fallback_block(ctx);

		const block = {
			c: function create() {
				if (icon_slot_or_fallback) icon_slot_or_fallback.c();
			},
			m: function mount(target, anchor) {
				if (icon_slot_or_fallback) {
					icon_slot_or_fallback.m(target, anchor);
				}

				current = true;
			},
			p: function update(ctx, dirty) {
				if (icon_slot) {
					if (icon_slot.p && (!current || dirty & /*$$scope*/ 256)) {
						update_slot_base(
							icon_slot,
							icon_slot_template,
							ctx,
							/*$$scope*/ ctx[8],
							!current
							? get_all_dirty_from_scope(/*$$scope*/ ctx[8])
							: get_slot_changes(icon_slot_template, /*$$scope*/ ctx[8], dirty, get_icon_slot_changes),
							get_icon_slot_context
						);
					}
				} else {
					if (icon_slot_or_fallback && icon_slot_or_fallback.p && (!current || dirty & /*svgClass*/ 4)) {
						icon_slot_or_fallback.p(ctx, !current ? -1 : dirty);
					}
				}
			},
			i: function intro(local) {
				if (current) return;
				transition_in(icon_slot_or_fallback, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(icon_slot_or_fallback, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (icon_slot_or_fallback) icon_slot_or_fallback.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_3$2.name,
			type: "if",
			source: "(37:2) {#if order !== 'default'}",
			ctx
		});

		return block;
	}

	// (38:22)        
	function fallback_block(ctx) {
		let svg;
		let path;

		const block = {
			c: function create() {
				svg = svg_element("svg");
				path = svg_element("path");
				attr_dev(path, "fill-rule", "evenodd");
				attr_dev(path, "d", "M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z");
				attr_dev(path, "clip-rule", "evenodd");
				add_location(path, file$6, 39, 8, 2095);
				attr_dev(svg, "aria-hidden", "true");
				attr_dev(svg, "class", /*svgClass*/ ctx[2]);
				attr_dev(svg, "fill", "currentColor");
				attr_dev(svg, "viewBox", "0 0 20 20");
				attr_dev(svg, "xmlns", "http://www.w3.org/2000/svg");
				add_location(svg, file$6, 38, 6, 1970);
			},
			m: function mount(target, anchor) {
				insert_dev(target, svg, anchor);
				append_dev(svg, path);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*svgClass*/ 4) {
					attr_dev(svg, "class", /*svgClass*/ ctx[2]);
				}
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(svg);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: fallback_block.name,
			type: "fallback",
			source: "(38:22)        ",
			ctx
		});

		return block;
	}

	// (47:2) {#if title}
	function create_if_block_2$2(ctx) {
		let h3;
		let t;

		const block = {
			c: function create() {
				h3 = element("h3");
				t = text(/*title*/ ctx[0]);
				attr_dev(h3, "class", /*h3Cls*/ ctx[7]);
				add_location(h3, file$6, 47, 4, 2409);
			},
			m: function mount(target, anchor) {
				insert_dev(target, h3, anchor);
				append_dev(h3, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*title*/ 1) set_data_dev(t, /*title*/ ctx[0]);
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(h3);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_2$2.name,
			type: "if",
			source: "(47:2) {#if title}",
			ctx
		});

		return block;
	}

	// (53:2) {#if order !== 'default'}
	function create_if_block$4(ctx) {
		let if_block_anchor;
		let if_block = /*date*/ ctx[1] && create_if_block_1$2(ctx);

		const block = {
			c: function create() {
				if (if_block) if_block.c();
				if_block_anchor = empty();
			},
			m: function mount(target, anchor) {
				if (if_block) if_block.m(target, anchor);
				insert_dev(target, if_block_anchor, anchor);
			},
			p: function update(ctx, dirty) {
				if (/*date*/ ctx[1]) {
					if (if_block) {
						if_block.p(ctx, dirty);
					} else {
						if_block = create_if_block_1$2(ctx);
						if_block.c();
						if_block.m(if_block_anchor.parentNode, if_block_anchor);
					}
				} else if (if_block) {
					if_block.d(1);
					if_block = null;
				}
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(if_block_anchor);
				}

				if (if_block) if_block.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block$4.name,
			type: "if",
			source: "(53:2) {#if order !== 'default'}",
			ctx
		});

		return block;
	}

	// (54:4) {#if date}
	function create_if_block_1$2(ctx) {
		let time;
		let t;

		const block = {
			c: function create() {
				time = element("time");
				t = text(/*date*/ ctx[1]);
				attr_dev(time, "class", /*timeCls*/ ctx[6]);
				add_location(time, file$6, 54, 6, 2510);
			},
			m: function mount(target, anchor) {
				insert_dev(target, time, anchor);
				append_dev(time, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*date*/ 2) set_data_dev(t, /*date*/ ctx[1]);
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(time);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_1$2.name,
			type: "if",
			source: "(54:4) {#if date}",
			ctx
		});

		return block;
	}

	function create_fragment$6(ctx) {
		let li;
		let div;
		let t0;
		let current_block_type_index;
		let if_block0;
		let t1;
		let t2;
		let t3;
		let current;
		const if_block_creators = [create_if_block_3$2, create_if_block_4$1];
		const if_blocks = [];

		function select_block_type(ctx, dirty) {
			if (/*order*/ ctx[3] !== 'default') return 0;
			if (/*date*/ ctx[1]) return 1;
			return -1;
		}

		if (~(current_block_type_index = select_block_type(ctx))) {
			if_block0 = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
		}

		let if_block1 = /*title*/ ctx[0] && create_if_block_2$2(ctx);
		let if_block2 = /*order*/ ctx[3] !== 'default' && create_if_block$4(ctx);
		const default_slot_template = /*#slots*/ ctx[9].default;
		const default_slot = create_slot(default_slot_template, ctx, /*$$scope*/ ctx[8], null);

		const block = {
			c: function create() {
				li = element("li");
				div = element("div");
				t0 = space();
				if (if_block0) if_block0.c();
				t1 = space();
				if (if_block1) if_block1.c();
				t2 = space();
				if (if_block2) if_block2.c();
				t3 = space();
				if (default_slot) default_slot.c();
				attr_dev(div, "class", /*divCls*/ ctx[5]);
				add_location(div, file$6, 35, 2, 1890);
				attr_dev(li, "class", /*liCls*/ ctx[4]);
				add_location(li, file$6, 34, 0, 1869);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				insert_dev(target, li, anchor);
				append_dev(li, div);
				append_dev(li, t0);

				if (~current_block_type_index) {
					if_blocks[current_block_type_index].m(li, null);
				}

				append_dev(li, t1);
				if (if_block1) if_block1.m(li, null);
				append_dev(li, t2);
				if (if_block2) if_block2.m(li, null);
				append_dev(li, t3);

				if (default_slot) {
					default_slot.m(li, null);
				}

				current = true;
			},
			p: function update(ctx, [dirty]) {
				let previous_block_index = current_block_type_index;
				current_block_type_index = select_block_type(ctx);

				if (current_block_type_index === previous_block_index) {
					if (~current_block_type_index) {
						if_blocks[current_block_type_index].p(ctx, dirty);
					}
				} else {
					if (if_block0) {
						group_outros();

						transition_out(if_blocks[previous_block_index], 1, 1, () => {
							if_blocks[previous_block_index] = null;
						});

						check_outros();
					}

					if (~current_block_type_index) {
						if_block0 = if_blocks[current_block_type_index];

						if (!if_block0) {
							if_block0 = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
							if_block0.c();
						} else {
							if_block0.p(ctx, dirty);
						}

						transition_in(if_block0, 1);
						if_block0.m(li, t1);
					} else {
						if_block0 = null;
					}
				}

				if (/*title*/ ctx[0]) {
					if (if_block1) {
						if_block1.p(ctx, dirty);
					} else {
						if_block1 = create_if_block_2$2(ctx);
						if_block1.c();
						if_block1.m(li, t2);
					}
				} else if (if_block1) {
					if_block1.d(1);
					if_block1 = null;
				}

				if (/*order*/ ctx[3] !== 'default') {
					if (if_block2) {
						if_block2.p(ctx, dirty);
					} else {
						if_block2 = create_if_block$4(ctx);
						if_block2.c();
						if_block2.m(li, t3);
					}
				} else if (if_block2) {
					if_block2.d(1);
					if_block2 = null;
				}

				if (default_slot) {
					if (default_slot.p && (!current || dirty & /*$$scope*/ 256)) {
						update_slot_base(
							default_slot,
							default_slot_template,
							ctx,
							/*$$scope*/ ctx[8],
							!current
							? get_all_dirty_from_scope(/*$$scope*/ ctx[8])
							: get_slot_changes(default_slot_template, /*$$scope*/ ctx[8], dirty, null),
							null
						);
					}
				}
			},
			i: function intro(local) {
				if (current) return;
				transition_in(if_block0);
				transition_in(default_slot, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(if_block0);
				transition_out(default_slot, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(li);
				}

				if (~current_block_type_index) {
					if_blocks[current_block_type_index].d();
				}

				if (if_block1) if_block1.d();
				if (if_block2) if_block2.d();
				if (default_slot) default_slot.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$6.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$6($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('TimelineItem', slots, ['icon','default']);
		let { title = '' } = $$props;
		let { date = '' } = $$props;
		let { svgClass = 'w-3 h-3 text-primary-600 dark:text-primary-400' } = $$props;
		let order = 'default';
		order = getContext('order');

		const liClasses = {
			default: 'mb-10 ms-4',
			vertical: 'mb-10 ms-6',
			horizontal: 'relative mb-6 sm:mb-0',
			activity: 'mb-10 ms-6',
			group: ''
		};

		const divClasses = {
			default: 'absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700',
			vertical: 'flex absolute -start-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900',
			horizontal: 'flex items-center',
			activity: 'flex absolute -start-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900',
			group: 'p-5 mb-4 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700'
		};

		const timeClasses = {
			default: 'mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500',
			vertical: 'block mb-2 text-sm font-normal leading-none text-gray-400 dark:text-gray-500',
			horizontal: 'block mb-2 text-sm font-normal leading-none text-gray-400 dark:text-gray-500',
			activity: 'mb-1 text-xs font-normal text-gray-400 sm:order-last sm:mb-0',
			group: 'text-lg font-semibold text-gray-900 dark:text-white'
		};

		let liCls = twMerge(liClasses[order], $$props.classLi);
		let divCls = twMerge(divClasses[order], $$props.classDiv);
		let timeCls = twMerge(timeClasses[order], $$props.classTime);

		const h3Cls = twMerge(
			order === 'vertical'
			? 'flex items-center mb-1 text-lg font-semibold text-gray-900 dark:text-white'
			: 'text-lg font-semibold text-gray-900 dark:text-white',
			$$props.classH3
		);

		$$self.$$set = $$new_props => {
			$$invalidate(13, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
			if ('title' in $$new_props) $$invalidate(0, title = $$new_props.title);
			if ('date' in $$new_props) $$invalidate(1, date = $$new_props.date);
			if ('svgClass' in $$new_props) $$invalidate(2, svgClass = $$new_props.svgClass);
			if ('$$scope' in $$new_props) $$invalidate(8, $$scope = $$new_props.$$scope);
		};

		$$self.$capture_state = () => ({
			twMerge,
			getContext,
			title,
			date,
			svgClass,
			order,
			liClasses,
			divClasses,
			timeClasses,
			liCls,
			divCls,
			timeCls,
			h3Cls
		});

		$$self.$inject_state = $$new_props => {
			$$invalidate(13, $$props = assign(assign({}, $$props), $$new_props));
			if ('title' in $$props) $$invalidate(0, title = $$new_props.title);
			if ('date' in $$props) $$invalidate(1, date = $$new_props.date);
			if ('svgClass' in $$props) $$invalidate(2, svgClass = $$new_props.svgClass);
			if ('order' in $$props) $$invalidate(3, order = $$new_props.order);
			if ('liCls' in $$props) $$invalidate(4, liCls = $$new_props.liCls);
			if ('divCls' in $$props) $$invalidate(5, divCls = $$new_props.divCls);
			if ('timeCls' in $$props) $$invalidate(6, timeCls = $$new_props.timeCls);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		$$props = exclude_internal_props($$props);
		return [title, date, svgClass, order, liCls, divCls, timeCls, h3Cls, $$scope, slots];
	}

	class TimelineItem extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$6, create_fragment$6, safe_not_equal, { title: 0, date: 1, svgClass: 2 });

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "TimelineItem",
				options,
				id: create_fragment$6.name
			});
		}

		get title() {
			throw new Error("<TimelineItem>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set title(value) {
			throw new Error("<TimelineItem>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get date() {
			throw new Error("<TimelineItem>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set date(value) {
			throw new Error("<TimelineItem>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get svgClass() {
			throw new Error("<TimelineItem>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set svgClass(value) {
			throw new Error("<TimelineItem>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}
	}

	/* node_modules/.pnpm/flowbite-svelte-icons@1.6.1_svelte@4.2.17_tailwind-merge@2.3.0_tailwindcss@3.4.3/node_modules/flowbite-svelte-icons/dist/ArrowRightOutline.svelte generated by Svelte v4.2.17 */
	const file$5 = "node_modules/.pnpm/flowbite-svelte-icons@1.6.1_svelte@4.2.17_tailwind-merge@2.3.0_tailwindcss@3.4.3/node_modules/flowbite-svelte-icons/dist/ArrowRightOutline.svelte";

	// (64:0) {:else}
	function create_else_block$1(ctx) {
		let svg;
		let if_block0_anchor;
		let path;
		let svg_class_value;
		let svg_aria_describedby_value;
		let if_block0 = /*title*/ ctx[4].id && /*title*/ ctx[4].title && create_if_block_4(ctx);
		let if_block1 = /*desc*/ ctx[6].id && /*desc*/ ctx[6].desc && create_if_block_3$1(ctx);

		let svg_levels = [
			{ xmlns: "http://www.w3.org/2000/svg" },
			{ fill: "none" },
			{ color: /*color*/ ctx[2] },
			/*$$restProps*/ ctx[11],
			{
				class: svg_class_value = twMerge('shrink-0', /*sizes*/ ctx[9][/*size*/ ctx[0] ?? 'md'], /*$$props*/ ctx[12].class)
			},
			{ role: /*role*/ ctx[1] },
			{ "aria-label": /*ariaLabel*/ ctx[7] },
			{
				"aria-describedby": svg_aria_describedby_value = /*hasDescription*/ ctx[8]
				? /*ariaDescribedby*/ ctx[10]
				: undefined
			},
			{ viewBox: "0 0 24 24" }
		];

		let svg_data = {};

		for (let i = 0; i < svg_levels.length; i += 1) {
			svg_data = assign(svg_data, svg_levels[i]);
		}

		const block = {
			c: function create() {
				svg = svg_element("svg");
				if (if_block0) if_block0.c();
				if_block0_anchor = empty();
				if (if_block1) if_block1.c();
				path = svg_element("path");
				attr_dev(path, "stroke", "currentColor");
				attr_dev(path, "stroke-linecap", "round");
				attr_dev(path, "stroke-linejoin", "round");
				attr_dev(path, "stroke-width", /*strokeWidth*/ ctx[5]);
				attr_dev(path, "d", "M19 12H5m14 0-4 4m4-4-4-4");
				add_location(path, file$5, 81, 4, 2042);
				set_svg_attributes(svg, svg_data);
				add_location(svg, file$5, 64, 2, 1565);
			},
			m: function mount(target, anchor) {
				insert_dev(target, svg, anchor);
				if (if_block0) if_block0.m(svg, null);
				append_dev(svg, if_block0_anchor);
				if (if_block1) if_block1.m(svg, null);
				append_dev(svg, path);
			},
			p: function update(ctx, dirty) {
				if (/*title*/ ctx[4].id && /*title*/ ctx[4].title) {
					if (if_block0) {
						if_block0.p(ctx, dirty);
					} else {
						if_block0 = create_if_block_4(ctx);
						if_block0.c();
						if_block0.m(svg, if_block0_anchor);
					}
				} else if (if_block0) {
					if_block0.d(1);
					if_block0 = null;
				}

				if (/*desc*/ ctx[6].id && /*desc*/ ctx[6].desc) {
					if (if_block1) {
						if_block1.p(ctx, dirty);
					} else {
						if_block1 = create_if_block_3$1(ctx);
						if_block1.c();
						if_block1.m(svg, path);
					}
				} else if (if_block1) {
					if_block1.d(1);
					if_block1 = null;
				}

				if (dirty & /*strokeWidth*/ 32) {
					attr_dev(path, "stroke-width", /*strokeWidth*/ ctx[5]);
				}

				set_svg_attributes(svg, svg_data = get_spread_update(svg_levels, [
					{ xmlns: "http://www.w3.org/2000/svg" },
					{ fill: "none" },
					dirty & /*color*/ 4 && { color: /*color*/ ctx[2] },
					dirty & /*$$restProps*/ 2048 && /*$$restProps*/ ctx[11],
					dirty & /*size, $$props*/ 4097 && svg_class_value !== (svg_class_value = twMerge('shrink-0', /*sizes*/ ctx[9][/*size*/ ctx[0] ?? 'md'], /*$$props*/ ctx[12].class)) && { class: svg_class_value },
					dirty & /*role*/ 2 && { role: /*role*/ ctx[1] },
					dirty & /*ariaLabel*/ 128 && { "aria-label": /*ariaLabel*/ ctx[7] },
					dirty & /*hasDescription*/ 256 && svg_aria_describedby_value !== (svg_aria_describedby_value = /*hasDescription*/ ctx[8]
					? /*ariaDescribedby*/ ctx[10]
					: undefined) && {
						"aria-describedby": svg_aria_describedby_value
					},
					{ viewBox: "0 0 24 24" }
				]));
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(svg);
				}

				if (if_block0) if_block0.d();
				if (if_block1) if_block1.d();
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_else_block$1.name,
			type: "else",
			source: "(64:0) {:else}",
			ctx
		});

		return block;
	}

	// (29:0) {#if withEvents}
	function create_if_block$3(ctx) {
		let svg;
		let if_block0_anchor;
		let path;
		let svg_class_value;
		let svg_aria_describedby_value;
		let mounted;
		let dispose;
		let if_block0 = /*title*/ ctx[4].id && /*title*/ ctx[4].title && create_if_block_2$1(ctx);
		let if_block1 = /*desc*/ ctx[6].id && /*desc*/ ctx[6].desc && create_if_block_1$1(ctx);

		let svg_levels = [
			{ xmlns: "http://www.w3.org/2000/svg" },
			{ fill: "none" },
			{ color: /*color*/ ctx[2] },
			/*$$restProps*/ ctx[11],
			{
				class: svg_class_value = twMerge('shrink-0', /*sizes*/ ctx[9][/*size*/ ctx[0] ?? 'md'], /*$$props*/ ctx[12].class)
			},
			{ role: /*role*/ ctx[1] },
			{ "aria-label": /*ariaLabel*/ ctx[7] },
			{
				"aria-describedby": svg_aria_describedby_value = /*hasDescription*/ ctx[8]
				? /*ariaDescribedby*/ ctx[10]
				: undefined
			},
			{ viewBox: "0 0 24 24" }
		];

		let svg_data = {};

		for (let i = 0; i < svg_levels.length; i += 1) {
			svg_data = assign(svg_data, svg_levels[i]);
		}

		const block = {
			c: function create() {
				svg = svg_element("svg");
				if (if_block0) if_block0.c();
				if_block0_anchor = empty();
				if (if_block1) if_block1.c();
				path = svg_element("path");
				attr_dev(path, "stroke", "currentColor");
				attr_dev(path, "stroke-linecap", "round");
				attr_dev(path, "stroke-linejoin", "round");
				attr_dev(path, "stroke-width", /*strokeWidth*/ ctx[5]);
				attr_dev(path, "d", "M19 12H5m14 0-4 4m4-4-4-4");
				add_location(path, file$5, 55, 4, 1377);
				set_svg_attributes(svg, svg_data);
				add_location(svg, file$5, 29, 2, 765);
			},
			m: function mount(target, anchor) {
				insert_dev(target, svg, anchor);
				if (if_block0) if_block0.m(svg, null);
				append_dev(svg, if_block0_anchor);
				if (if_block1) if_block1.m(svg, null);
				append_dev(svg, path);

				if (!mounted) {
					dispose = [
						listen_dev(svg, "click", /*click_handler*/ ctx[13], false, false, false, false),
						listen_dev(svg, "keydown", /*keydown_handler*/ ctx[14], false, false, false, false),
						listen_dev(svg, "keyup", /*keyup_handler*/ ctx[15], false, false, false, false),
						listen_dev(svg, "focus", /*focus_handler*/ ctx[16], false, false, false, false),
						listen_dev(svg, "blur", /*blur_handler*/ ctx[17], false, false, false, false),
						listen_dev(svg, "mouseenter", /*mouseenter_handler*/ ctx[18], false, false, false, false),
						listen_dev(svg, "mouseleave", /*mouseleave_handler*/ ctx[19], false, false, false, false),
						listen_dev(svg, "mouseover", /*mouseover_handler*/ ctx[20], false, false, false, false),
						listen_dev(svg, "mouseout", /*mouseout_handler*/ ctx[21], false, false, false, false)
					];

					mounted = true;
				}
			},
			p: function update(ctx, dirty) {
				if (/*title*/ ctx[4].id && /*title*/ ctx[4].title) {
					if (if_block0) {
						if_block0.p(ctx, dirty);
					} else {
						if_block0 = create_if_block_2$1(ctx);
						if_block0.c();
						if_block0.m(svg, if_block0_anchor);
					}
				} else if (if_block0) {
					if_block0.d(1);
					if_block0 = null;
				}

				if (/*desc*/ ctx[6].id && /*desc*/ ctx[6].desc) {
					if (if_block1) {
						if_block1.p(ctx, dirty);
					} else {
						if_block1 = create_if_block_1$1(ctx);
						if_block1.c();
						if_block1.m(svg, path);
					}
				} else if (if_block1) {
					if_block1.d(1);
					if_block1 = null;
				}

				if (dirty & /*strokeWidth*/ 32) {
					attr_dev(path, "stroke-width", /*strokeWidth*/ ctx[5]);
				}

				set_svg_attributes(svg, svg_data = get_spread_update(svg_levels, [
					{ xmlns: "http://www.w3.org/2000/svg" },
					{ fill: "none" },
					dirty & /*color*/ 4 && { color: /*color*/ ctx[2] },
					dirty & /*$$restProps*/ 2048 && /*$$restProps*/ ctx[11],
					dirty & /*size, $$props*/ 4097 && svg_class_value !== (svg_class_value = twMerge('shrink-0', /*sizes*/ ctx[9][/*size*/ ctx[0] ?? 'md'], /*$$props*/ ctx[12].class)) && { class: svg_class_value },
					dirty & /*role*/ 2 && { role: /*role*/ ctx[1] },
					dirty & /*ariaLabel*/ 128 && { "aria-label": /*ariaLabel*/ ctx[7] },
					dirty & /*hasDescription*/ 256 && svg_aria_describedby_value !== (svg_aria_describedby_value = /*hasDescription*/ ctx[8]
					? /*ariaDescribedby*/ ctx[10]
					: undefined) && {
						"aria-describedby": svg_aria_describedby_value
					},
					{ viewBox: "0 0 24 24" }
				]));
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(svg);
				}

				if (if_block0) if_block0.d();
				if (if_block1) if_block1.d();
				mounted = false;
				run_all(dispose);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block$3.name,
			type: "if",
			source: "(29:0) {#if withEvents}",
			ctx
		});

		return block;
	}

	// (76:4) {#if title.id && title.title}
	function create_if_block_4(ctx) {
		let title_1;
		let t_value = /*title*/ ctx[4].title + "";
		let t;
		let title_1_id_value;

		const block = {
			c: function create() {
				title_1 = svg_element("title");
				t = text(t_value);
				attr_dev(title_1, "id", title_1_id_value = /*title*/ ctx[4].id);
				add_location(title_1, file$5, 76, 6, 1900);
			},
			m: function mount(target, anchor) {
				insert_dev(target, title_1, anchor);
				append_dev(title_1, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*title*/ 16 && t_value !== (t_value = /*title*/ ctx[4].title + "")) set_data_dev(t, t_value);

				if (dirty & /*title*/ 16 && title_1_id_value !== (title_1_id_value = /*title*/ ctx[4].id)) {
					attr_dev(title_1, "id", title_1_id_value);
				}
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(title_1);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_4.name,
			type: "if",
			source: "(76:4) {#if title.id && title.title}",
			ctx
		});

		return block;
	}

	// (79:4) {#if desc.id && desc.desc}
	function create_if_block_3$1(ctx) {
		let desc_1;
		let t_value = /*desc*/ ctx[6].desc + "";
		let t;
		let desc_1_id_value;

		const block = {
			c: function create() {
				desc_1 = svg_element("desc");
				t = text(t_value);
				attr_dev(desc_1, "id", desc_1_id_value = /*desc*/ ctx[6].id);
				add_location(desc_1, file$5, 79, 6, 1990);
			},
			m: function mount(target, anchor) {
				insert_dev(target, desc_1, anchor);
				append_dev(desc_1, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*desc*/ 64 && t_value !== (t_value = /*desc*/ ctx[6].desc + "")) set_data_dev(t, t_value);

				if (dirty & /*desc*/ 64 && desc_1_id_value !== (desc_1_id_value = /*desc*/ ctx[6].id)) {
					attr_dev(desc_1, "id", desc_1_id_value);
				}
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(desc_1);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_3$1.name,
			type: "if",
			source: "(79:4) {#if desc.id && desc.desc}",
			ctx
		});

		return block;
	}

	// (50:4) {#if title.id && title.title}
	function create_if_block_2$1(ctx) {
		let title_1;
		let t_value = /*title*/ ctx[4].title + "";
		let t;
		let title_1_id_value;

		const block = {
			c: function create() {
				title_1 = svg_element("title");
				t = text(t_value);
				attr_dev(title_1, "id", title_1_id_value = /*title*/ ctx[4].id);
				add_location(title_1, file$5, 50, 6, 1235);
			},
			m: function mount(target, anchor) {
				insert_dev(target, title_1, anchor);
				append_dev(title_1, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*title*/ 16 && t_value !== (t_value = /*title*/ ctx[4].title + "")) set_data_dev(t, t_value);

				if (dirty & /*title*/ 16 && title_1_id_value !== (title_1_id_value = /*title*/ ctx[4].id)) {
					attr_dev(title_1, "id", title_1_id_value);
				}
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(title_1);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_2$1.name,
			type: "if",
			source: "(50:4) {#if title.id && title.title}",
			ctx
		});

		return block;
	}

	// (53:4) {#if desc.id && desc.desc}
	function create_if_block_1$1(ctx) {
		let desc_1;
		let t_value = /*desc*/ ctx[6].desc + "";
		let t;
		let desc_1_id_value;

		const block = {
			c: function create() {
				desc_1 = svg_element("desc");
				t = text(t_value);
				attr_dev(desc_1, "id", desc_1_id_value = /*desc*/ ctx[6].id);
				add_location(desc_1, file$5, 53, 6, 1325);
			},
			m: function mount(target, anchor) {
				insert_dev(target, desc_1, anchor);
				append_dev(desc_1, t);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*desc*/ 64 && t_value !== (t_value = /*desc*/ ctx[6].desc + "")) set_data_dev(t, t_value);

				if (dirty & /*desc*/ 64 && desc_1_id_value !== (desc_1_id_value = /*desc*/ ctx[6].id)) {
					attr_dev(desc_1, "id", desc_1_id_value);
				}
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(desc_1);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_1$1.name,
			type: "if",
			source: "(53:4) {#if desc.id && desc.desc}",
			ctx
		});

		return block;
	}

	function create_fragment$5(ctx) {
		let if_block_anchor;

		function select_block_type(ctx, dirty) {
			if (/*withEvents*/ ctx[3]) return create_if_block$3;
			return create_else_block$1;
		}

		let current_block_type = select_block_type(ctx);
		let if_block = current_block_type(ctx);

		const block = {
			c: function create() {
				if_block.c();
				if_block_anchor = empty();
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				if_block.m(target, anchor);
				insert_dev(target, if_block_anchor, anchor);
			},
			p: function update(ctx, [dirty]) {
				if (current_block_type === (current_block_type = select_block_type(ctx)) && if_block) {
					if_block.p(ctx, dirty);
				} else {
					if_block.d(1);
					if_block = current_block_type(ctx);

					if (if_block) {
						if_block.c();
						if_block.m(if_block_anchor.parentNode, if_block_anchor);
					}
				}
			},
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(if_block_anchor);
				}

				if_block.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$5.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$5($$self, $$props, $$invalidate) {
		const omit_props_names = ["size","role","color","withEvents","title","strokeWidth","desc","ariaLabel"];
		let $$restProps = compute_rest_props($$props, omit_props_names);
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('ArrowRightOutline', slots, []);
		const ctx = getContext("iconCtx") ?? {};

		const sizes = {
			xs: "w-3 h-3",
			sm: "w-4 h-4",
			md: "w-5 h-5",
			lg: "w-6 h-6",
			xl: "w-8 h-8"
		};

		let { size = ctx.size || "md" } = $$props;
		let { role = ctx.role || "img" } = $$props;
		let { color = ctx.color || "currentColor" } = $$props;
		let { withEvents = ctx.withEvents || false } = $$props;
		let { title = {} } = $$props;
		let { strokeWidth = ctx.strokeWidth || "2" } = $$props;
		let { desc = {} } = $$props;
		let ariaDescribedby = `${title.id || ""} ${desc.id || ""}`;
		let hasDescription = false;
		let { ariaLabel = "arrow right outline" } = $$props;

		function click_handler(event) {
			bubble.call(this, $$self, event);
		}

		function keydown_handler(event) {
			bubble.call(this, $$self, event);
		}

		function keyup_handler(event) {
			bubble.call(this, $$self, event);
		}

		function focus_handler(event) {
			bubble.call(this, $$self, event);
		}

		function blur_handler(event) {
			bubble.call(this, $$self, event);
		}

		function mouseenter_handler(event) {
			bubble.call(this, $$self, event);
		}

		function mouseleave_handler(event) {
			bubble.call(this, $$self, event);
		}

		function mouseover_handler(event) {
			bubble.call(this, $$self, event);
		}

		function mouseout_handler(event) {
			bubble.call(this, $$self, event);
		}

		$$self.$$set = $$new_props => {
			$$invalidate(12, $$props = assign(assign({}, $$props), exclude_internal_props($$new_props)));
			$$invalidate(11, $$restProps = compute_rest_props($$props, omit_props_names));
			if ('size' in $$new_props) $$invalidate(0, size = $$new_props.size);
			if ('role' in $$new_props) $$invalidate(1, role = $$new_props.role);
			if ('color' in $$new_props) $$invalidate(2, color = $$new_props.color);
			if ('withEvents' in $$new_props) $$invalidate(3, withEvents = $$new_props.withEvents);
			if ('title' in $$new_props) $$invalidate(4, title = $$new_props.title);
			if ('strokeWidth' in $$new_props) $$invalidate(5, strokeWidth = $$new_props.strokeWidth);
			if ('desc' in $$new_props) $$invalidate(6, desc = $$new_props.desc);
			if ('ariaLabel' in $$new_props) $$invalidate(7, ariaLabel = $$new_props.ariaLabel);
		};

		$$self.$capture_state = () => ({
			getContext,
			twMerge,
			ctx,
			sizes,
			size,
			role,
			color,
			withEvents,
			title,
			strokeWidth,
			desc,
			ariaDescribedby,
			hasDescription,
			ariaLabel
		});

		$$self.$inject_state = $$new_props => {
			$$invalidate(12, $$props = assign(assign({}, $$props), $$new_props));
			if ('size' in $$props) $$invalidate(0, size = $$new_props.size);
			if ('role' in $$props) $$invalidate(1, role = $$new_props.role);
			if ('color' in $$props) $$invalidate(2, color = $$new_props.color);
			if ('withEvents' in $$props) $$invalidate(3, withEvents = $$new_props.withEvents);
			if ('title' in $$props) $$invalidate(4, title = $$new_props.title);
			if ('strokeWidth' in $$props) $$invalidate(5, strokeWidth = $$new_props.strokeWidth);
			if ('desc' in $$props) $$invalidate(6, desc = $$new_props.desc);
			if ('ariaDescribedby' in $$props) $$invalidate(10, ariaDescribedby = $$new_props.ariaDescribedby);
			if ('hasDescription' in $$props) $$invalidate(8, hasDescription = $$new_props.hasDescription);
			if ('ariaLabel' in $$props) $$invalidate(7, ariaLabel = $$new_props.ariaLabel);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		$$self.$$.update = () => {
			if ($$self.$$.dirty & /*title, desc*/ 80) {
				if (title.id || desc.id) {
					$$invalidate(8, hasDescription = true);
				} else {
					$$invalidate(8, hasDescription = false);
				}
			}
		};

		$$props = exclude_internal_props($$props);

		return [
			size,
			role,
			color,
			withEvents,
			title,
			strokeWidth,
			desc,
			ariaLabel,
			hasDescription,
			sizes,
			ariaDescribedby,
			$$restProps,
			$$props,
			click_handler,
			keydown_handler,
			keyup_handler,
			focus_handler,
			blur_handler,
			mouseenter_handler,
			mouseleave_handler,
			mouseover_handler,
			mouseout_handler
		];
	}

	class ArrowRightOutline extends SvelteComponentDev {
		constructor(options) {
			super(options);

			init(this, options, instance$5, create_fragment$5, safe_not_equal, {
				size: 0,
				role: 1,
				color: 2,
				withEvents: 3,
				title: 4,
				strokeWidth: 5,
				desc: 6,
				ariaLabel: 7
			});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "ArrowRightOutline",
				options,
				id: create_fragment$5.name
			});
		}

		get size() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set size(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get role() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set role(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get color() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set color(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get withEvents() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set withEvents(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get title() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set title(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get strokeWidth() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set strokeWidth(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get desc() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set desc(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		get ariaLabel() {
			throw new Error("<ArrowRightOutline>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set ariaLabel(value) {
			throw new Error("<ArrowRightOutline>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}
	}

	/* src/components/MyTimeline.svelte generated by Svelte v4.2.17 */
	const file$4 = "src/components/MyTimeline.svelte";

	// (9:4) <Button color="alternative">
	function create_default_slot_4(ctx) {
		let t;
		let arrowrightoutline;
		let current;

		arrowrightoutline = new ArrowRightOutline({
				props: { class: "ms-2 w-5 h-5" },
				$$inline: true
			});

		const block = {
			c: function create() {
				t = text("Learn more");
				create_component(arrowrightoutline.$$.fragment);
			},
			m: function mount(target, anchor) {
				insert_dev(target, t, anchor);
				mount_component(arrowrightoutline, target, anchor);
				current = true;
			},
			p: noop,
			i: function intro(local) {
				if (current) return;
				transition_in(arrowrightoutline.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(arrowrightoutline.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(t);
				}

				destroy_component(arrowrightoutline, detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_default_slot_4.name,
			type: "slot",
			source: "(9:4) <Button color=\\\"alternative\\\">",
			ctx
		});

		return block;
	}

	// (7:2) <TimelineItem title="Application UI code in Tailwind CSS" date="February 2022">
	function create_default_slot_3(ctx) {
		let p;
		let t1;
		let button;
		let current;

		button = new Button({
				props: {
					color: "alternative",
					$$slots: { default: [create_default_slot_4] },
					$$scope: { ctx }
				},
				$$inline: true
			});

		const block = {
			c: function create() {
				p = element("p");
				p.textContent = "Get access to over 20+ pages including a dashboard layout, charts, kanban board, calendar, and pre-order E-commerce & Marketing pages.";
				t1 = space();
				create_component(button.$$.fragment);
				attr_dev(p, "class", "mb-4 text-base font-normal text-gray-500 dark:text-gray-400");
				add_location(p, file$4, 7, 4, 246);
			},
			m: function mount(target, anchor) {
				insert_dev(target, p, anchor);
				insert_dev(target, t1, anchor);
				mount_component(button, target, anchor);
				current = true;
			},
			p: function update(ctx, dirty) {
				const button_changes = {};

				if (dirty & /*$$scope*/ 1) {
					button_changes.$$scope = { dirty, ctx };
				}

				button.$set(button_changes);
			},
			i: function intro(local) {
				if (current) return;
				transition_in(button.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(button.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(p);
					detach_dev(t1);
				}

				destroy_component(button, detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_default_slot_3.name,
			type: "slot",
			source: "(7:2) <TimelineItem title=\\\"Application UI code in Tailwind CSS\\\" date=\\\"February 2022\\\">",
			ctx
		});

		return block;
	}

	// (11:2) <TimelineItem title="Application UI code in Tailwind CSS" date="March 2022">
	function create_default_slot_2(ctx) {
		let p;

		const block = {
			c: function create() {
				p = element("p");
				p.textContent = "All of the pages and components are first designed in Figma and we keep a parity between the two versions even as we update the project.";
				attr_dev(p, "class", "text-base font-normal text-gray-500 dark:text-gray-400");
				add_location(p, file$4, 11, 4, 651);
			},
			m: function mount(target, anchor) {
				insert_dev(target, p, anchor);
			},
			p: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(p);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_default_slot_2.name,
			type: "slot",
			source: "(11:2) <TimelineItem title=\\\"Application UI code in Tailwind CSS\\\" date=\\\"March 2022\\\">",
			ctx
		});

		return block;
	}

	// (14:2) <TimelineItem title="Application UI code in Tailwind CSS" date="April 2022">
	function create_default_slot_1(ctx) {
		let p;

		const block = {
			c: function create() {
				p = element("p");
				p.textContent = "Get started with dozens of web components and interactive elements built on top of Tailwind CSS.";
				attr_dev(p, "class", "text-base font-normal text-gray-500 dark:text-gray-400");
				add_location(p, file$4, 14, 4, 959);
			},
			m: function mount(target, anchor) {
				insert_dev(target, p, anchor);
			},
			p: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(p);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_default_slot_1.name,
			type: "slot",
			source: "(14:2) <TimelineItem title=\\\"Application UI code in Tailwind CSS\\\" date=\\\"April 2022\\\">",
			ctx
		});

		return block;
	}

	// (6:0) <Timeline>
	function create_default_slot(ctx) {
		let timelineitem0;
		let t0;
		let timelineitem1;
		let t1;
		let timelineitem2;
		let current;

		timelineitem0 = new TimelineItem({
				props: {
					title: "Application UI code in Tailwind CSS",
					date: "February 2022",
					$$slots: { default: [create_default_slot_3] },
					$$scope: { ctx }
				},
				$$inline: true
			});

		timelineitem1 = new TimelineItem({
				props: {
					title: "Application UI code in Tailwind CSS",
					date: "March 2022",
					$$slots: { default: [create_default_slot_2] },
					$$scope: { ctx }
				},
				$$inline: true
			});

		timelineitem2 = new TimelineItem({
				props: {
					title: "Application UI code in Tailwind CSS",
					date: "April 2022",
					$$slots: { default: [create_default_slot_1] },
					$$scope: { ctx }
				},
				$$inline: true
			});

		const block = {
			c: function create() {
				create_component(timelineitem0.$$.fragment);
				t0 = space();
				create_component(timelineitem1.$$.fragment);
				t1 = space();
				create_component(timelineitem2.$$.fragment);
			},
			m: function mount(target, anchor) {
				mount_component(timelineitem0, target, anchor);
				insert_dev(target, t0, anchor);
				mount_component(timelineitem1, target, anchor);
				insert_dev(target, t1, anchor);
				mount_component(timelineitem2, target, anchor);
				current = true;
			},
			p: function update(ctx, dirty) {
				const timelineitem0_changes = {};

				if (dirty & /*$$scope*/ 1) {
					timelineitem0_changes.$$scope = { dirty, ctx };
				}

				timelineitem0.$set(timelineitem0_changes);
				const timelineitem1_changes = {};

				if (dirty & /*$$scope*/ 1) {
					timelineitem1_changes.$$scope = { dirty, ctx };
				}

				timelineitem1.$set(timelineitem1_changes);
				const timelineitem2_changes = {};

				if (dirty & /*$$scope*/ 1) {
					timelineitem2_changes.$$scope = { dirty, ctx };
				}

				timelineitem2.$set(timelineitem2_changes);
			},
			i: function intro(local) {
				if (current) return;
				transition_in(timelineitem0.$$.fragment, local);
				transition_in(timelineitem1.$$.fragment, local);
				transition_in(timelineitem2.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(timelineitem0.$$.fragment, local);
				transition_out(timelineitem1.$$.fragment, local);
				transition_out(timelineitem2.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(t0);
					detach_dev(t1);
				}

				destroy_component(timelineitem0, detaching);
				destroy_component(timelineitem1, detaching);
				destroy_component(timelineitem2, detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_default_slot.name,
			type: "slot",
			source: "(6:0) <Timeline>",
			ctx
		});

		return block;
	}

	function create_fragment$4(ctx) {
		let timeline;
		let current;

		timeline = new Timeline({
				props: {
					$$slots: { default: [create_default_slot] },
					$$scope: { ctx }
				},
				$$inline: true
			});

		const block = {
			c: function create() {
				create_component(timeline.$$.fragment);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				mount_component(timeline, target, anchor);
				current = true;
			},
			p: function update(ctx, [dirty]) {
				const timeline_changes = {};

				if (dirty & /*$$scope*/ 1) {
					timeline_changes.$$scope = { dirty, ctx };
				}

				timeline.$set(timeline_changes);
			},
			i: function intro(local) {
				if (current) return;
				transition_in(timeline.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(timeline.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				destroy_component(timeline, detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$4.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$4($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('MyTimeline', slots, []);
		const writable_props = [];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<MyTimeline> was created with unknown prop '${key}'`);
		});

		$$self.$capture_state = () => ({
			Timeline,
			TimelineItem,
			Button,
			ArrowRightOutline
		});

		return [];
	}

	class MyTimeline extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$4, create_fragment$4, safe_not_equal, {});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "MyTimeline",
				options,
				id: create_fragment$4.name
			});
		}
	}

	/* src/components/Countdown.svelte generated by Svelte v4.2.17 */

	const { console: console_1 } = globals;
	const file$3 = "src/components/Countdown.svelte";

	// (77:0) {:else}
	function create_else_block(ctx) {
		let div5;
		let div0;
		let span0;
		let t0;
		let t1;
		let span1;
		let t3;
		let div1;
		let span2;
		let t4;
		let t5;
		let span3;
		let t7;
		let div2;
		let span4;
		let t8;
		let t9;
		let span5;
		let t11;
		let div3;
		let span6;
		let t12;
		let t13;
		let span7;
		let t15;
		let div4;
		let span8;
		let t16;
		let t17;
		let span9;
		let div5_intro;
		let div5_outro;
		let current;

		const block = {
			c: function create() {
				div5 = element("div");
				div0 = element("div");
				span0 = element("span");
				t0 = text(/*currentYears*/ ctx[1]);
				t1 = space();
				span1 = element("span");
				span1.textContent = "years";
				t3 = space();
				div1 = element("div");
				span2 = element("span");
				t4 = text(/*currentDays*/ ctx[2]);
				t5 = space();
				span3 = element("span");
				span3.textContent = "days";
				t7 = space();
				div2 = element("div");
				span4 = element("span");
				t8 = text(/*currentHours*/ ctx[3]);
				t9 = space();
				span5 = element("span");
				span5.textContent = "hours";
				t11 = space();
				div3 = element("div");
				span6 = element("span");
				t12 = text(/*currentMinutes*/ ctx[4]);
				t13 = space();
				span7 = element("span");
				span7.textContent = "min";
				t15 = space();
				div4 = element("div");
				span8 = element("span");
				t16 = text(/*currentSeconds*/ ctx[5]);
				t17 = space();
				span9 = element("span");
				span9.textContent = "sec";
				attr_dev(span0, "class", "countdown-value svelte-14d8aj5");
				add_location(span0, file$3, 79, 6, 2022);
				attr_dev(span1, "class", "countdown-label svelte-14d8aj5");
				add_location(span1, file$3, 80, 6, 2080);
				attr_dev(div0, "class", "countdown-item svelte-14d8aj5");
				add_location(div0, file$3, 78, 4, 1987);
				attr_dev(span2, "class", "countdown-value svelte-14d8aj5");
				add_location(span2, file$3, 83, 6, 2173);
				attr_dev(span3, "class", "countdown-label svelte-14d8aj5");
				add_location(span3, file$3, 84, 6, 2230);
				attr_dev(div1, "class", "countdown-item svelte-14d8aj5");
				add_location(div1, file$3, 82, 4, 2138);
				attr_dev(span4, "class", "countdown-value svelte-14d8aj5");
				add_location(span4, file$3, 87, 6, 2322);
				attr_dev(span5, "class", "countdown-label svelte-14d8aj5");
				add_location(span5, file$3, 88, 6, 2380);
				attr_dev(div2, "class", "countdown-item svelte-14d8aj5");
				add_location(div2, file$3, 86, 4, 2287);
				attr_dev(span6, "class", "countdown-value svelte-14d8aj5");
				add_location(span6, file$3, 91, 6, 2473);
				attr_dev(span7, "class", "countdown-label svelte-14d8aj5");
				add_location(span7, file$3, 92, 6, 2533);
				attr_dev(div3, "class", "countdown-item svelte-14d8aj5");
				add_location(div3, file$3, 90, 4, 2438);
				attr_dev(span8, "class", "countdown-value svelte-14d8aj5");
				add_location(span8, file$3, 95, 6, 2624);
				attr_dev(span9, "class", "countdown-label svelte-14d8aj5");
				add_location(span9, file$3, 96, 6, 2684);
				attr_dev(div4, "class", "countdown-item svelte-14d8aj5");
				add_location(div4, file$3, 94, 4, 2589);
				attr_dev(div5, "class", "countdown-container svelte-14d8aj5");
				add_location(div5, file$3, 77, 2, 1892);
			},
			m: function mount(target, anchor) {
				insert_dev(target, div5, anchor);
				append_dev(div5, div0);
				append_dev(div0, span0);
				append_dev(span0, t0);
				append_dev(div0, t1);
				append_dev(div0, span1);
				append_dev(div5, t3);
				append_dev(div5, div1);
				append_dev(div1, span2);
				append_dev(span2, t4);
				append_dev(div1, t5);
				append_dev(div1, span3);
				append_dev(div5, t7);
				append_dev(div5, div2);
				append_dev(div2, span4);
				append_dev(span4, t8);
				append_dev(div2, t9);
				append_dev(div2, span5);
				append_dev(div5, t11);
				append_dev(div5, div3);
				append_dev(div3, span6);
				append_dev(span6, t12);
				append_dev(div3, t13);
				append_dev(div3, span7);
				append_dev(div5, t15);
				append_dev(div5, div4);
				append_dev(div4, span8);
				append_dev(span8, t16);
				append_dev(div4, t17);
				append_dev(div4, span9);
				current = true;
			},
			p: function update(ctx, dirty) {
				if (!current || dirty & /*currentYears*/ 2) set_data_dev(t0, /*currentYears*/ ctx[1]);
				if (!current || dirty & /*currentDays*/ 4) set_data_dev(t4, /*currentDays*/ ctx[2]);
				if (!current || dirty & /*currentHours*/ 8) set_data_dev(t8, /*currentHours*/ ctx[3]);
				if (!current || dirty & /*currentMinutes*/ 16) set_data_dev(t12, /*currentMinutes*/ ctx[4]);
				if (!current || dirty & /*currentSeconds*/ 32) set_data_dev(t16, /*currentSeconds*/ ctx[5]);
			},
			i: function intro(local) {
				if (current) return;

				if (local) {
					add_render_callback(() => {
						if (!current) return;
						if (div5_outro) div5_outro.end(1);
						div5_intro = create_in_transition(div5, fade, { duration: 500 });
						div5_intro.start();
					});
				}

				current = true;
			},
			o: function outro(local) {
				if (div5_intro) div5_intro.invalidate();

				if (local) {
					div5_outro = create_out_transition(div5, fade, { duration: 300 });
				}

				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div5);
				}

				if (detaching && div5_outro) div5_outro.end();
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_else_block.name,
			type: "else",
			source: "(77:0) {:else}",
			ctx
		});

		return block;
	}

	// (73:0) {#if isLoading}
	function create_if_block$2(ctx) {
		let div;
		let span;
		let t1;

		const block = {
			c: function create() {
				div = element("div");
				span = element("span");
				span.textContent = "●";
				t1 = text(" Loading...");
				attr_dev(span, "class", "loading-icon svelte-14d8aj5");
				add_location(span, file$3, 74, 4, 1820);
				attr_dev(div, "class", "loading-container svelte-14d8aj5");
				add_location(div, file$3, 73, 2, 1784);
			},
			m: function mount(target, anchor) {
				insert_dev(target, div, anchor);
				append_dev(div, span);
				append_dev(div, t1);
			},
			p: noop,
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block$2.name,
			type: "if",
			source: "(73:0) {#if isLoading}",
			ctx
		});

		return block;
	}

	function create_fragment$3(ctx) {
		let current_block_type_index;
		let if_block;
		let if_block_anchor;
		const if_block_creators = [create_if_block$2, create_else_block];
		const if_blocks = [];

		function select_block_type(ctx, dirty) {
			if (/*isLoading*/ ctx[0]) return 0;
			return 1;
		}

		current_block_type_index = select_block_type(ctx);
		if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);

		const block = {
			c: function create() {
				if_block.c();
				if_block_anchor = empty();
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				if_blocks[current_block_type_index].m(target, anchor);
				insert_dev(target, if_block_anchor, anchor);
			},
			p: function update(ctx, [dirty]) {
				let previous_block_index = current_block_type_index;
				current_block_type_index = select_block_type(ctx);

				if (current_block_type_index === previous_block_index) {
					if_blocks[current_block_type_index].p(ctx, dirty);
				} else {
					group_outros();

					transition_out(if_blocks[previous_block_index], 1, 1, () => {
						if_blocks[previous_block_index] = null;
					});

					check_outros();
					if_block = if_blocks[current_block_type_index];

					if (!if_block) {
						if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
						if_block.c();
					} else {
						if_block.p(ctx, dirty);
					}

					transition_in(if_block, 1);
					if_block.m(if_block_anchor.parentNode, if_block_anchor);
				}
			},
			i: function intro(local) {
				transition_in(if_block);
			},
			o: function outro(local) {
				transition_out(if_block);
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(if_block_anchor);
				}

				if_blocks[current_block_type_index].d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$3.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$3($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('Countdown', slots, []);
		let { targetDate } = $$props;
		let isLoading = true;
		let currentYears = 0;
		let currentDays = 0;
		let currentHours = 0;
		let currentMinutes = 0;
		let currentSeconds = 0;
		let years = 0;
		let days = 0;
		let hours = 0;
		let minutes = 0;
		let seconds = 0;
		let countdownInterval;

		function startCountdown() {
			countdownInterval = setInterval(
				() => {
					updateCountdown();
					$$invalidate(0, isLoading = false); // Set isLoading to false after the first update
				},
				1000
			);
		}

		function updateCountdown() {
			if (!targetDate || isNaN(targetDate)) {
				clearInterval(countdownInterval);
				years = 0;
				days = 0;
				hours = 0;
				minutes = 0;
				seconds = 0;
				console.error('Invalid targetDate provided to Countdown component');
				return;
			}

			const currentTime = new Date().getTime();
			const difference = targetDate - currentTime;

			if (difference <= 0) {
				clearInterval(countdownInterval);
				years = 0;
				days = 0;
				hours = 0;
				minutes = 0;
				seconds = 0;
				return;
			}

			const totalDays = Math.floor(difference / (1000 * 60 * 60 * 24));
			years = Math.floor(totalDays / 365);
			days = totalDays % 365;
			hours = Math.floor(difference % (1000 * 60 * 60 * 24) / (1000 * 60 * 60));
			minutes = Math.floor(difference % (1000 * 60 * 60) / (1000 * 60));
			seconds = Math.floor(difference % (1000 * 60) / 1000);

			// Update the current values
			$$invalidate(1, currentYears = years);

			$$invalidate(2, currentDays = days);
			$$invalidate(3, currentHours = hours);
			$$invalidate(4, currentMinutes = minutes);
			$$invalidate(5, currentSeconds = seconds);
		}

		onDestroy(() => {
			clearInterval(countdownInterval);
		});

		startCountdown();

		$$self.$$.on_mount.push(function () {
			if (targetDate === undefined && !('targetDate' in $$props || $$self.$$.bound[$$self.$$.props['targetDate']])) {
				console_1.warn("<Countdown> was created without expected prop 'targetDate'");
			}
		});

		const writable_props = ['targetDate'];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1.warn(`<Countdown> was created with unknown prop '${key}'`);
		});

		$$self.$$set = $$props => {
			if ('targetDate' in $$props) $$invalidate(6, targetDate = $$props.targetDate);
		};

		$$self.$capture_state = () => ({
			onDestroy,
			fade,
			targetDate,
			isLoading,
			currentYears,
			currentDays,
			currentHours,
			currentMinutes,
			currentSeconds,
			years,
			days,
			hours,
			minutes,
			seconds,
			countdownInterval,
			startCountdown,
			updateCountdown
		});

		$$self.$inject_state = $$props => {
			if ('targetDate' in $$props) $$invalidate(6, targetDate = $$props.targetDate);
			if ('isLoading' in $$props) $$invalidate(0, isLoading = $$props.isLoading);
			if ('currentYears' in $$props) $$invalidate(1, currentYears = $$props.currentYears);
			if ('currentDays' in $$props) $$invalidate(2, currentDays = $$props.currentDays);
			if ('currentHours' in $$props) $$invalidate(3, currentHours = $$props.currentHours);
			if ('currentMinutes' in $$props) $$invalidate(4, currentMinutes = $$props.currentMinutes);
			if ('currentSeconds' in $$props) $$invalidate(5, currentSeconds = $$props.currentSeconds);
			if ('years' in $$props) years = $$props.years;
			if ('days' in $$props) days = $$props.days;
			if ('hours' in $$props) hours = $$props.hours;
			if ('minutes' in $$props) minutes = $$props.minutes;
			if ('seconds' in $$props) seconds = $$props.seconds;
			if ('countdownInterval' in $$props) countdownInterval = $$props.countdownInterval;
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		return [
			isLoading,
			currentYears,
			currentDays,
			currentHours,
			currentMinutes,
			currentSeconds,
			targetDate
		];
	}

	class Countdown extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$3, create_fragment$3, safe_not_equal, { targetDate: 6 });

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "Countdown",
				options,
				id: create_fragment$3.name
			});
		}

		get targetDate() {
			throw new Error("<Countdown>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set targetDate(value) {
			throw new Error("<Countdown>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}
	}

	let customAlphabet = (alphabet, defaultSize = 21) => {
	  return (size = defaultSize) => {
	    let id = '';
	    let i = size;
	    while (i--) {
	      id += alphabet[(Math.random() * alphabet.length) | 0];
	    }
	    return id
	  }
	};

	// ../../node_modules/.pnpm/swrev@4.0.0/node_modules/swrev/dist/swrev.mjs
	var P = Object.defineProperty;
	var F = (r, e, t) => e in r ? P(r, e, { enumerable: true, configurable: true, writable: true, value: t }) : r[e] = t;
	var h = (r, e, t) => (F(r, typeof e != "symbol" ? e + "" : e, t), t);
	var I = class {
	  constructor() {
	    h(this, "listeners", /* @__PURE__ */ new Map());
	  }
	  /**
	   * Subscribes a given listener.
	   */
	  subscribe(e, t) {
	    this.listeners.has(e) || this.listeners.set(e, []), !this.listeners.get(e).includes(t) && this.listeners.get(e).push(t);
	  }
	  /**
	   * Unsubscribes the given listener.
	   */
	  unsubscribe(e, t) {
	    this.listeners.has(e) && this.listeners.get(e).includes(t) && (this.listeners.get(e).splice(this.listeners.get(e).indexOf(t), 1), this.listeners.get(e).length === 0 && this.listeners.delete(e));
	  }
	  /**
	   * Emits an event to all active listeners.
	   */
	  emit(e, t) {
	    this.listeners.has(e) && this.listeners.get(e).forEach((s) => s(t));
	  }
	};
	var L = {
	  broadcast: false
	};
	var S = {
	  broadcast: false
	};
	var O = class {
	  /**
	   * Creates the cache item given the data and expiration at.
	   */
	  constructor({ data: e, expiresAt: t = null }) {
	    h(this, "data");
	    h(this, "expiresAt");
	    this.data = e, this.expiresAt = t;
	  }
	  /**
	   * Determines if the current cache item is still being resolved.
	   * This returns true if data is a promise, or false if type `D`.
	   */
	  isResolving() {
	    return this.data instanceof Promise;
	  }
	  /**
	   * Determines if the given cache item has expired.
	   */
	  hasExpired() {
	    return this.expiresAt === null || this.expiresAt < /* @__PURE__ */ new Date();
	  }
	  /**
	   * Set the expiration time of the given cache item relative to now.
	   */
	  expiresIn(e) {
	    return this.expiresAt = /* @__PURE__ */ new Date(), this.expiresAt.setMilliseconds(this.expiresAt.getMilliseconds() + e), this;
	  }
	};
	var q = class {
	  constructor() {
	    h(this, "elements", /* @__PURE__ */ new Map());
	    h(this, "event", new I());
	  }
	  /**
	   * Resolves the promise and replaces the Promise to the resolved data.
	   * It also broadcasts the value change if needed or deletes the key if
	   * the value resolves to undefined or null.
	   */
	  resolve(e, t) {
	    Promise.resolve(t.data).then((s) => {
	      if (s == null)
	        return this.remove(e);
	      t.data = s, this.broadcast(e, s);
	    });
	  }
	  /**
	   * Gets an element from the cache.
	   *
	   * It is assumed the item always exist when
	   * you get it. Use the has method to check
	   * for the existence of it.
	   */
	  get(e) {
	    return this.elements.get(e);
	  }
	  /**
	   * Sets an element to the cache.
	   */
	  set(e, t) {
	    this.elements.set(e, t), this.resolve(e, t);
	  }
	  /**
	   * Removes an key-value pair from the cache.
	   */
	  remove(e, t) {
	    const { broadcast: s } = { ...L, ...t };
	    s && this.broadcast(e, void 0), this.elements.delete(e);
	  }
	  /**
	   * Removes all the key-value pairs from the cache.
	   */
	  clear(e) {
	    const { broadcast: t } = { ...S, ...e };
	    if (t)
	      for (const s of this.elements.keys())
	        this.broadcast(s, void 0);
	    this.elements.clear();
	  }
	  /**
	   * Determines if the given key exists
	   * in the cache.
	   */
	  has(e) {
	    return this.elements.has(e);
	  }
	  /**
	   * Subscribes the callback to the given key.
	   */
	  subscribe(e, t) {
	    this.event.subscribe(e, t);
	  }
	  /**
	   * Unsubscribes to the given key events.
	   */
	  unsubscribe(e, t) {
	    this.event.unsubscribe(e, t);
	  }
	  /**
	   * Broadcasts a value change  on all subscribed instances.
	   */
	  broadcast(e, t) {
	    this.event.emit(e, t);
	  }
	};
	var x = {
	  cache: new q(),
	  errors: new I(),
	  fetcher: async (r) => {
	    const e = await fetch(r);
	    if (!e.ok)
	      throw Error("Not a 2XX response.");
	    return e.json();
	  },
	  fallbackData: void 0,
	  loadInitialCache: true,
	  revalidateOnStart: true,
	  dedupingInterval: 2e3,
	  revalidateOnFocus: true,
	  focusThrottleInterval: 5e3,
	  revalidateOnReconnect: true,
	  reconnectWhen: (r, { enabled: e }) => e && typeof window < "u" ? (window.addEventListener("online", r), () => window.removeEventListener("online", r)) : () => {
	  },
	  focusWhen: (r, { enabled: e, throttleInterval: t }) => {
	    if (e && typeof window < "u") {
	      let s = null;
	      const i = () => {
	        const a = Date.now();
	        (s === null || a - s > t) && (s = a, r());
	      };
	      return window.addEventListener("focus", i), () => window.removeEventListener("focus", i);
	    }
	    return () => {
	    };
	  },
	  revalidateFunction: void 0
	};
	var E = {
	  ...x,
	  force: false
	};
	var T = {
	  revalidate: true,
	  revalidateOptions: { ...E },
	  revalidateFunction: void 0
	};
	var X = {
	  broadcast: false
	};
	var H = class {
	  /**
	   * Creates a new instance of SWR.
	   */
	  constructor(e) {
	    h(this, "options");
	    this.options = { ...x, ...e };
	  }
	  /**
	   * Gets the cache of the SWR.
	   */
	  get cache() {
	    return this.options.cache;
	  }
	  /**
	   * Gets the cache of the SWR.
	   */
	  get errors() {
	    return this.options.errors;
	  }
	  /**
	   * Requests the data using the provided fetcher.
	   */
	  async requestData(e, t) {
	    return await Promise.resolve(t(e)).catch((s) => {
	      throw this.errors.emit(e, s), s;
	    });
	  }
	  /**
	   * Resolves the given to a SWRKey or undefined.
	   */
	  resolveKey(e) {
	    if (typeof e == "function")
	      try {
	        return e();
	      } catch (e2) {
	        return;
	      }
	    return e;
	  }
	  /**
	   * Clear the specified keys from the cache. If no keys
	   * are specified, it clears all the cache keys.
	   */
	  clear(e, t) {
	    const s = { ...X, ...t };
	    if (e == null)
	      return this.cache.clear(s);
	    if (!Array.isArray(e))
	      return this.cache.remove(e, s);
	    for (const i of e)
	      this.cache.remove(i, s);
	  }
	  /**
	   * Revalidates the key and mutates the cache if needed.
	   */
	  async revalidate(e, t) {
	    if (!e)
	      throw new Error("[Revalidate] Key issue: ${key}");
	    const { fetcher: s, dedupingInterval: i } = this.options, { force: a, fetcher: o, dedupingInterval: n } = {
	      ...E,
	      fetcher: s,
	      dedupingInterval: i,
	      ...t
	    };
	    if (a || !this.cache.has(e) || this.cache.has(e) && this.cache.get(e).hasExpired()) {
	      const c2 = this.requestData(e, o), l = c2.catch(() => {
	      });
	      return this.cache.set(e, new O({ data: l }).expiresIn(n)), await c2;
	    }
	    return this.getWait(e);
	  }
	  /**
	   * Mutates the data of a given key with a new value.
	   * This is used to replace the cache contents of the
	   * given key manually.
	   */
	  async mutate(e, t, s) {
	    var _a;
	    if (!e)
	      throw new Error("[Mutate] Key issue: ${key}");
	    const {
	      revalidate: i,
	      revalidateOptions: a,
	      revalidateFunction: o
	    } = {
	      ...T,
	      ...s
	    };
	    let n;
	    if (typeof t == "function") {
	      let c2;
	      if (this.cache.has(e)) {
	        const l = this.cache.get(e);
	        l.isResolving() || (c2 = l.data);
	      }
	      n = t(c2);
	    } else
	      n = t;
	    return this.cache.set(e, new O({ data: n })), i ? await ((_a = o == null ? void 0 : o(e, a)) != null ? _a : this.revalidate(e, a)) : n;
	  }
	  /**
	   * Gets the data of the given key. Keep in mind
	   * this data will be stale and revalidate in the background
	   * unless specified otherwise.
	   */
	  subscribeData(e, t) {
	    if (e) {
	      const s = (i) => t(i);
	      return this.cache.subscribe(e, s), () => this.cache.unsubscribe(e, s);
	    }
	    return () => {
	    };
	  }
	  /**
	   * Subscribes to errors on the given key.
	   */
	  subscribeErrors(e, t) {
	    if (e) {
	      const s = (i) => t(i);
	      return this.errors.subscribe(e, s), () => this.errors.unsubscribe(e, s);
	    }
	    return () => {
	    };
	  }
	  /**
	   * Gets the current cached data of the given key.
	   * This does not trigger any revalidation nor mutation
	   * of the data.
	   * - If the data has never been validated
	   * (there is no cache) it will return undefined.
	   * - If the item is pending to resolve (there is a request
	   * pending to resolve) it will return undefined.
	   */
	  get(e) {
	    if (e && this.cache.has(e)) {
	      const t = this.cache.get(e);
	      if (!t.isResolving())
	        return t.data;
	    }
	  }
	  /**
	   * Gets an element from the cache. The difference
	   * with the get is that this method returns a promise
	   * that will resolve the the value. If there's no item
	   * in the cache, it will wait for it before resolving.
	   */
	  getWait(e) {
	    return new Promise((t, s) => {
	      const i = this.subscribeData(e, (n) => {
	        if (i(), n !== void 0)
	          return t(n);
	      }), a = this.subscribeErrors(e, (n) => {
	        if (a(), n !== void 0)
	          return s(n);
	      }), o = this.get(e);
	      if (o !== void 0)
	        return t(o);
	    });
	  }
	  /**
	   * Use a SWR value given the key and
	   * subscribe to future changes.
	   */
	  subscribe(e, t, s, i) {
	    const {
	      fetcher: a,
	      fallbackData: o,
	      loadInitialCache: n,
	      revalidateOnStart: c2,
	      dedupingInterval: l,
	      revalidateOnFocus: A2,
	      focusThrottleInterval: C,
	      revalidateOnReconnect: R,
	      reconnectWhen: W2,
	      focusWhen: D2,
	      revalidateFunction: d
	    } = {
	      // Current instance options
	      // (includes default options)
	      ...this.options,
	      // Current call options.
	      ...i
	    }, K2 = (m) => {
	      var _a;
	      return (_a = d == null ? void 0 : d(this.resolveKey(e), m)) != null ? _a : this.revalidate(this.resolveKey(e), m);
	    }, f = () => K2({ fetcher: a, dedupingInterval: l }), u = n ? this.get(this.resolveKey(e)) : o != null ? o : void 0, g = c2 ? f() : Promise.resolve(void 0), M = u ? Promise.resolve(u) : g;
	    u && (t == null || t(u));
	    const v2 = t ? this.subscribeData(this.resolveKey(e), t) : void 0, b = s ? this.subscribeErrors(this.resolveKey(e), s) : void 0, p2 = D2(f, {
	      throttleInterval: C,
	      enabled: A2
	    }), w2 = W2(f, {
	      enabled: R
	    });
	    return { unsubscribe: () => {
	      v2 == null || v2(), b == null || b(), p2 == null || p2(), w2 == null || w2();
	    }, dataPromise: M, revalidatePromise: g };
	  }
	};
	function p() {
	}
	function D(t) {
	  return t();
	}
	function q2(t) {
	  t.forEach(D);
	}
	function x2(t) {
	  return typeof t == "function";
	}
	function K(t, e) {
	  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
	}
	function z(t, ...e) {
	  if (t == null) {
	    for (const r of e)
	      r(void 0);
	    return p;
	  }
	  const n = t.subscribe(...e);
	  return n.unsubscribe ? () => n.unsubscribe() : n;
	}
	var v = [];
	function A(t, e) {
	  return {
	    subscribe: y(t, e).subscribe
	  };
	}
	function y(t, e = p) {
	  let n;
	  const r = /* @__PURE__ */ new Set();
	  function i(u) {
	    if (K(t, u) && (t = u, n)) {
	      const f = !v.length;
	      for (const s of r)
	        s[1](), v.push(s, t);
	      if (f) {
	        for (let s = 0; s < v.length; s += 2)
	          v[s][0](v[s + 1]);
	        v.length = 0;
	      }
	    }
	  }
	  function a(u) {
	    i(u(t));
	  }
	  function d(u, f = p) {
	    const s = [u, f];
	    return r.add(s), r.size === 1 && (n = e(i, a) || p), u(t), () => {
	      r.delete(s), r.size === 0 && n && (n(), n = null);
	    };
	  }
	  return { set: i, update: a, subscribe: d };
	}
	function S2(t, e, n) {
	  const r = !Array.isArray(t), i = r ? [t] : t;
	  if (!i.every(Boolean))
	    throw new Error("derived() expects stores as input, got a falsy value");
	  const a = e.length < 2;
	  return A(n, (d, u) => {
	    let f = false;
	    const s = [];
	    let h2 = 0, o = p;
	    const l = () => {
	      if (h2)
	        return;
	      o();
	      const b = e(r ? s[0] : s, d, u);
	      a ? d(b) : o = x2(b) ? b : p;
	    }, g = i.map(
	      (b, m) => z(
	        b,
	        (R) => {
	          s[m] = R, h2 &= ~(1 << m), f && l();
	        },
	        () => {
	          h2 |= 1 << m;
	        }
	      )
	    );
	    return f = true, l(), function() {
	      q2(g), o(), f = false;
	    };
	  });
	}
	var O2 = class extends H {
	  /**
	   * Svelte specific use of SWR.
	   */
	  useSWR(e, n) {
	    let r;
	    const i = y(void 0, () => () => r == null ? void 0 : r()), a = y(void 0, () => () => r == null ? void 0 : r());
	    beforeUpdate(() => {
	      const o = (g) => {
	        a.set(void 0), i.set(g);
	      }, l = (g) => a.set(g);
	      r || (r = this.subscribe(e, o, l, {
	        loadInitialCache: true,
	        ...n
	      }).unsubscribe);
	    }), onDestroy(() => r == null ? void 0 : r());
	    const d = (o, l) => this.mutate(this.resolveKey(e), o, {
	      revalidateOptions: n,
	      ...l
	    }), u = (o) => this.revalidate(this.resolveKey(e), { ...n, ...o }), f = (o) => this.clear(this.resolveKey(e), o), s = S2([i, a], ([o, l]) => o === void 0 && l === void 0), h2 = S2([i, a], ([o, l]) => o !== void 0 && l === void 0);
	    return { data: i, error: a, mutate: d, revalidate: u, clear: f, isLoading: s, isValid: h2 };
	  }
	};
	var W = (t) => new O2(t);
	var c = W();
	var F2 = (t, e) => c.useSWR(t, e);
	var generateId = customAlphabet(
	  "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
	  7
	);

	// shared/stream-parts.ts
	var textStreamPart = {
	  code: "0",
	  name: "text",
	  parse: (value) => {
	    if (typeof value !== "string") {
	      throw new Error('"text" parts expect a string value.');
	    }
	    return { type: "text", value };
	  }
	};
	var functionCallStreamPart = {
	  code: "1",
	  name: "function_call",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("function_call" in value) || typeof value.function_call !== "object" || value.function_call == null || !("name" in value.function_call) || !("arguments" in value.function_call) || typeof value.function_call.name !== "string" || typeof value.function_call.arguments !== "string") {
	      throw new Error(
	        '"function_call" parts expect an object with a "function_call" property.'
	      );
	    }
	    return {
	      type: "function_call",
	      value
	    };
	  }
	};
	var dataStreamPart = {
	  code: "2",
	  name: "data",
	  parse: (value) => {
	    if (!Array.isArray(value)) {
	      throw new Error('"data" parts expect an array value.');
	    }
	    return { type: "data", value };
	  }
	};
	var errorStreamPart = {
	  code: "3",
	  name: "error",
	  parse: (value) => {
	    if (typeof value !== "string") {
	      throw new Error('"error" parts expect a string value.');
	    }
	    return { type: "error", value };
	  }
	};
	var assistantMessageStreamPart = {
	  code: "4",
	  name: "assistant_message",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("id" in value) || !("role" in value) || !("content" in value) || typeof value.id !== "string" || typeof value.role !== "string" || value.role !== "assistant" || !Array.isArray(value.content) || !value.content.every(
	      (item) => item != null && typeof item === "object" && "type" in item && item.type === "text" && "text" in item && item.text != null && typeof item.text === "object" && "value" in item.text && typeof item.text.value === "string"
	    )) {
	      throw new Error(
	        '"assistant_message" parts expect an object with an "id", "role", and "content" property.'
	      );
	    }
	    return {
	      type: "assistant_message",
	      value
	    };
	  }
	};
	var assistantControlDataStreamPart = {
	  code: "5",
	  name: "assistant_control_data",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("threadId" in value) || !("messageId" in value) || typeof value.threadId !== "string" || typeof value.messageId !== "string") {
	      throw new Error(
	        '"assistant_control_data" parts expect an object with a "threadId" and "messageId" property.'
	      );
	    }
	    return {
	      type: "assistant_control_data",
	      value: {
	        threadId: value.threadId,
	        messageId: value.messageId
	      }
	    };
	  }
	};
	var dataMessageStreamPart = {
	  code: "6",
	  name: "data_message",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("role" in value) || !("data" in value) || typeof value.role !== "string" || value.role !== "data") {
	      throw new Error(
	        '"data_message" parts expect an object with a "role" and "data" property.'
	      );
	    }
	    return {
	      type: "data_message",
	      value
	    };
	  }
	};
	var toolCallsStreamPart = {
	  code: "7",
	  name: "tool_calls",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("tool_calls" in value) || typeof value.tool_calls !== "object" || value.tool_calls == null || !Array.isArray(value.tool_calls) || value.tool_calls.some(
	      (tc) => tc == null || typeof tc !== "object" || !("id" in tc) || typeof tc.id !== "string" || !("type" in tc) || typeof tc.type !== "string" || !("function" in tc) || tc.function == null || typeof tc.function !== "object" || !("arguments" in tc.function) || typeof tc.function.name !== "string" || typeof tc.function.arguments !== "string"
	    )) {
	      throw new Error(
	        '"tool_calls" parts expect an object with a ToolCallPayload.'
	      );
	    }
	    return {
	      type: "tool_calls",
	      value
	    };
	  }
	};
	var messageAnnotationsStreamPart = {
	  code: "8",
	  name: "message_annotations",
	  parse: (value) => {
	    if (!Array.isArray(value)) {
	      throw new Error('"message_annotations" parts expect an array value.');
	    }
	    return { type: "message_annotations", value };
	  }
	};
	var toolCallStreamPart = {
	  code: "9",
	  name: "tool_call",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("toolCallId" in value) || typeof value.toolCallId !== "string" || !("toolName" in value) || typeof value.toolName !== "string" || !("args" in value) || typeof value.args !== "object") {
	      throw new Error(
	        '"tool_call" parts expect an object with a "toolCallId", "toolName", and "args" property.'
	      );
	    }
	    return {
	      type: "tool_call",
	      value
	    };
	  }
	};
	var toolResultStreamPart = {
	  code: "a",
	  name: "tool_result",
	  parse: (value) => {
	    if (value == null || typeof value !== "object" || !("toolCallId" in value) || typeof value.toolCallId !== "string" || !("toolName" in value) || typeof value.toolName !== "string" || !("args" in value) || typeof value.args !== "object" || !("result" in value)) {
	      throw new Error(
	        '"tool_result" parts expect an object with a "toolCallId", "toolName", "args", and "result" property.'
	      );
	    }
	    return {
	      type: "tool_result",
	      value
	    };
	  }
	};
	var streamParts = [
	  textStreamPart,
	  functionCallStreamPart,
	  dataStreamPart,
	  errorStreamPart,
	  assistantMessageStreamPart,
	  assistantControlDataStreamPart,
	  dataMessageStreamPart,
	  toolCallsStreamPart,
	  messageAnnotationsStreamPart,
	  toolCallStreamPart,
	  toolResultStreamPart
	];
	var streamPartsByCode = {
	  [textStreamPart.code]: textStreamPart,
	  [functionCallStreamPart.code]: functionCallStreamPart,
	  [dataStreamPart.code]: dataStreamPart,
	  [errorStreamPart.code]: errorStreamPart,
	  [assistantMessageStreamPart.code]: assistantMessageStreamPart,
	  [assistantControlDataStreamPart.code]: assistantControlDataStreamPart,
	  [dataMessageStreamPart.code]: dataMessageStreamPart,
	  [toolCallsStreamPart.code]: toolCallsStreamPart,
	  [messageAnnotationsStreamPart.code]: messageAnnotationsStreamPart,
	  [toolCallStreamPart.code]: toolCallStreamPart,
	  [toolResultStreamPart.code]: toolResultStreamPart
	};
	({
	  [textStreamPart.name]: textStreamPart.code,
	  [functionCallStreamPart.name]: functionCallStreamPart.code,
	  [dataStreamPart.name]: dataStreamPart.code,
	  [errorStreamPart.name]: errorStreamPart.code,
	  [assistantMessageStreamPart.name]: assistantMessageStreamPart.code,
	  [assistantControlDataStreamPart.name]: assistantControlDataStreamPart.code,
	  [dataMessageStreamPart.name]: dataMessageStreamPart.code,
	  [toolCallsStreamPart.name]: toolCallsStreamPart.code,
	  [messageAnnotationsStreamPart.name]: messageAnnotationsStreamPart.code,
	  [toolCallStreamPart.name]: toolCallStreamPart.code,
	  [toolResultStreamPart.name]: toolResultStreamPart.code
	});
	var validCodes = streamParts.map((part) => part.code);
	var parseStreamPart = (line) => {
	  const firstSeparatorIndex = line.indexOf(":");
	  if (firstSeparatorIndex === -1) {
	    throw new Error("Failed to parse stream string. No separator found.");
	  }
	  const prefix = line.slice(0, firstSeparatorIndex);
	  if (!validCodes.includes(prefix)) {
	    throw new Error(`Failed to parse stream string. Invalid code ${prefix}.`);
	  }
	  const code = prefix;
	  const textValue = line.slice(firstSeparatorIndex + 1);
	  const jsonValue = JSON.parse(textValue);
	  return streamPartsByCode[code].parse(jsonValue);
	};

	// shared/read-data-stream.ts
	var NEWLINE = "\n".charCodeAt(0);
	function concatChunks(chunks, totalLength) {
	  const concatenatedChunks = new Uint8Array(totalLength);
	  let offset = 0;
	  for (const chunk of chunks) {
	    concatenatedChunks.set(chunk, offset);
	    offset += chunk.length;
	  }
	  chunks.length = 0;
	  return concatenatedChunks;
	}
	async function* readDataStream(reader, {
	  isAborted
	} = {}) {
	  const decoder = new TextDecoder();
	  const chunks = [];
	  let totalLength = 0;
	  while (true) {
	    const { value } = await reader.read();
	    if (value) {
	      chunks.push(value);
	      totalLength += value.length;
	      if (value[value.length - 1] !== NEWLINE) {
	        continue;
	      }
	    }
	    if (chunks.length === 0) {
	      break;
	    }
	    const concatenatedChunks = concatChunks(chunks, totalLength);
	    totalLength = 0;
	    const streamParts2 = decoder.decode(concatenatedChunks, { stream: true }).split("\n").filter((line) => line !== "").map(parseStreamPart);
	    for (const streamPart of streamParts2) {
	      yield streamPart;
	    }
	    if (isAborted == null ? void 0 : isAborted()) {
	      reader.cancel();
	      break;
	    }
	  }
	}

	// shared/parse-complex-response.ts
	function assignAnnotationsToMessage(message, annotations) {
	  if (!message || !annotations || !annotations.length)
	    return message;
	  return { ...message, annotations: [...annotations] };
	}
	async function parseComplexResponse({
	  reader,
	  abortControllerRef,
	  update,
	  onFinish,
	  generateId: generateId2 = generateId,
	  getCurrentDate = () => /* @__PURE__ */ new Date()
	}) {
	  const createdAt = getCurrentDate();
	  const prefixMap = {
	    data: []
	  };
	  let message_annotations = void 0;
	  for await (const { type, value } of readDataStream(reader, {
	    isAborted: () => (abortControllerRef == null ? void 0 : abortControllerRef.current) === null
	  })) {
	    if (type === "text") {
	      if (prefixMap["text"]) {
	        prefixMap["text"] = {
	          ...prefixMap["text"],
	          content: (prefixMap["text"].content || "") + value
	        };
	      } else {
	        prefixMap["text"] = {
	          id: generateId2(),
	          role: "assistant",
	          content: value,
	          createdAt
	        };
	      }
	    }
	    if (type === "tool_call") {
	      if (prefixMap.text == null) {
	        prefixMap.text = {
	          id: generateId2(),
	          role: "assistant",
	          content: "",
	          createdAt
	        };
	      }
	      if (prefixMap.text.toolInvocations == null) {
	        prefixMap.text.toolInvocations = [];
	      }
	      prefixMap.text.toolInvocations.push(value);
	    } else if (type === "tool_result") {
	      if (prefixMap.text == null) {
	        prefixMap.text = {
	          id: generateId2(),
	          role: "assistant",
	          content: "",
	          createdAt
	        };
	      }
	      if (prefixMap.text.toolInvocations == null) {
	        prefixMap.text.toolInvocations = [];
	      }
	      const toolInvocationIndex = prefixMap.text.toolInvocations.findIndex(
	        (invocation) => invocation.toolCallId === value.toolCallId
	      );
	      if (toolInvocationIndex !== -1) {
	        prefixMap.text.toolInvocations[toolInvocationIndex] = value;
	      } else {
	        prefixMap.text.toolInvocations.push(value);
	      }
	    }
	    let functionCallMessage = null;
	    if (type === "function_call") {
	      prefixMap["function_call"] = {
	        id: generateId2(),
	        role: "assistant",
	        content: "",
	        function_call: value.function_call,
	        name: value.function_call.name,
	        createdAt
	      };
	      functionCallMessage = prefixMap["function_call"];
	    }
	    let toolCallMessage = null;
	    if (type === "tool_calls") {
	      prefixMap["tool_calls"] = {
	        id: generateId2(),
	        role: "assistant",
	        content: "",
	        tool_calls: value.tool_calls,
	        createdAt
	      };
	      toolCallMessage = prefixMap["tool_calls"];
	    }
	    if (type === "data") {
	      prefixMap["data"].push(...value);
	    }
	    let responseMessage = prefixMap["text"];
	    if (type === "message_annotations") {
	      if (!message_annotations) {
	        message_annotations = [...value];
	      } else {
	        message_annotations.push(...value);
	      }
	      functionCallMessage = assignAnnotationsToMessage(
	        prefixMap["function_call"],
	        message_annotations
	      );
	      toolCallMessage = assignAnnotationsToMessage(
	        prefixMap["tool_calls"],
	        message_annotations
	      );
	      responseMessage = assignAnnotationsToMessage(
	        prefixMap["text"],
	        message_annotations
	      );
	    }
	    if (message_annotations == null ? void 0 : message_annotations.length) {
	      const messagePrefixKeys = [
	        "text",
	        "function_call",
	        "tool_calls"
	      ];
	      messagePrefixKeys.forEach((key) => {
	        if (prefixMap[key]) {
	          prefixMap[key].annotations = [...message_annotations];
	        }
	      });
	    }
	    const merged = [functionCallMessage, toolCallMessage, responseMessage].filter(Boolean).map((message) => ({
	      ...assignAnnotationsToMessage(message, message_annotations)
	    }));
	    update(merged, [...prefixMap["data"]]);
	  }
	  onFinish == null ? void 0 : onFinish(prefixMap);
	  return {
	    messages: [
	      prefixMap.text,
	      prefixMap.function_call,
	      prefixMap.tool_calls
	    ].filter(Boolean),
	    data: prefixMap.data
	  };
	}

	// shared/utils.ts
	function createChunkDecoder(complex) {
	  const decoder = new TextDecoder();
	  if (!complex) {
	    return function(chunk) {
	      if (!chunk)
	        return "";
	      return decoder.decode(chunk, { stream: true });
	    };
	  }
	  return function(chunk) {
	    const decoded = decoder.decode(chunk, { stream: true }).split("\n").filter((line) => line !== "");
	    return decoded.map(parseStreamPart).filter(Boolean);
	  };
	}

	// shared/call-chat-api.ts
	async function callChatApi({
	  api,
	  messages,
	  body,
	  streamMode = "stream-data",
	  credentials,
	  headers,
	  abortController,
	  restoreMessagesOnFailure,
	  onResponse,
	  onUpdate,
	  onFinish,
	  generateId: generateId2
	}) {
	  var _a;
	  const response = await fetch(api, {
	    method: "POST",
	    body: JSON.stringify({
	      messages,
	      ...body
	    }),
	    headers: {
	      "Content-Type": "application/json",
	      ...headers
	    },
	    signal: (_a = abortController == null ? void 0 : abortController()) == null ? void 0 : _a.signal,
	    credentials
	  }).catch((err) => {
	    restoreMessagesOnFailure();
	    throw err;
	  });
	  if (onResponse) {
	    try {
	      await onResponse(response);
	    } catch (err) {
	      throw err;
	    }
	  }
	  if (!response.ok) {
	    restoreMessagesOnFailure();
	    throw new Error(
	      await response.text() || "Failed to fetch the chat response."
	    );
	  }
	  if (!response.body) {
	    throw new Error("The response body is empty.");
	  }
	  const reader = response.body.getReader();
	  switch (streamMode) {
	    case "text": {
	      const decoder = createChunkDecoder();
	      const resultMessage = {
	        id: generateId2(),
	        createdAt: /* @__PURE__ */ new Date(),
	        role: "assistant",
	        content: ""
	      };
	      while (true) {
	        const { done, value } = await reader.read();
	        if (done) {
	          break;
	        }
	        resultMessage.content += decoder(value);
	        resultMessage.id = generateId2();
	        onUpdate([{ ...resultMessage }], []);
	        if ((abortController == null ? void 0 : abortController()) === null) {
	          reader.cancel();
	          break;
	        }
	      }
	      onFinish == null ? void 0 : onFinish(resultMessage);
	      return {
	        messages: [resultMessage],
	        data: []
	      };
	    }
	    case "stream-data": {
	      return await parseComplexResponse({
	        reader,
	        abortControllerRef: abortController != null ? { current: abortController() } : void 0,
	        update: onUpdate,
	        onFinish(prefixMap) {
	          if (onFinish && prefixMap.text != null) {
	            onFinish(prefixMap.text);
	          }
	        },
	        generateId: generateId2
	      });
	    }
	    default: {
	      const exhaustiveCheck = streamMode;
	      throw new Error(`Unknown stream mode: ${exhaustiveCheck}`);
	    }
	  }
	}

	// shared/process-chat-stream.ts
	async function processChatStream({
	  getStreamedResponse: getStreamedResponse2,
	  experimental_onFunctionCall,
	  experimental_onToolCall,
	  updateChatRequest,
	  getCurrentMessages
	}) {
	  while (true) {
	    const messagesAndDataOrJustMessage = await getStreamedResponse2();
	    if ("messages" in messagesAndDataOrJustMessage) {
	      let hasFollowingResponse = false;
	      for (const message of messagesAndDataOrJustMessage.messages) {
	        if ((message.function_call === void 0 || typeof message.function_call === "string") && (message.tool_calls === void 0 || typeof message.tool_calls === "string")) {
	          continue;
	        }
	        hasFollowingResponse = true;
	        if (experimental_onFunctionCall) {
	          const functionCall = message.function_call;
	          if (typeof functionCall !== "object") {
	            console.warn(
	              "experimental_onFunctionCall should not be defined when using tools"
	            );
	            continue;
	          }
	          const functionCallResponse = await experimental_onFunctionCall(
	            getCurrentMessages(),
	            functionCall
	          );
	          if (functionCallResponse === void 0) {
	            hasFollowingResponse = false;
	            break;
	          }
	          updateChatRequest(functionCallResponse);
	        }
	        if (experimental_onToolCall) {
	          const toolCalls = message.tool_calls;
	          if (!Array.isArray(toolCalls) || toolCalls.some((toolCall) => typeof toolCall !== "object")) {
	            console.warn(
	              "experimental_onToolCall should not be defined when using tools"
	            );
	            continue;
	          }
	          const toolCallResponse = await experimental_onToolCall(getCurrentMessages(), toolCalls);
	          if (toolCallResponse === void 0) {
	            hasFollowingResponse = false;
	            break;
	          }
	          updateChatRequest(toolCallResponse);
	        }
	      }
	      if (!hasFollowingResponse) {
	        break;
	      }
	    } else {
	      let fixFunctionCallArguments2 = function(response) {
	        for (const message of response.messages) {
	          if (message.tool_calls !== void 0) {
	            for (const toolCall of message.tool_calls) {
	              if (typeof toolCall === "object") {
	                if (toolCall.function.arguments && typeof toolCall.function.arguments !== "string") {
	                  toolCall.function.arguments = JSON.stringify(
	                    toolCall.function.arguments
	                  );
	                }
	              }
	            }
	          }
	          if (message.function_call !== void 0) {
	            if (typeof message.function_call === "object") {
	              if (message.function_call.arguments && typeof message.function_call.arguments !== "string") {
	                message.function_call.arguments = JSON.stringify(
	                  message.function_call.arguments
	                );
	              }
	            }
	          }
	        }
	      };
	      const streamedResponseMessage = messagesAndDataOrJustMessage;
	      if ((streamedResponseMessage.function_call === void 0 || typeof streamedResponseMessage.function_call === "string") && (streamedResponseMessage.tool_calls === void 0 || typeof streamedResponseMessage.tool_calls === "string")) {
	        break;
	      }
	      if (experimental_onFunctionCall) {
	        const functionCall = streamedResponseMessage.function_call;
	        if (!(typeof functionCall === "object")) {
	          console.warn(
	            "experimental_onFunctionCall should not be defined when using tools"
	          );
	          continue;
	        }
	        const functionCallResponse = await experimental_onFunctionCall(getCurrentMessages(), functionCall);
	        if (functionCallResponse === void 0)
	          break;
	        fixFunctionCallArguments2(functionCallResponse);
	        updateChatRequest(functionCallResponse);
	      }
	      if (experimental_onToolCall) {
	        const toolCalls = streamedResponseMessage.tool_calls;
	        if (!(typeof toolCalls === "object")) {
	          console.warn(
	            "experimental_onToolCall should not be defined when using functions"
	          );
	          continue;
	        }
	        const toolCallResponse = await experimental_onToolCall(getCurrentMessages(), toolCalls);
	        if (toolCallResponse === void 0)
	          break;
	        fixFunctionCallArguments2(toolCallResponse);
	        updateChatRequest(toolCallResponse);
	      }
	    }
	  }
	}

	// svelte/use-chat.ts
	var getStreamedResponse = async (api, chatRequest, mutate, mutateStreamData, existingData, extraMetadata, previousMessages, abortControllerRef, generateId2, streamMode, onFinish, onResponse, sendExtraMessageFields) => {
	  var _a, _b;
	  mutate(chatRequest.messages);
	  const constructedMessagesPayload = sendExtraMessageFields ? chatRequest.messages : chatRequest.messages.map(
	    ({ role, content, name, function_call, tool_calls, tool_call_id }) => ({
	      role,
	      content,
	      tool_call_id,
	      ...name !== void 0 && { name },
	      ...function_call !== void 0 && {
	        function_call
	      },
	      ...tool_calls !== void 0 && {
	        tool_calls
	      }
	    })
	  );
	  return await callChatApi({
	    api,
	    messages: constructedMessagesPayload,
	    body: {
	      ...extraMetadata.body,
	      ...(_a = chatRequest.options) == null ? void 0 : _a.body,
	      ...chatRequest.functions !== void 0 && {
	        functions: chatRequest.functions
	      },
	      ...chatRequest.function_call !== void 0 && {
	        function_call: chatRequest.function_call
	      },
	      ...chatRequest.tools !== void 0 && {
	        tools: chatRequest.tools
	      },
	      ...chatRequest.tool_choice !== void 0 && {
	        tool_choice: chatRequest.tool_choice
	      }
	    },
	    streamMode,
	    credentials: extraMetadata.credentials,
	    headers: {
	      ...extraMetadata.headers,
	      ...(_b = chatRequest.options) == null ? void 0 : _b.headers
	    },
	    abortController: () => abortControllerRef,
	    restoreMessagesOnFailure() {
	      mutate(previousMessages);
	    },
	    onResponse,
	    onUpdate(merged, data) {
	      mutate([...chatRequest.messages, ...merged]);
	      mutateStreamData([...existingData || [], ...data || []]);
	    },
	    onFinish,
	    generateId: generateId2
	  });
	};
	var uniqueId = 0;
	var store = {};
	function useChat({
	  api = "/api/chat",
	  id,
	  initialMessages = [],
	  initialInput = "",
	  sendExtraMessageFields,
	  experimental_onFunctionCall,
	  experimental_onToolCall,
	  streamMode,
	  onResponse,
	  onFinish,
	  onError,
	  credentials,
	  headers,
	  body,
	  generateId: generateId2 = generateId
	} = {}) {
	  const chatId = id || `chat-${uniqueId++}`;
	  const key = `${api}|${chatId}`;
	  const {
	    data,
	    mutate: originalMutate,
	    isLoading: isSWRLoading
	  } = F2(key, {
	    fetcher: () => store[key] || initialMessages,
	    fallbackData: initialMessages
	  });
	  const streamData = writable(void 0);
	  const loading = writable(false);
	  data.set(initialMessages);
	  const mutate = (data2) => {
	    store[key] = data2;
	    return originalMutate(data2);
	  };
	  const messages = data;
	  let abortController = null;
	  const extraMetadata = {
	    credentials,
	    headers,
	    body
	  };
	  const error = writable(void 0);
	  async function triggerRequest(chatRequest) {
	    try {
	      error.set(void 0);
	      loading.set(true);
	      abortController = new AbortController();
	      await processChatStream({
	        getStreamedResponse: () => getStreamedResponse(
	          api,
	          chatRequest,
	          mutate,
	          (data2) => {
	            streamData.set(data2);
	          },
	          get_store_value(streamData),
	          extraMetadata,
	          get_store_value(messages),
	          abortController,
	          generateId2,
	          streamMode,
	          onFinish,
	          onResponse,
	          sendExtraMessageFields
	        ),
	        experimental_onFunctionCall,
	        experimental_onToolCall,
	        updateChatRequest: (chatRequestParam) => {
	          chatRequest = chatRequestParam;
	        },
	        getCurrentMessages: () => get_store_value(messages)
	      });
	      abortController = null;
	      return null;
	    } catch (err) {
	      if (err.name === "AbortError") {
	        abortController = null;
	        return null;
	      }
	      if (onError && err instanceof Error) {
	        onError(err);
	      }
	      error.set(err);
	    } finally {
	      loading.set(false);
	    }
	  }
	  const append = async (message, {
	    options,
	    functions,
	    function_call,
	    tools,
	    tool_choice
	  } = {}) => {
	    if (!message.id) {
	      message.id = generateId2();
	    }
	    const chatRequest = {
	      messages: get_store_value(messages).concat(message),
	      options,
	      ...functions !== void 0 && { functions },
	      ...function_call !== void 0 && { function_call },
	      ...tools !== void 0 && { tools },
	      ...tool_choice !== void 0 && { tool_choice }
	    };
	    return triggerRequest(chatRequest);
	  };
	  const reload = async ({
	    options,
	    functions,
	    function_call,
	    tools,
	    tool_choice
	  } = {}) => {
	    const messagesSnapshot = get_store_value(messages);
	    if (messagesSnapshot.length === 0)
	      return null;
	    const lastMessage = messagesSnapshot.at(-1);
	    if ((lastMessage == null ? void 0 : lastMessage.role) === "assistant") {
	      const chatRequest2 = {
	        messages: messagesSnapshot.slice(0, -1),
	        options,
	        ...functions !== void 0 && { functions },
	        ...function_call !== void 0 && { function_call },
	        ...tools !== void 0 && { tools },
	        ...tool_choice !== void 0 && { tool_choice }
	      };
	      return triggerRequest(chatRequest2);
	    }
	    const chatRequest = {
	      messages: messagesSnapshot,
	      options,
	      ...functions !== void 0 && { functions },
	      ...function_call !== void 0 && { function_call },
	      ...tools !== void 0 && { tools },
	      ...tool_choice !== void 0 && { tool_choice }
	    };
	    return triggerRequest(chatRequest);
	  };
	  const stop = () => {
	    if (abortController) {
	      abortController.abort();
	      abortController = null;
	    }
	  };
	  const setMessages = (messages2) => {
	    mutate(messages2);
	  };
	  const input = writable(initialInput);
	  const handleSubmit = (e, options = {}) => {
	    e.preventDefault();
	    const inputValue = get_store_value(input);
	    if (!inputValue)
	      return;
	    append(
	      {
	        content: inputValue,
	        role: "user",
	        createdAt: /* @__PURE__ */ new Date()
	      },
	      options
	    );
	    input.set("");
	  };
	  const isLoading = derived(
	    [isSWRLoading, loading],
	    ([$isSWRLoading, $loading]) => {
	      return $isSWRLoading || $loading;
	    }
	  );
	  return {
	    messages,
	    error,
	    append,
	    reload,
	    stop,
	    setMessages,
	    input,
	    handleSubmit,
	    isLoading,
	    data: streamData
	  };
	}

	/* src/components/Chat.svelte generated by Svelte v4.2.17 */
	const file$2 = "src/components/Chat.svelte";

	function get_each_context(ctx, list, i) {
		const child_ctx = ctx.slice();
		child_ctx[8] = list[i];
		return child_ctx;
	}

	// (33:6) {#each chatMessages as message}
	function create_each_block(ctx) {
		let li;
		let t0_value = /*message*/ ctx[8].role + "";
		let t0;
		let t1;
		let t2_value = /*message*/ ctx[8].content + "";
		let t2;

		const block = {
			c: function create() {
				li = element("li");
				t0 = text(t0_value);
				t1 = text(": ");
				t2 = text(t2_value);
				attr_dev(li, "class", "svelte-1509ki1");
				add_location(li, file$2, 33, 8, 876);
			},
			m: function mount(target, anchor) {
				insert_dev(target, li, anchor);
				append_dev(li, t0);
				append_dev(li, t1);
				append_dev(li, t2);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*chatMessages*/ 1 && t0_value !== (t0_value = /*message*/ ctx[8].role + "")) set_data_dev(t0, t0_value);
				if (dirty & /*chatMessages*/ 1 && t2_value !== (t2_value = /*message*/ ctx[8].content + "")) set_data_dev(t2, t2_value);
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(li);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_each_block.name,
			type: "each",
			source: "(33:6) {#each chatMessages as message}",
			ctx
		});

		return block;
	}

	// (36:6) {#if streamingMessage}
	function create_if_block$1(ctx) {
		let li;
		let t0;
		let t1;

		const block = {
			c: function create() {
				li = element("li");
				t0 = text("assistant: ");
				t1 = text(/*streamingMessage*/ ctx[1]);
				attr_dev(li, "class", "svelte-1509ki1");
				add_location(li, file$2, 36, 8, 970);
			},
			m: function mount(target, anchor) {
				insert_dev(target, li, anchor);
				append_dev(li, t0);
				append_dev(li, t1);
			},
			p: function update(ctx, dirty) {
				if (dirty & /*streamingMessage*/ 2) set_data_dev(t1, /*streamingMessage*/ ctx[1]);
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(li);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block$1.name,
			type: "if",
			source: "(36:6) {#if streamingMessage}",
			ctx
		});

		return block;
	}

	function create_fragment$2(ctx) {
		let meta;
		let t0;
		let section;
		let h1;
		let t2;
		let ul;
		let t3;
		let t4;
		let form;
		let input_1;
		let t5;
		let button;
		let mounted;
		let dispose;
		let each_value = ensure_array_like_dev(/*chatMessages*/ ctx[0]);
		let each_blocks = [];

		for (let i = 0; i < each_value.length; i += 1) {
			each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
		}

		let if_block = /*streamingMessage*/ ctx[1] && create_if_block$1(ctx);

		const block = {
			c: function create() {
				meta = element("meta");
				t0 = space();
				section = element("section");
				h1 = element("h1");
				h1.textContent = "Chat with AI";
				t2 = space();
				ul = element("ul");

				for (let i = 0; i < each_blocks.length; i += 1) {
					each_blocks[i].c();
				}

				t3 = space();
				if (if_block) if_block.c();
				t4 = space();
				form = element("form");
				input_1 = element("input");
				t5 = space();
				button = element("button");
				button.textContent = "Send";
				document.title = "Chat";
				attr_dev(meta, "name", "description");
				attr_dev(meta, "content", "AI-powered chat using SvelteKit");
				add_location(meta, file$2, 26, 4, 693);
				attr_dev(h1, "class", "svelte-1509ki1");
				add_location(h1, file$2, 30, 4, 799);
				attr_dev(ul, "class", "svelte-1509ki1");
				add_location(ul, file$2, 31, 4, 825);
				attr_dev(input_1, "placeholder", "Type your message...");
				attr_dev(input_1, "class", "svelte-1509ki1");
				add_location(input_1, file$2, 40, 6, 1088);
				attr_dev(button, "type", "submit");
				attr_dev(button, "class", "svelte-1509ki1");
				add_location(button, file$2, 41, 6, 1159);
				attr_dev(form, "class", "svelte-1509ki1");
				add_location(form, file$2, 39, 4, 1035);
				attr_dev(section, "class", "svelte-1509ki1");
				add_location(section, file$2, 29, 2, 785);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				append_dev(document.head, meta);
				insert_dev(target, t0, anchor);
				insert_dev(target, section, anchor);
				append_dev(section, h1);
				append_dev(section, t2);
				append_dev(section, ul);

				for (let i = 0; i < each_blocks.length; i += 1) {
					if (each_blocks[i]) {
						each_blocks[i].m(ul, null);
					}
				}

				append_dev(ul, t3);
				if (if_block) if_block.m(ul, null);
				append_dev(section, t4);
				append_dev(section, form);
				append_dev(form, input_1);
				set_input_value(input_1, /*$input*/ ctx[2]);
				append_dev(form, t5);
				append_dev(form, button);

				if (!mounted) {
					dispose = [
						listen_dev(input_1, "input", /*input_1_input_handler*/ ctx[5]),
						listen_dev(form, "submit", prevent_default(/*handleSubmit*/ ctx[4]), false, true, false, false)
					];

					mounted = true;
				}
			},
			p: function update(ctx, [dirty]) {
				if (dirty & /*chatMessages*/ 1) {
					each_value = ensure_array_like_dev(/*chatMessages*/ ctx[0]);
					let i;

					for (i = 0; i < each_value.length; i += 1) {
						const child_ctx = get_each_context(ctx, each_value, i);

						if (each_blocks[i]) {
							each_blocks[i].p(child_ctx, dirty);
						} else {
							each_blocks[i] = create_each_block(child_ctx);
							each_blocks[i].c();
							each_blocks[i].m(ul, t3);
						}
					}

					for (; i < each_blocks.length; i += 1) {
						each_blocks[i].d(1);
					}

					each_blocks.length = each_value.length;
				}

				if (/*streamingMessage*/ ctx[1]) {
					if (if_block) {
						if_block.p(ctx, dirty);
					} else {
						if_block = create_if_block$1(ctx);
						if_block.c();
						if_block.m(ul, null);
					}
				} else if (if_block) {
					if_block.d(1);
					if_block = null;
				}

				if (dirty & /*$input*/ 4 && input_1.value !== /*$input*/ ctx[2]) {
					set_input_value(input_1, /*$input*/ ctx[2]);
				}
			},
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(t0);
					detach_dev(section);
				}

				detach_dev(meta);
				destroy_each(each_blocks, detaching);
				if (if_block) if_block.d();
				mounted = false;
				run_all(dispose);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$2.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$2($$self, $$props, $$invalidate) {
		let $input;
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('Chat', slots, []);
		const { input, handleSubmit, messages } = useChat();
		validate_store(input, 'input');
		component_subscribe($$self, input, value => $$invalidate(2, $input = value));
		let chatMessages = [];
		let streamingMessage = '';

		const unsubscribe = messages.subscribe(value => {
			if (value.length > chatMessages.length) {
				const lastMessage = value[value.length - 1];

				if (lastMessage.role === 'assistant') {
					$$invalidate(1, streamingMessage += lastMessage.content);
				} else {
					$$invalidate(0, chatMessages = [...chatMessages, lastMessage]);
					$$invalidate(1, streamingMessage = '');
				}
			}
		});

		onDestroy(unsubscribe);
		const writable_props = [];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Chat> was created with unknown prop '${key}'`);
		});

		function input_1_input_handler() {
			$input = this.value;
			input.set($input);
		}

		$$self.$capture_state = () => ({
			onDestroy,
			useChat,
			input,
			handleSubmit,
			messages,
			chatMessages,
			streamingMessage,
			unsubscribe,
			$input
		});

		$$self.$inject_state = $$props => {
			if ('chatMessages' in $$props) $$invalidate(0, chatMessages = $$props.chatMessages);
			if ('streamingMessage' in $$props) $$invalidate(1, streamingMessage = $$props.streamingMessage);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		return [
			chatMessages,
			streamingMessage,
			$input,
			input,
			handleSubmit,
			input_1_input_handler
		];
	}

	class Chat extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$2, create_fragment$2, safe_not_equal, {});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "Chat",
				options,
				id: create_fragment$2.name
			});
		}
	}

	/* src/components/ProgressBar.svelte generated by Svelte v4.2.17 */
	const file$1 = "src/components/ProgressBar.svelte";

	function create_fragment$1(ctx) {
		let div2;
		let div0;
		let t0;
		let div1;
		let span0;
		let t2;
		let span1;

		const block = {
			c: function create() {
				div2 = element("div");
				div0 = element("div");
				t0 = space();
				div1 = element("div");
				span0 = element("span");
				span0.textContent = "Industrial Revolution";
				t2 = space();
				span1 = element("span");
				span1.textContent = "The Singularity";
				attr_dev(div0, "class", "progress-bar svelte-1x9bggd");
				set_style(div0, "width", /*progress*/ ctx[0] + "%");
				add_location(div0, file$1, 5, 2, 124);
				attr_dev(span0, "class", "label-left svelte-1x9bggd");
				add_location(span0, file$1, 7, 4, 221);
				attr_dev(span1, "class", "label-right svelte-1x9bggd");
				add_location(span1, file$1, 8, 4, 279);
				attr_dev(div1, "class", "progress-labels svelte-1x9bggd");
				add_location(div1, file$1, 6, 2, 187);
				attr_dev(div2, "class", "progress-bar-container svelte-1x9bggd");
				add_location(div2, file$1, 4, 0, 85);
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				insert_dev(target, div2, anchor);
				append_dev(div2, div0);
				append_dev(div2, t0);
				append_dev(div2, div1);
				append_dev(div1, span0);
				append_dev(div1, t2);
				append_dev(div1, span1);
			},
			p: function update(ctx, [dirty]) {
				if (dirty & /*progress*/ 1) {
					set_style(div0, "width", /*progress*/ ctx[0] + "%");
				}
			},
			i: noop,
			o: noop,
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div2);
				}
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment$1.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance$1($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('ProgressBar', slots, []);
		let { progress = 0 } = $$props;
		const writable_props = ['progress'];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<ProgressBar> was created with unknown prop '${key}'`);
		});

		$$self.$$set = $$props => {
			if ('progress' in $$props) $$invalidate(0, progress = $$props.progress);
		};

		$$self.$capture_state = () => ({ progress });

		$$self.$inject_state = $$props => {
			if ('progress' in $$props) $$invalidate(0, progress = $$props.progress);
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		return [progress];
	}

	class ProgressBar extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance$1, create_fragment$1, safe_not_equal, { progress: 0 });

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "ProgressBar",
				options,
				id: create_fragment$1.name
			});
		}

		get progress() {
			throw new Error("<ProgressBar>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}

		set progress(value) {
			throw new Error("<ProgressBar>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
		}
	}

	/* src/App.svelte generated by Svelte v4.2.17 */
	const file = "src/App.svelte";

	// (37:0) {#if activeTab === 'Home'}
	function create_if_block_3(ctx) {
		let div1;
		let h1;
		let t1;
		let div0;
		let countdown;
		let t2;
		let progressbar;
		let t3;
		let h2;
		let t5;
		let mytimeline;
		let current;

		countdown = new Countdown({
				props: { targetDate: /*targetDate*/ ctx[2] },
				$$inline: true
			});

		progressbar = new ProgressBar({
				props: { progress: /*progressPercentage*/ ctx[1] },
				$$inline: true
			});

		mytimeline = new MyTimeline({ $$inline: true });

		const block = {
			c: function create() {
				div1 = element("div");
				h1 = element("h1");
				h1.textContent = "Time Left Until the Singularity:";
				t1 = space();
				div0 = element("div");
				create_component(countdown.$$.fragment);
				t2 = space();
				create_component(progressbar.$$.fragment);
				t3 = space();
				h2 = element("h2");
				h2.textContent = "Timeline of Events";
				t5 = space();
				create_component(mytimeline.$$.fragment);
				attr_dev(h1, "class", "text-center font-bold text-4xl mt-4 mb-2");
				add_location(h1, file, 38, 4, 1179);
				attr_dev(div0, "class", "countdown-container mt-1");
				add_location(div0, file, 39, 4, 1274);
				attr_dev(h2, "class", "text-center text-2xl mt-4");
				add_location(h2, file, 43, 4, 1413);
				attr_dev(div1, "class", "home-content");
				add_location(div1, file, 37, 2, 1148);
			},
			m: function mount(target, anchor) {
				insert_dev(target, div1, anchor);
				append_dev(div1, h1);
				append_dev(div1, t1);
				append_dev(div1, div0);
				mount_component(countdown, div0, null);
				append_dev(div0, t2);
				mount_component(progressbar, div0, null);
				append_dev(div1, t3);
				append_dev(div1, h2);
				append_dev(div1, t5);
				mount_component(mytimeline, div1, null);
				current = true;
			},
			p: function update(ctx, dirty) {
				const progressbar_changes = {};
				if (dirty & /*progressPercentage*/ 2) progressbar_changes.progress = /*progressPercentage*/ ctx[1];
				progressbar.$set(progressbar_changes);
			},
			i: function intro(local) {
				if (current) return;
				transition_in(countdown.$$.fragment, local);
				transition_in(progressbar.$$.fragment, local);
				transition_in(mytimeline.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(countdown.$$.fragment, local);
				transition_out(progressbar.$$.fragment, local);
				transition_out(mytimeline.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div1);
				}

				destroy_component(countdown);
				destroy_component(progressbar);
				destroy_component(mytimeline);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_3.name,
			type: "if",
			source: "(37:0) {#if activeTab === 'Home'}",
			ctx
		});

		return block;
	}

	// (49:0) {#if activeTab === 'About'}
	function create_if_block_2(ctx) {
		let div;
		let about;
		let current;
		about = new About({ $$inline: true });

		const block = {
			c: function create() {
				div = element("div");
				create_component(about.$$.fragment);
				add_location(div, file, 49, 2, 1540);
			},
			m: function mount(target, anchor) {
				insert_dev(target, div, anchor);
				mount_component(about, div, null);
				current = true;
			},
			i: function intro(local) {
				if (current) return;
				transition_in(about.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(about.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div);
				}

				destroy_component(about);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_2.name,
			type: "if",
			source: "(49:0) {#if activeTab === 'About'}",
			ctx
		});

		return block;
	}

	// (54:0) {#if activeTab === 'Contact'}
	function create_if_block_1(ctx) {
		let div;
		let contact;
		let current;
		contact = new Contact({ $$inline: true });

		const block = {
			c: function create() {
				div = element("div");
				create_component(contact.$$.fragment);
				add_location(div, file, 54, 2, 1607);
			},
			m: function mount(target, anchor) {
				insert_dev(target, div, anchor);
				mount_component(contact, div, null);
				current = true;
			},
			i: function intro(local) {
				if (current) return;
				transition_in(contact.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(contact.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div);
				}

				destroy_component(contact);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block_1.name,
			type: "if",
			source: "(54:0) {#if activeTab === 'Contact'}",
			ctx
		});

		return block;
	}

	// (60:0) {#if activeTab === 'Chat'}
	function create_if_block(ctx) {
		let div;
		let chat;
		let current;
		chat = new Chat({ $$inline: true });

		const block = {
			c: function create() {
				div = element("div");
				create_component(chat.$$.fragment);
				add_location(div, file, 60, 2, 1674);
			},
			m: function mount(target, anchor) {
				insert_dev(target, div, anchor);
				mount_component(chat, div, null);
				current = true;
			},
			i: function intro(local) {
				if (current) return;
				transition_in(chat.$$.fragment, local);
				current = true;
			},
			o: function outro(local) {
				transition_out(chat.$$.fragment, local);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(div);
				}

				destroy_component(chat);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_if_block.name,
			type: "if",
			source: "(60:0) {#if activeTab === 'Chat'}",
			ctx
		});

		return block;
	}

	function create_fragment(ctx) {
		let navbar;
		let t0;
		let t1;
		let t2;
		let t3;
		let if_block3_anchor;
		let current;
		navbar = new Navbar({ $$inline: true });
		navbar.$on("tabChange", /*tabChange_handler*/ ctx[3]);
		let if_block0 = /*activeTab*/ ctx[0] === 'Home' && create_if_block_3(ctx);
		let if_block1 = /*activeTab*/ ctx[0] === 'About' && create_if_block_2(ctx);
		let if_block2 = /*activeTab*/ ctx[0] === 'Contact' && create_if_block_1(ctx);
		let if_block3 = /*activeTab*/ ctx[0] === 'Chat' && create_if_block(ctx);

		const block = {
			c: function create() {
				create_component(navbar.$$.fragment);
				t0 = space();
				if (if_block0) if_block0.c();
				t1 = space();
				if (if_block1) if_block1.c();
				t2 = space();
				if (if_block2) if_block2.c();
				t3 = space();
				if (if_block3) if_block3.c();
				if_block3_anchor = empty();
			},
			l: function claim(nodes) {
				throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
			},
			m: function mount(target, anchor) {
				mount_component(navbar, target, anchor);
				insert_dev(target, t0, anchor);
				if (if_block0) if_block0.m(target, anchor);
				insert_dev(target, t1, anchor);
				if (if_block1) if_block1.m(target, anchor);
				insert_dev(target, t2, anchor);
				if (if_block2) if_block2.m(target, anchor);
				insert_dev(target, t3, anchor);
				if (if_block3) if_block3.m(target, anchor);
				insert_dev(target, if_block3_anchor, anchor);
				current = true;
			},
			p: function update(ctx, [dirty]) {
				if (/*activeTab*/ ctx[0] === 'Home') {
					if (if_block0) {
						if_block0.p(ctx, dirty);

						if (dirty & /*activeTab*/ 1) {
							transition_in(if_block0, 1);
						}
					} else {
						if_block0 = create_if_block_3(ctx);
						if_block0.c();
						transition_in(if_block0, 1);
						if_block0.m(t1.parentNode, t1);
					}
				} else if (if_block0) {
					group_outros();

					transition_out(if_block0, 1, 1, () => {
						if_block0 = null;
					});

					check_outros();
				}

				if (/*activeTab*/ ctx[0] === 'About') {
					if (if_block1) {
						if (dirty & /*activeTab*/ 1) {
							transition_in(if_block1, 1);
						}
					} else {
						if_block1 = create_if_block_2(ctx);
						if_block1.c();
						transition_in(if_block1, 1);
						if_block1.m(t2.parentNode, t2);
					}
				} else if (if_block1) {
					group_outros();

					transition_out(if_block1, 1, 1, () => {
						if_block1 = null;
					});

					check_outros();
				}

				if (/*activeTab*/ ctx[0] === 'Contact') {
					if (if_block2) {
						if (dirty & /*activeTab*/ 1) {
							transition_in(if_block2, 1);
						}
					} else {
						if_block2 = create_if_block_1(ctx);
						if_block2.c();
						transition_in(if_block2, 1);
						if_block2.m(t3.parentNode, t3);
					}
				} else if (if_block2) {
					group_outros();

					transition_out(if_block2, 1, 1, () => {
						if_block2 = null;
					});

					check_outros();
				}

				if (/*activeTab*/ ctx[0] === 'Chat') {
					if (if_block3) {
						if (dirty & /*activeTab*/ 1) {
							transition_in(if_block3, 1);
						}
					} else {
						if_block3 = create_if_block(ctx);
						if_block3.c();
						transition_in(if_block3, 1);
						if_block3.m(if_block3_anchor.parentNode, if_block3_anchor);
					}
				} else if (if_block3) {
					group_outros();

					transition_out(if_block3, 1, 1, () => {
						if_block3 = null;
					});

					check_outros();
				}
			},
			i: function intro(local) {
				if (current) return;
				transition_in(navbar.$$.fragment, local);
				transition_in(if_block0);
				transition_in(if_block1);
				transition_in(if_block2);
				transition_in(if_block3);
				current = true;
			},
			o: function outro(local) {
				transition_out(navbar.$$.fragment, local);
				transition_out(if_block0);
				transition_out(if_block1);
				transition_out(if_block2);
				transition_out(if_block3);
				current = false;
			},
			d: function destroy(detaching) {
				if (detaching) {
					detach_dev(t0);
					detach_dev(t1);
					detach_dev(t2);
					detach_dev(t3);
					detach_dev(if_block3_anchor);
				}

				destroy_component(navbar, detaching);
				if (if_block0) if_block0.d(detaching);
				if (if_block1) if_block1.d(detaching);
				if (if_block2) if_block2.d(detaching);
				if (if_block3) if_block3.d(detaching);
			}
		};

		dispatch_dev("SvelteRegisterBlock", {
			block,
			id: create_fragment.name,
			type: "component",
			source: "",
			ctx
		});

		return block;
	}

	function instance($$self, $$props, $$invalidate) {
		let { $$slots: slots = {}, $$scope } = $$props;
		validate_slots('App', slots, []);
		let activeTab = 'Home';
		const targetDate = new Date('2027-11-20').getTime();
		const startDate = new Date('1888-11-20').getTime();
		let progressPercentage = 0;
		let countdownInterval;

		function startProgressUpdate() {
			countdownInterval = setInterval(
				() => {
					updateProgress();
				},
				1000
			);
		}

		function updateProgress() {
			const currentTime = new Date().getTime();
			const totalDuration = targetDate - startDate;
			$$invalidate(1, progressPercentage = (currentTime - startDate) / totalDuration * 100);

			if (progressPercentage >= 100) {
				clearInterval(countdownInterval);
				$$invalidate(1, progressPercentage = 100);
			}
		}

		startProgressUpdate();
		const writable_props = [];

		Object.keys($$props).forEach(key => {
			if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<App> was created with unknown prop '${key}'`);
		});

		const tabChange_handler = e => $$invalidate(0, activeTab = e.detail.tab);

		$$self.$capture_state = () => ({
			Navbar,
			About,
			Contact,
			MyTimeline,
			Countdown,
			Chat,
			ProgressBar,
			activeTab,
			targetDate,
			startDate,
			progressPercentage,
			countdownInterval,
			startProgressUpdate,
			updateProgress
		});

		$$self.$inject_state = $$props => {
			if ('activeTab' in $$props) $$invalidate(0, activeTab = $$props.activeTab);
			if ('progressPercentage' in $$props) $$invalidate(1, progressPercentage = $$props.progressPercentage);
			if ('countdownInterval' in $$props) countdownInterval = $$props.countdownInterval;
		};

		if ($$props && "$$inject" in $$props) {
			$$self.$inject_state($$props.$$inject);
		}

		return [activeTab, progressPercentage, targetDate, tabChange_handler];
	}

	class App extends SvelteComponentDev {
		constructor(options) {
			super(options);
			init(this, options, instance, create_fragment, safe_not_equal, {});

			dispatch_dev("SvelteRegisterComponent", {
				component: this,
				tagName: "App",
				options,
				id: create_fragment.name
			});
		}
	}

	const app = new App({
	  target: document.body,
	});

	return app;

})();
//# sourceMappingURL=bundle.js.map
