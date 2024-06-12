import { c as create_ssr_component, v as validate_component, b as each, o as onDestroy, s as setContext, d as add_attribute, e as escape, f as compute_rest_props, g as getContext, h as spread, i as escape_attribute_value, j as escape_object } from './ssr-DH4u9ZHx.js';
import { N as Navbar_1, S as Spacer, B as BottomNav_1, t as twMerge, i as is_void } from './Spacer-fKOGNVLp.js';
import { M as MailchimpSignup } from './MailchimpSignup-CTqHLH3J.js';
import './index-mAg2Gvoi.js';
import './supabaseClient-DNeOHnRL.js';
import '@supabase/supabase-js';

const Button = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $$restProps = compute_rest_props($$props, ["pill", "outline", "size", "href", "type", "color", "shadow", "tag", "checked"]);
  const group = getContext("group");
  let { pill = false } = $$props;
  let { outline = false } = $$props;
  let { size = group ? "sm" : "md" } = $$props;
  let { href = void 0 } = $$props;
  let { type = "button" } = $$props;
  let { color = group ? outline ? "dark" : "alternative" : "primary" } = $$props;
  let { shadow = false } = $$props;
  let { tag = "button" } = $$props;
  let { checked = void 0 } = $$props;
  const colorClasses = {
    alternative: "text-gray-900 bg-white border border-gray-200 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-400 hover:text-primary-700 focus-within:text-primary-700 dark:focus-within:text-white dark:hover:text-white dark:hover:bg-gray-700",
    blue: "text-white bg-blue-700 hover:bg-blue-800 dark:bg-blue-600 dark:hover:bg-blue-700",
    dark: "text-white bg-gray-800 hover:bg-gray-900 dark:bg-gray-800 dark:hover:bg-gray-700",
    green: "text-white bg-green-700 hover:bg-green-800 dark:bg-green-600 dark:hover:bg-green-700",
    light: "text-gray-900 bg-white border border-gray-300 hover:bg-gray-100 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600",
    primary: "text-white bg-primary-700 hover:bg-primary-800 dark:bg-primary-600 dark:hover:bg-primary-700",
    purple: "text-white bg-purple-700 hover:bg-purple-800 dark:bg-purple-600 dark:hover:bg-purple-700",
    red: "text-white bg-red-700 hover:bg-red-800 dark:bg-red-600 dark:hover:bg-red-700",
    yellow: "text-white bg-yellow-400 hover:bg-yellow-500 ",
    none: ""
  };
  const colorCheckedClasses = {
    alternative: "text-primary-700 border dark:text-primary-500 bg-gray-100 dark:bg-gray-700 border-gray-300 shadow-gray-300 dark:shadow-gray-800 shadow-inner",
    blue: "text-blue-900 bg-blue-400 dark:bg-blue-500 shadow-blue-700 dark:shadow-blue-800 shadow-inner",
    dark: "text-white bg-gray-500 dark:bg-gray-600 shadow-gray-800 dark:shadow-gray-900 shadow-inner",
    green: "text-green-900 bg-green-400 dark:bg-green-500 shadow-green-700 dark:shadow-green-800 shadow-inner",
    light: "text-gray-900 bg-gray-100 border border-gray-300 dark:bg-gray-500 dark:text-gray-900 dark:border-gray-700 shadow-gray-300 dark:shadow-gray-700 shadow-inner",
    primary: "text-primary-900 bg-primary-400 dark:bg-primary-500 shadow-primary-700 dark:shadow-primary-800 shadow-inner",
    purple: "text-purple-900 bg-purple-400 dark:bg-purple-500 shadow-purple-700 dark:shadow-purple-800 shadow-inner",
    red: "text-red-900 bg-red-400 dark:bg-red-500 shadow-red-700 dark:shadow-red-800 shadow-inner",
    yellow: "text-yellow-900 bg-yellow-300 dark:bg-yellow-400 shadow-yellow-500 dark:shadow-yellow-700 shadow-inner",
    none: ""
  };
  const coloredFocusClasses = {
    alternative: "focus-within:ring-gray-200 dark:focus-within:ring-gray-700",
    blue: "focus-within:ring-blue-300 dark:focus-within:ring-blue-800",
    dark: "focus-within:ring-gray-300 dark:focus-within:ring-gray-700",
    green: "focus-within:ring-green-300 dark:focus-within:ring-green-800",
    light: "focus-within:ring-gray-200 dark:focus-within:ring-gray-700",
    primary: "focus-within:ring-primary-300 dark:focus-within:ring-primary-800",
    purple: "focus-within:ring-purple-300 dark:focus-within:ring-purple-900",
    red: "focus-within:ring-red-300 dark:focus-within:ring-red-900",
    yellow: "focus-within:ring-yellow-300 dark:focus-within:ring-yellow-900",
    none: ""
  };
  const coloredShadowClasses = {
    alternative: "shadow-gray-500/50 dark:shadow-gray-800/80",
    blue: "shadow-blue-500/50 dark:shadow-blue-800/80",
    dark: "shadow-gray-500/50 dark:shadow-gray-800/80",
    green: "shadow-green-500/50 dark:shadow-green-800/80",
    light: "shadow-gray-500/50 dark:shadow-gray-800/80",
    primary: "shadow-primary-500/50 dark:shadow-primary-800/80",
    purple: "shadow-purple-500/50 dark:shadow-purple-800/80",
    red: "shadow-red-500/50 dark:shadow-red-800/80 ",
    yellow: "shadow-yellow-500/50 dark:shadow-yellow-800/80 ",
    none: ""
  };
  const outlineClasses = {
    alternative: "text-gray-900 dark:text-gray-400 hover:text-white border border-gray-800 hover:bg-gray-900 focus-within:bg-gray-900 focus-within:text-white focus-within:ring-gray-300 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-600 dark:focus-within:ring-gray-800",
    blue: "text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-600",
    dark: "text-gray-900 hover:text-white border border-gray-800 hover:bg-gray-900 focus-within:bg-gray-900 focus-within:text-white dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-600",
    green: "text-green-700 hover:text-white border border-green-700 hover:bg-green-800 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600",
    light: "text-gray-500 hover:text-gray-900 bg-white border border-gray-200 dark:border-gray-600 dark:hover:text-white dark:text-gray-400 hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-600",
    primary: "text-primary-700 hover:text-white border border-primary-700 hover:bg-primary-700 dark:border-primary-500 dark:text-primary-500 dark:hover:text-white dark:hover:bg-primary-600",
    purple: "text-purple-700 hover:text-white border border-purple-700 hover:bg-purple-800 dark:border-purple-400 dark:text-purple-400 dark:hover:text-white dark:hover:bg-purple-500",
    red: "text-red-700 hover:text-white border border-red-700 hover:bg-red-800 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600",
    yellow: "text-yellow-400 hover:text-white border border-yellow-400 hover:bg-yellow-500 dark:border-yellow-300 dark:text-yellow-300 dark:hover:text-white dark:hover:bg-yellow-400",
    none: ""
  };
  const sizeClasses = {
    xs: "px-3 py-2 text-xs",
    sm: "px-4 py-2 text-sm",
    md: "px-5 py-2.5 text-sm",
    lg: "px-5 py-3 text-base",
    xl: "px-6 py-3.5 text-base"
  };
  const hasBorder = () => outline || color === "alternative" || color === "light";
  let buttonClass;
  if ($$props.pill === void 0 && $$bindings.pill && pill !== void 0)
    $$bindings.pill(pill);
  if ($$props.outline === void 0 && $$bindings.outline && outline !== void 0)
    $$bindings.outline(outline);
  if ($$props.size === void 0 && $$bindings.size && size !== void 0)
    $$bindings.size(size);
  if ($$props.href === void 0 && $$bindings.href && href !== void 0)
    $$bindings.href(href);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.color === void 0 && $$bindings.color && color !== void 0)
    $$bindings.color(color);
  if ($$props.shadow === void 0 && $$bindings.shadow && shadow !== void 0)
    $$bindings.shadow(shadow);
  if ($$props.tag === void 0 && $$bindings.tag && tag !== void 0)
    $$bindings.tag(tag);
  if ($$props.checked === void 0 && $$bindings.checked && checked !== void 0)
    $$bindings.checked(checked);
  buttonClass = twMerge(
    "text-center font-medium",
    group ? "focus-within:ring-2" : "focus-within:ring-4",
    group && "focus-within:z-10",
    group || "focus-within:outline-none",
    "inline-flex items-center justify-center " + sizeClasses[size],
    outline && checked && "border dark:border-gray-900",
    outline && checked && colorCheckedClasses[color],
    outline && !checked && outlineClasses[color],
    !outline && checked && colorCheckedClasses[color],
    !outline && !checked && colorClasses[color],
    color === "alternative" && (group && !checked ? "dark:bg-gray-700 dark:text-white dark:border-gray-700 dark:hover:border-gray-600 dark:hover:bg-gray-600" : "dark:bg-transparent dark:border-gray-600 dark:hover:border-gray-600"),
    outline && color === "dark" && (group ? checked ? "bg-gray-900 border-gray-800 dark:border-white dark:bg-gray-600" : "dark:text-white border-gray-800 dark:border-white" : "dark:text-gray-400 dark:border-gray-700"),
    coloredFocusClasses[color],
    hasBorder() && group && "border-s-0 first:border-s",
    group ? pill && "first:rounded-s-full last:rounded-e-full" || "first:rounded-s-lg last:rounded-e-lg" : pill && "rounded-full" || "rounded-lg",
    shadow && "shadow-lg",
    shadow && coloredShadowClasses[color],
    $$restProps.disabled && "cursor-not-allowed opacity-50",
    $$props.class
  );
  return `${href && !$$restProps.disabled ? `<a${spread(
    [
      { href: escape_attribute_value(href) },
      escape_object($$restProps),
      {
        class: escape_attribute_value(buttonClass)
      },
      { role: "button" }
    ],
    {}
  )}>${slots.default ? slots.default({}) : ``}</a>` : `${tag === "button" && !$$restProps.disabled ? `<button${spread(
    [
      { type: escape_attribute_value(type) },
      escape_object($$restProps),
      {
        class: escape_attribute_value(buttonClass)
      }
    ],
    {}
  )}>${slots.default ? slots.default({}) : ``}</button>` : `${((tag$1) => {
    return tag$1 ? `<${tag}${add_attribute("class", buttonClass, 0)}>${is_void(tag$1) ? "" : `${slots.default ? slots.default({}) : ``}`}${is_void(tag$1) ? "" : `</${tag$1}>`}` : "";
  })(tag)}`}`} `;
});
const Timeline = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { order = "default" } = $$props;
  setContext("order", order);
  let olClasses = {
    group: "p-5 mb-4 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700",
    horizontal: "sm:flex",
    activity: "relative border-s border-gray-200 dark:border-gray-700",
    vertical: "relative border-s border-gray-200 dark:border-gray-700",
    default: "relative border-s border-gray-200 dark:border-gray-700"
  };
  if ($$props.order === void 0 && $$bindings.order && order !== void 0)
    $$bindings.order(order);
  return `<ol${add_attribute("class", twMerge(olClasses[order], $$props.class), 0)}>${slots.default ? slots.default({}) : ``}</ol> `;
});
const TimelineItem = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { title = "" } = $$props;
  let { date = "" } = $$props;
  let { svgClass = "w-3 h-3 text-primary-600 dark:text-primary-400" } = $$props;
  let order = "default";
  order = getContext("order");
  const liClasses = {
    default: "mb-10 ms-4",
    vertical: "mb-10 ms-6",
    horizontal: "relative mb-6 sm:mb-0",
    activity: "mb-10 ms-6",
    group: ""
  };
  const divClasses = {
    default: "absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700",
    vertical: "flex absolute -start-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900",
    horizontal: "flex items-center",
    activity: "flex absolute -start-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900",
    group: "p-5 mb-4 bg-gray-50 rounded-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700"
  };
  const timeClasses = {
    default: "mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500",
    vertical: "block mb-2 text-sm font-normal leading-none text-gray-400 dark:text-gray-500",
    horizontal: "block mb-2 text-sm font-normal leading-none text-gray-400 dark:text-gray-500",
    activity: "mb-1 text-xs font-normal text-gray-400 sm:order-last sm:mb-0",
    group: "text-lg font-semibold text-gray-900 dark:text-white"
  };
  let liCls = twMerge(liClasses[order], $$props.classLi);
  let divCls = twMerge(divClasses[order], $$props.classDiv);
  let timeCls = twMerge(timeClasses[order], $$props.classTime);
  const h3Cls = twMerge(
    order === "vertical" ? "flex items-center mb-1 text-lg font-semibold text-gray-900 dark:text-white" : "text-lg font-semibold text-gray-900 dark:text-white",
    $$props.classH3
  );
  if ($$props.title === void 0 && $$bindings.title && title !== void 0)
    $$bindings.title(title);
  if ($$props.date === void 0 && $$bindings.date && date !== void 0)
    $$bindings.date(date);
  if ($$props.svgClass === void 0 && $$bindings.svgClass && svgClass !== void 0)
    $$bindings.svgClass(svgClass);
  return `<li${add_attribute("class", liCls, 0)}><div${add_attribute("class", divCls, 0)}></div> ${order !== "default" ? `${slots.icon ? slots.icon({}) : ` <svg aria-hidden="true"${add_attribute("class", svgClass, 0)} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path></svg> `}` : `${date ? `<time${add_attribute("class", timeCls, 0)}>${escape(date)}</time>` : ``}`} ${title ? `<h3${add_attribute("class", h3Cls, 0)}>${escape(title)}</h3>` : ``} ${order !== "default" ? `${date ? `<time${add_attribute("class", timeCls, 0)}>${escape(date)}</time>` : ``}` : ``} ${slots.default ? slots.default({}) : ``}</li> `;
});
const ArrowRightOutline = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $$restProps = compute_rest_props($$props, ["size", "role", "color", "withEvents", "title", "strokeWidth", "desc", "ariaLabel"]);
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
  if ($$props.size === void 0 && $$bindings.size && size !== void 0)
    $$bindings.size(size);
  if ($$props.role === void 0 && $$bindings.role && role !== void 0)
    $$bindings.role(role);
  if ($$props.color === void 0 && $$bindings.color && color !== void 0)
    $$bindings.color(color);
  if ($$props.withEvents === void 0 && $$bindings.withEvents && withEvents !== void 0)
    $$bindings.withEvents(withEvents);
  if ($$props.title === void 0 && $$bindings.title && title !== void 0)
    $$bindings.title(title);
  if ($$props.strokeWidth === void 0 && $$bindings.strokeWidth && strokeWidth !== void 0)
    $$bindings.strokeWidth(strokeWidth);
  if ($$props.desc === void 0 && $$bindings.desc && desc !== void 0)
    $$bindings.desc(desc);
  if ($$props.ariaLabel === void 0 && $$bindings.ariaLabel && ariaLabel !== void 0)
    $$bindings.ariaLabel(ariaLabel);
  {
    if (title.id || desc.id) {
      hasDescription = true;
    } else {
      hasDescription = false;
    }
  }
  return `${withEvents ? `<svg${spread(
    [
      { xmlns: "http://www.w3.org/2000/svg" },
      { fill: "none" },
      { color: escape_attribute_value(color) },
      escape_object($$restProps),
      {
        class: escape_attribute_value(twMerge("shrink-0", sizes[size ?? "md"], $$props.class))
      },
      { role: escape_attribute_value(role) },
      {
        "aria-label": escape_attribute_value(ariaLabel)
      },
      {
        "aria-describedby": escape_attribute_value(hasDescription ? ariaDescribedby : void 0)
      },
      { viewBox: "0 0 24 24" }
    ],
    {}
  )}>${title.id && title.title ? `<title${add_attribute("id", title.id, 0)}>${escape(title.title)}</title>` : ``}${desc.id && desc.desc ? `<desc${add_attribute("id", desc.id, 0)}>${escape(desc.desc)}</desc>` : ``}<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"${add_attribute("stroke-width", strokeWidth, 0)} d="M19 12H5m14 0-4 4m4-4-4-4"></path></svg>` : `<svg${spread(
    [
      { xmlns: "http://www.w3.org/2000/svg" },
      { fill: "none" },
      { color: escape_attribute_value(color) },
      escape_object($$restProps),
      {
        class: escape_attribute_value(twMerge("shrink-0", sizes[size ?? "md"], $$props.class))
      },
      { role: escape_attribute_value(role) },
      {
        "aria-label": escape_attribute_value(ariaLabel)
      },
      {
        "aria-describedby": escape_attribute_value(hasDescription ? ariaDescribedby : void 0)
      },
      { viewBox: "0 0 24 24" }
    ],
    {}
  )}>${title.id && title.title ? `<title${add_attribute("id", title.id, 0)}>${escape(title.title)}</title>` : ``}${desc.id && desc.desc ? `<desc${add_attribute("id", desc.id, 0)}>${escape(desc.desc)}</desc>` : ``}<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"${add_attribute("stroke-width", strokeWidth, 0)} d="M19 12H5m14 0-4 4m4-4-4-4"></path></svg>`} `;
});
const timelineItems = [
  {
    id: 1,
    title: "Sumerian Abacus",
    abstract: "The inception of computational tools with the creation of the abacus around 3000 BC.",
    description: "The inception of computational tools with the creation of the abacus around 3000 BC.",
    date: "-3000-02-02",
    urls: {
      main: "https://www.example.com/sumerian_abacus",
      wikipedia: "https://en.wikipedia.org/wiki/Abacus"
    }
  },
  {
    id: 2,
    title: "Antikythera Mechanism",
    abstract: "The Antikythera Mechanism, an ancient analog computer, demonstrates early mechanical computation for astronomical predictions between 100 BCE and 100 CE.",
    description: "The Antikythera Mechanism, an ancient analog computer, demonstrates early mechanical computation for astronomical predictions between 100 BCE and 100 CE.",
    date: "0100-03-03",
    urls: {
      main: "https://www.example.com/antikythera_mechanism",
      wikipedia: "https://en.wikipedia.org/wiki/Antikythera_mechanism"
    }
  },
  {
    id: 3,
    title: "Al-Khwarizmi's Algorithmic Foundations",
    abstract: "Al-Khwarizmi establishes the basis for algorithmic thinking and computational methods around 825 CE.",
    description: "Al-Khwarizmi establishes the basis for algorithmic thinking and computational methods around 825 CE.",
    date: "0825-11-11",
    urls: {
      main: "https://www.example.com/al-khwarizmis_algorithmic_foundations",
      wikipedia: "https://en.wikipedia.org/wiki/Al-Khwarizmi"
    }
  },
  {
    id: 4,
    title: "The Astrolabe's Refinement",
    abstract: "The astrolabe, an ancient analog computer, is refined during the 1200s, showcasing mechanical computation for celestial navigation.",
    description: "The astrolabe, an ancient analog computer, is refined during the 1200s, showcasing mechanical computation for celestial navigation.",
    date: "1200-04-01",
    urls: {
      main: "https://www.example.com/astrolabes_refinement",
      wikipedia: "https://en.wikipedia.org/wiki/Astrolabe"
    }
  },
  {
    id: 5,
    title: "Gutenberg's Printing Press",
    abstract: "Gutenberg's invention of the printing press in 1450 facilitates the broad dissemination of scientific and mathematical knowledge.",
    description: "Gutenberg's invention of the printing press in 1450 facilitates the broad dissemination of scientific and mathematical knowledge.",
    date: "1450-09-12",
    urls: {
      main: "https://www.example.com/gutenbergs_printing_press",
      wikipedia: "https://en.wikipedia.org/wiki/Printing_press"
    }
  },
  {
    id: 6,
    title: "Napier's Bones",
    abstract: "John Napier invents 'Napier's Bones,' a manual calculation device for multiplication and division, in 1617.",
    description: "John Napier invents 'Napier's Bones,' a manual calculation device for multiplication and division, in 1617.",
    date: "1617-01-01",
    urls: {
      main: "https://www.example.com/napier_bones",
      wikipedia: "https://en.wikipedia.org/wiki/Napier's_bones"
    }
  },
  {
    id: 7,
    title: "Pascal's Calculating Machine",
    abstract: "Blaise Pascal invents the mechanical calculator, one of the first calculating machines, in 1642.",
    description: "Blaise Pascal invents the mechanical calculator, one of the first calculating machines, in 1642.",
    date: "1642-01-01",
    urls: {
      main: "https://www.example.com/pascals_calculating_machine",
      wikipedia: "https://en.wikipedia.org/wiki/Pascal's_calculator"
    }
  },
  {
    id: 8,
    title: "Leibniz's Stepped Reckoner",
    abstract: "Gottfried Wilhelm Leibniz invents the 'Stepped Reckoner,' a mechanical calculator capable of multiplication and division, in 1673.",
    description: "Gottfried Wilhelm Leibniz invents the 'Stepped Reckoner,' a mechanical calculator capable of multiplication and division, in 1673.",
    date: "1673-01-01",
    urls: {
      main: "https://www.example.com/leibnizs_stepped_reckoner",
      wikipedia: "https://en.wikipedia.org/wiki/Stepped_reckoner"
    }
  },
  {
    id: 9,
    title: "Jacquard's Loom",
    abstract: "Joseph Marie Jacquard invents the Jacquard loom, a programmable machine using punched cards, in 1801.",
    description: "Joseph Marie Jacquard invents the Jacquard loom, a programmable machine using punched cards, in 1801.",
    date: "1801-01-01",
    urls: {
      main: "https://www.example.com/jacquards_loom",
      wikipedia: "https://en.wikipedia.org/wiki/Jacquard_loom"
    }
  },
  {
    id: 10,
    title: "Babbage's Analytical Engine",
    abstract: "Charles Babbage conceives the design for the Analytical Engine, a pioneering general-purpose mechanical computer, in 1837.",
    description: "Charles Babbage conceives the design for the Analytical Engine, a pioneering general-purpose mechanical computer, in 1837.",
    date: "1837-01-01",
    urls: {
      main: "https://www.example.com/babbages_analytical_engine",
      wikipedia: "https://en.wikipedia.org/wiki/Analytical_engine"
    }
  },
  {
    id: 11,
    title: "Neural Networks and Machine Learning",
    abstract: "The early concepts and foundations of neural networks are laid in the 1940s and 1950s, laying the groundwork for creating intelligent systems that can learn and adapt, a crucial step towards the pursuit of technological singularity.",
    description: "The early concepts and foundations of neural networks are laid in the 1940s and 1950s, laying the groundwork for creating intelligent systems that can learn and adapt, a crucial step towards the pursuit of technological singularity.",
    date: "1950-01-01",
    urls: {
      main: "https://www.example.com/neural_networks_and_machine_learning",
      wikipedia: "https://en.wikipedia.org/wiki/Neural_networks"
    }
  },
  {
    id: 12,
    title: "High-Level Programming Languages",
    abstract: "The development of high-level programming languages, such as FORTRAN, LISP, and COBOL, in the late 1950s and early 1960s, makes programming more accessible and efficient.",
    description: "The development of high-level programming languages, such as FORTRAN, LISP, and COBOL, in the late 1950s and early 1960s, makes programming more accessible and efficient.",
    date: "1959-01-01",
    urls: {
      main: "https://www.example.com/high_level_programming_languages",
      wikipedia: "https://en.wikipedia.org/wiki/High-level_programming_language"
    }
  },
  {
    id: 13,
    title: "Integrated Circuit",
    abstract: "The integrated circuit, a single chip containing transistors and other components, is independently invented by Jack Kilby and Robert Noyce in 1958-1959, revolutionizing electronics and enabling modern computing.",
    description: "The integrated circuit, a single chip containing transistors and other components, is independently invented by Jack Kilby and Robert Noyce in 1958-1959, revolutionizing electronics and enabling modern computing.",
    date: "1959-01-01",
    urls: {
      main: "https://www.example.com/integrated_circuit",
      wikipedia: "https://en.wikipedia.org/wiki/Integrated_circuit"
    }
  },
  {
    id: 14,
    title: "ASCII and Character Encoding Standards",
    abstract: "The American Standard Code for Information Interchange (ASCII) is published as a standard for electronic communication in 1963, enabling interoperability and data exchange.",
    description: "The American Standard Code for Information Interchange (ASCII) is published as a standard for electronic communication in 1963, enabling interoperability and data exchange.",
    date: "1963-01-01",
    urls: {
      main: "https://www.example.com/ascii_and_character_encoding",
      wikipedia: "https://en.wikipedia.org/wiki/ASCII"
    }
  },
  {
    id: 15,
    title: "Unix Operating System",
    abstract: "The Unix operating system, a pioneering and influential multi-user, multi-tasking system, is developed at Bell Labs in the early 1970s.",
    description: "The Unix operating system, a pioneering and influential multi-user, multi-tasking system, is developed at Bell Labs in the early 1970s.",
    date: "1973-01-01",
    urls: {
      main: "https://www.example.com/unix_operating_system",
      wikipedia: "https://en.wikipedia.org/wiki/Unix"
    }
  },
  {
    id: 16,
    title: "Personal Computing Revolution",
    abstract: "The personal computing revolution begins in the 1970s, democratizing access to computing power and laying the foundation for future advancements in artificial intelligence and the pursuit of technological singularity.",
    description: "The personal computing revolution begins in the 1970s, democratizing access to computing power and laying the foundation for future advancements in artificial intelligence and the pursuit of technological singularity.",
    date: "1977-01-01",
    urls: {
      main: "https://www.example.com/personal_computing_revolution",
      wikipedia: "https://en.wikipedia.org/wiki/Personal_computer_revolution"
    }
  },
  {
    id: 17,
    title: "Quantum Computing",
    abstract: "Quantum computing, a revolutionary paradigm of computation based on quantum mechanics, is proposed in the 1980s and continues to advance in the pursuit of solving complex problems beyond the reach of classical computers.",
    description: "Quantum computing, a revolutionary paradigm of computation based on quantum mechanics, is proposed in the 1980s and continues to advance in the pursuit of solving complex problems beyond the reach of classical computers.",
    date: "1980-01-01",
    urls: {
      main: "https://www.example.com/quantum_computing",
      wikipedia: "https://en.wikipedia.org/wiki/Quantum_computing"
    }
  },
  {
    id: 18,
    title: "Transformer Architecture and Attention Mechanism",
    abstract: "The introduction of the Transformer architecture and attention mechanism in 2017 revolutionizes natural language processing and paves the way for breakthroughs in language models.",
    description: "The introduction of the Transformer architecture and attention mechanism in 2017 revolutionizes natural language processing and paves the way for breakthroughs in language models.",
    date: "2017-01-01",
    urls: {
      main: "https://www.example.com/transformer_architecture",
      wikipedia: "https://en.wikipedia.org/wiki/Transformer_architecture"
    }
  },
  {
    id: 19,
    title: "ChatGPT",
    abstract: "ChatGPT, a large language model developed by OpenAI, is released in 2022, showcasing the ability to engage in human-like conversations and complete a wide range of tasks.",
    description: "ChatGPT, a large language model developed by OpenAI, is released in 2022, showcasing the ability to engage in human-like conversations and complete a wide range of tasks.",
    date: "2022-11-30",
    urls: {
      main: "https://www.example.com/chatgpt",
      wikipedia: "https://en.wikipedia.org/wiki/ChatGPT"
    }
  },
  {
    id: 20,
    title: "Multimodal AI and Generative Models",
    abstract: "The development of multimodal AI and generative models like DALL-E, Stable Diffusion, and Claude in the early 2020s enables breakthroughs in image generation, video processing, and multimodal tasks.",
    description: "The development of multimodal AI and generative models like DALL-E, Stable Diffusion, and Claude in the early 2020s enables breakthroughs in image generation, video processing, and multimodal tasks.",
    date: "2022-01-01",
    urls: {
      main: "https://www.example.com/multimodal_ai",
      wikipedia: "https://en.wikipedia.org/wiki/Multimodal_AI"
    }
  },
  {
    id: 21,
    title: "Embodied AI and Robotics",
    abstract: "Embodied AI and robotics research focuses on developing intelligent systems that interact with and learn from the physical world, enabling robots to perform complex tasks and adapt to dynamic environments.",
    description: "Embodied AI and robotics research focuses on developing intelligent systems that interact with and learn from the physical world, enabling robots to perform complex tasks and adapt to dynamic environments.",
    date: "2023-01-01",
    urls: {
      main: "https://www.example.com/embodied_ai",
      wikipedia: "https://en.wikipedia.org/wiki/Embodied_artificial_intelligence"
    }
  }
];
const timelineItems$1 = {
  timelineItems
};
const css$1 = {
  code: ".timeline-container.svelte-dqne7{padding:2rem}.timeline-header.svelte-dqne7{text-align:center;font-weight:bold;font-size:1.5rem;margin-bottom:.5rem}",
  map: `{"version":3,"file":"Timeline.svelte","sources":["Timeline.svelte"],"sourcesContent":["<script>\\n  import { Timeline, TimelineItem, Button } from 'flowbite-svelte';\\n  import { ArrowRightOutline } from 'flowbite-svelte-icons';\\n  import timelineItems from '../data/timelineItems.json'; // Adjust the path as necessary\\n\\n  function searchGoogle(title) {\\n    const query = encodeURIComponent(title);\\n    window.open(\`https://www.google.com/search?q=\${query}\`, '_blank');\\n  }\\n<\/script>\\n\\n<div class=\\"timeline-container\\">\\n\\n  <div class=\\"timeline-header\\">Timeline of Events</div>\\n  <hr class=\\"my-8 border-t border-gray-300 dark:border-gray-700\\" />\\n  <Timeline>\\n    {#each timelineItems.timelineItems as item (item.id)}\\n      <TimelineItem title={item.title} date={item.date}>\\n        <p class=\\"mb-4 text-base font-normal text-gray-500 dark:text-gray-400\\">{item.abstract}</p>\\n        <Button on:click={() => searchGoogle(item.title)} color=\\"black\\" size=\\"small\\">\\n          Learn More <ArrowRightOutline />\\n        </Button>\\n      </TimelineItem>\\n    {/each}\\n  </Timeline>\\n  <hr class=\\"my-8 border-t border-gray-300 dark:border-gray-700\\" />\\n\\n</div>\\n\\n<style>\\n  .timeline-container {\\n    padding: 2rem; /* Equivalent to p-4 in Tailwind CSS */\\n  }\\n  .timeline-header {\\n    text-align: center;\\n    font-weight: bold;\\n    font-size: 1.5rem;\\n    margin-bottom: .5rem; /* Add some spacing below the header */\\n  }\\n</style>\\n"],"names":[],"mappings":"AA8BE,gCAAoB,CAClB,OAAO,CAAE,IACX,CACA,6BAAiB,CACf,UAAU,CAAE,MAAM,CAClB,WAAW,CAAE,IAAI,CACjB,SAAS,CAAE,MAAM,CACjB,aAAa,CAAE,KACjB"}`
};
const Timeline_1 = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  $$result.css.add(css$1);
  return `<div class="timeline-container svelte-dqne7"><div class="timeline-header svelte-dqne7" data-svelte-h="svelte-bd2kcz">Timeline of Events</div> <hr class="my-8 border-t border-gray-300 dark:border-gray-700"> ${validate_component(Timeline, "Timeline").$$render($$result, {}, {}, {
    default: () => {
      return `${each(timelineItems$1.timelineItems, (item) => {
        return `${validate_component(TimelineItem, "TimelineItem").$$render($$result, { title: item.title, date: item.date }, {}, {
          default: () => {
            return `<p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">${escape(item.abstract)}</p> ${validate_component(Button, "Button").$$render($$result, { color: "black", size: "small" }, {}, {
              default: () => {
                return `Learn More ${validate_component(ArrowRightOutline, "ArrowRightOutline").$$render($$result, {}, {}, {})} `;
              }
            })} `;
          }
        })}`;
      })}`;
    }
  })} <hr class="my-8 border-t border-gray-300 dark:border-gray-700"> </div>`;
});
const css = {
  code: ".countdown-header.svelte-11xtfa6{text-align:center;font-weight:bold;margin-bottom:1rem;font-size:3rem}.countdown-container.svelte-11xtfa6{display:flex;flex-direction:row;justify-content:space-between;align-items:center;gap:0.5rem;height:auto;padding:1rem;white-space:nowrap;max-width:100vw;box-sizing:border-box;overflow:hidden}.countdown-item.svelte-11xtfa6{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0.2rem;color:#000000;border-radius:4px;flex:1;min-width:0}.countdown-value.svelte-11xtfa6{font-family:'Courier New', Courier, monospace;font-size:5vw;font-weight:bold;text-align:center;min-width:5vw}.countdown-label.svelte-11xtfa6{font-size:2vw;text-transform:uppercase;text-align:center}.loading-container.svelte-11xtfa6{display:flex;align-items:center;justify-content:center;font-size:1.2rem;width:100%;height:100%}.loading-icon.svelte-11xtfa6{animation:svelte-11xtfa6-pulse 1s infinite;margin-right:0.5rem}@keyframes svelte-11xtfa6-pulse{0%{opacity:0.2}50%{opacity:1}100%{opacity:0.2}}@media(max-width: 600px){.countdown-value.svelte-11xtfa6{font-size:7vw;min-width:7vw}.countdown-label.svelte-11xtfa6{font-size:3vw}}@media(max-width: 400px){.countdown-value.svelte-11xtfa6{font-size:8vw;min-width:8vw}.countdown-label.svelte-11xtfa6{font-size:4vw}}",
  map: `{"version":3,"file":"Countdown.svelte","sources":["Countdown.svelte"],"sourcesContent":["<script>\\n  import { onDestroy } from 'svelte';\\n  import { fade } from 'svelte/transition';\\n  export let targetDate;\\n\\n  let isLoading = true;\\n  let currentYears = 0;\\n  let currentDays = 0;\\n  let currentHours = 0;\\n  let currentMinutes = 0;\\n  let currentSeconds = 0;\\n  let years = 0;\\n  let days = 0;\\n  let hours = 0;\\n  let minutes = 0;\\n  let seconds = 0;\\n  let countdownInterval;\\n\\n  function startCountdown() {\\n    countdownInterval = setInterval(() => {\\n      updateCountdown();\\n      isLoading = false; // Set isLoading to false after the first update\\n    }, 1000);\\n  }\\n\\n  function updateCountdown() {\\n    if (!targetDate || isNaN(targetDate)) {\\n      clearInterval(countdownInterval);\\n      years = 0;\\n      days = 0;\\n      hours = 0;\\n      minutes = 0;\\n      seconds = 0;\\n      console.error('Invalid targetDate provided to Countdown component');\\n      return;\\n    }\\n\\n    const currentTime = new Date().getTime();\\n    const difference = targetDate - currentTime;\\n\\n    if (difference <= 0) {\\n      clearInterval(countdownInterval);\\n      years = 0;\\n      days = 0;\\n      hours = 0;\\n      minutes = 0;\\n      seconds = 0;\\n      return;\\n    }\\n\\n    const totalDays = Math.floor(difference / (1000 * 60 * 60 * 24));\\n    years = Math.floor(totalDays / 365);\\n    days = totalDays % 365;\\n    hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));\\n    minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));\\n    seconds = Math.floor((difference % (1000 * 60)) / 1000);\\n\\n    // Update the current values\\n    currentYears = years;\\n    currentDays = days;\\n    currentHours = hours;\\n    currentMinutes = minutes;\\n    currentSeconds = seconds;\\n  }\\n\\n  onDestroy(() => {\\n    clearInterval(countdownInterval);\\n  });\\n\\n  startCountdown();\\n<\/script>\\n\\n<div class=\\"countdown-header\\">\\n  Time Left Until the Singularity\\n</div>\\n\\n{#if isLoading}\\n  <div class=\\"loading-container\\">\\n    <span class=\\"loading-icon\\">&#9679;</span> Loading...\\n  </div>\\n{:else}\\n  <div in:fade={{ duration: 500 }} out:fade={{ duration: 300 }} class=\\"countdown-container\\">\\n    <div class=\\"countdown-item\\">\\n      <span class=\\"countdown-value\\">{currentYears}</span>\\n      <span class=\\"countdown-label\\">years</span>\\n    </div>\\n    <div class=\\"countdown-item\\">\\n      <span class=\\"countdown-value\\">{currentDays}</span>\\n      <span class=\\"countdown-label\\">days</span>\\n    </div>\\n    <div class=\\"countdown-item\\">\\n      <span class=\\"countdown-value\\">{currentHours}</span>\\n      <span class=\\"countdown-label\\">hours</span>\\n    </div>\\n    <div class=\\"countdown-item\\">\\n      <span class=\\"countdown-value\\">{currentMinutes}</span>\\n      <span class=\\"countdown-label\\">min</span>\\n    </div>\\n    <div class=\\"countdown-item\\">\\n      <span class=\\"countdown-value\\">{currentSeconds}</span>\\n      <span class=\\"countdown-label\\">sec</span>\\n    </div>\\n  </div>\\n{/if}\\n\\n<style>\\n  .countdown-header {\\n    text-align: center;\\n    font-weight: bold;\\n    margin-bottom: 1rem;\\n    font-size: 3rem;\\n  }\\n\\n  .countdown-container {\\n    display: flex;\\n    flex-direction: row;\\n    justify-content: space-between;\\n    align-items: center;\\n    gap: 0.5rem;\\n    height: auto;\\n    padding: 1rem;\\n    white-space: nowrap;\\n    max-width: 100vw;\\n    box-sizing: border-box;\\n    overflow: hidden;\\n  }\\n\\n  .countdown-item {\\n    display: flex;\\n    flex-direction: column;\\n    align-items: center;\\n    justify-content: center;\\n    padding: 0.2rem;\\n    color: #000000;\\n    border-radius: 4px;\\n    flex: 1; /* Ensure items are evenly spaced */\\n    min-width: 0; /* Prevent flex items from overflowing */\\n  }\\n\\n  .countdown-value {\\n    font-family: 'Courier New', Courier, monospace;\\n    font-size: 5vw;\\n    font-weight: bold;\\n    text-align: center;\\n    min-width: 5vw; /* Ensure consistent width to prevent shifting */\\n  }\\n\\n  .countdown-label {\\n    font-size: 2vw;\\n    text-transform: uppercase;\\n    text-align: center;\\n  }\\n\\n  .loading-container {\\n    display: flex;\\n    align-items: center;\\n    justify-content: center;\\n    font-size: 1.2rem;\\n    width: 100%; /* Ensure the loading container takes full width */\\n    height: 100%; /* Ensure the loading container takes full height */\\n  }\\n\\n  .loading-icon {\\n    animation: pulse 1s infinite;\\n    margin-right: 0.5rem;\\n  }\\n\\n  @keyframes pulse {\\n    0% {\\n      opacity: 0.2;\\n    }\\n    50% {\\n      opacity: 1;\\n    }\\n    100% {\\n      opacity: 0.2;\\n    }\\n  }\\n\\n  /* Media queries for responsive design */\\n  @media (max-width: 600px) {\\n    .countdown-value {\\n      font-size: 7vw;\\n      min-width: 7vw;\\n    }\\n\\n    .countdown-label {\\n      font-size: 3vw;\\n    }\\n  }\\n\\n  @media (max-width: 400px) {\\n    .countdown-value {\\n      font-size: 8vw;\\n      min-width: 8vw;\\n    }\\n\\n    .countdown-label {\\n      font-size: 4vw;\\n    }\\n  }\\n</style>\\n"],"names":[],"mappings":"AA0GE,gCAAkB,CAChB,UAAU,CAAE,MAAM,CAClB,WAAW,CAAE,IAAI,CACjB,aAAa,CAAE,IAAI,CACnB,SAAS,CAAE,IACb,CAEA,mCAAqB,CACnB,OAAO,CAAE,IAAI,CACb,cAAc,CAAE,GAAG,CACnB,eAAe,CAAE,aAAa,CAC9B,WAAW,CAAE,MAAM,CACnB,GAAG,CAAE,MAAM,CACX,MAAM,CAAE,IAAI,CACZ,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,SAAS,CAAE,KAAK,CAChB,UAAU,CAAE,UAAU,CACtB,QAAQ,CAAE,MACZ,CAEA,8BAAgB,CACd,OAAO,CAAE,IAAI,CACb,cAAc,CAAE,MAAM,CACtB,WAAW,CAAE,MAAM,CACnB,eAAe,CAAE,MAAM,CACvB,OAAO,CAAE,MAAM,CACf,KAAK,CAAE,OAAO,CACd,aAAa,CAAE,GAAG,CAClB,IAAI,CAAE,CAAC,CACP,SAAS,CAAE,CACb,CAEA,+BAAiB,CACf,WAAW,CAAE,aAAa,CAAC,CAAC,OAAO,CAAC,CAAC,SAAS,CAC9C,SAAS,CAAE,GAAG,CACd,WAAW,CAAE,IAAI,CACjB,UAAU,CAAE,MAAM,CAClB,SAAS,CAAE,GACb,CAEA,+BAAiB,CACf,SAAS,CAAE,GAAG,CACd,cAAc,CAAE,SAAS,CACzB,UAAU,CAAE,MACd,CAEA,iCAAmB,CACjB,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,eAAe,CAAE,MAAM,CACvB,SAAS,CAAE,MAAM,CACjB,KAAK,CAAE,IAAI,CACX,MAAM,CAAE,IACV,CAEA,4BAAc,CACZ,SAAS,CAAE,oBAAK,CAAC,EAAE,CAAC,QAAQ,CAC5B,YAAY,CAAE,MAChB,CAEA,WAAW,oBAAM,CACf,EAAG,CACD,OAAO,CAAE,GACX,CACA,GAAI,CACF,OAAO,CAAE,CACX,CACA,IAAK,CACH,OAAO,CAAE,GACX,CACF,CAGA,MAAO,YAAY,KAAK,CAAE,CACxB,+BAAiB,CACf,SAAS,CAAE,GAAG,CACd,SAAS,CAAE,GACb,CAEA,+BAAiB,CACf,SAAS,CAAE,GACb,CACF,CAEA,MAAO,YAAY,KAAK,CAAE,CACxB,+BAAiB,CACf,SAAS,CAAE,GAAG,CACd,SAAS,CAAE,GACb,CAEA,+BAAiB,CACf,SAAS,CAAE,GACb,CACF"}`
};
const Countdown = create_ssr_component(($$result, $$props, $$bindings, slots) => {
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
        isLoading = false;
      },
      1e3
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
      console.error("Invalid targetDate provided to Countdown component");
      return;
    }
    const currentTime = (/* @__PURE__ */ new Date()).getTime();
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
    const totalDays = Math.floor(difference / (1e3 * 60 * 60 * 24));
    years = Math.floor(totalDays / 365);
    days = totalDays % 365;
    hours = Math.floor(difference % (1e3 * 60 * 60 * 24) / (1e3 * 60 * 60));
    minutes = Math.floor(difference % (1e3 * 60 * 60) / (1e3 * 60));
    seconds = Math.floor(difference % (1e3 * 60) / 1e3);
    currentYears = years;
    currentDays = days;
    currentHours = hours;
    currentMinutes = minutes;
    currentSeconds = seconds;
  }
  onDestroy(() => {
    clearInterval(countdownInterval);
  });
  startCountdown();
  if ($$props.targetDate === void 0 && $$bindings.targetDate && targetDate !== void 0)
    $$bindings.targetDate(targetDate);
  $$result.css.add(css);
  return `<div class="countdown-header svelte-11xtfa6" data-svelte-h="svelte-1ext6vo">Time Left Until the Singularity</div> ${isLoading ? `<div class="loading-container svelte-11xtfa6" data-svelte-h="svelte-wa8i6g"><span class="loading-icon svelte-11xtfa6">●</span> Loading...</div>` : `<div class="countdown-container svelte-11xtfa6"><div class="countdown-item svelte-11xtfa6"><span class="countdown-value svelte-11xtfa6">${escape(currentYears)}</span> <span class="countdown-label svelte-11xtfa6" data-svelte-h="svelte-eirkcv">years</span></div> <div class="countdown-item svelte-11xtfa6"><span class="countdown-value svelte-11xtfa6">${escape(currentDays)}</span> <span class="countdown-label svelte-11xtfa6" data-svelte-h="svelte-1t00k4q">days</span></div> <div class="countdown-item svelte-11xtfa6"><span class="countdown-value svelte-11xtfa6">${escape(currentHours)}</span> <span class="countdown-label svelte-11xtfa6" data-svelte-h="svelte-1n22zb0">hours</span></div> <div class="countdown-item svelte-11xtfa6"><span class="countdown-value svelte-11xtfa6">${escape(currentMinutes)}</span> <span class="countdown-label svelte-11xtfa6" data-svelte-h="svelte-1cr9shd">min</span></div> <div class="countdown-item svelte-11xtfa6"><span class="countdown-value svelte-11xtfa6">${escape(currentSeconds)}</span> <span class="countdown-label svelte-11xtfa6" data-svelte-h="svelte-vgwnla">sec</span></div></div>`}`;
});
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  const targetDate = (/* @__PURE__ */ new Date("2027-11-20T23:59:59")).getTime();
  return `${validate_component(Navbar_1, "Navbar").$$render($$result, {}, {}, {})}  ${validate_component(Countdown, "Countdown").$$render($$result, { targetDate }, {}, {})}  ${validate_component(Timeline_1, "Timeline").$$render($$result, { items: timelineItems$1.timelineItems }, {}, {})} ${validate_component(MailchimpSignup, "MailchimpSignup").$$render($$result, {}, {}, {})} ${validate_component(Spacer, "Spacer").$$render($$result, { height: "6rem" }, {}, {})} ${validate_component(BottomNav_1, "BottomNav").$$render($$result, {}, {}, {})}`;
});

export { Page as default };
//# sourceMappingURL=_page.svelte-Z9yis1p2.js.map
