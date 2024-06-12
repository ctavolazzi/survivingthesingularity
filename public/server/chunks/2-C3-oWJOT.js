import { s as supabase } from './supabaseClient-DNeOHnRL.js';
import '@supabase/supabase-js';

async function load() {
  const { data } = await supabase.from("countries").select();
  return {
    countries: data ?? []
  };
}

var _page_server = /*#__PURE__*/Object.freeze({
  __proto__: null,
  load: load
});

const index = 2;
let component_cache;
const component = async () => component_cache ??= (await import('./_page.svelte-Z9yis1p2.js')).default;
const server_id = "src/routes/+page.server.js";
const imports = ["_app/immutable/nodes/2.Dic8j5Dy.js","_app/immutable/chunks/scheduler.DB5l2x1O.js","_app/immutable/chunks/index.BzcHPuj_.js","_app/immutable/chunks/Spacer.GsLtfyTS.js","_app/immutable/chunks/index.igSbMWXI.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/MailchimpSignup.Djd6m_mW.js"];
const stylesheets = ["_app/immutable/assets/2.BqTc6xi6.css","_app/immutable/assets/Spacer.D0l6HJPT.css"];
const fonts = [];

export { component, fonts, imports, index, _page_server as server, server_id, stylesheets };
//# sourceMappingURL=2-C3-oWJOT.js.map
