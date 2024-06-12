import { c as create_ssr_component, v as validate_component } from './ssr-DH4u9ZHx.js';
import { N as Navbar_1, S as Spacer, B as BottomNav_1 } from './Spacer-fKOGNVLp.js';
import './index-mAg2Gvoi.js';
import './supabaseClient-DNeOHnRL.js';
import '@supabase/supabase-js';

const css = {
  code: ".container.svelte-zmsnzz{max-width:1200px;margin:0 auto;padding:2rem;color:#333}.form-wrapper.svelte-zmsnzz{background-color:#fff;border-radius:8px;box-shadow:0 2px 8px rgba(0, 0, 0, 0.1);padding:2rem}.form-title.svelte-zmsnzz{text-align:center;margin-bottom:2rem}",
  map: `{"version":3,"file":"+page.svelte","sources":["+page.svelte"],"sourcesContent":["<script>\\n  import Navbar from '../../components/Navbar.svelte';\\n  import BottomNav from '../../components/BottomNav.svelte';\\n  import Spacer from '../../components/Spacer.svelte'; // Import Spacer component\\n<\/script>\\n\\n<Navbar />\\n\\n<div class=\\"container mx-auto p-4\\">\\n  <div class=\\"form-wrapper max-w-lg mx-auto bg-white p-8 rounded-lg shadow-md\\">\\n    <h1 class=\\"form-title text-2xl font-semibold mb-6 text-center\\">Get in touch:</h1>\\n    <p class=\\"text-center\\">Please use the Mailchimp form below to get in touch with us.</p>\\n    <iframe src=\\"https://us19.list-manage.com/contact-form?u=79a060ac083c62360805246c1&form_id=c4630b003308d7c72c1d0479c30c9a64\\" width=\\"100%\\" height=\\"600px\\" frameborder=\\"0\\" style=\\"border:0; overflow:hidden;\\" title=\\"Mailchimp contact form\\"></iframe>\\n  </div>\\n</div>\\n\\n<!-- Spacer for bottom navigation -->\\n<Spacer height=\\"6rem\\" />\\n\\n<BottomNav />\\n\\n<style>\\n  .container {\\n    max-width: 1200px;\\n    margin: 0 auto;\\n    padding: 2rem;\\n    color: #333;\\n  }\\n\\n  .form-wrapper {\\n    background-color: #fff;\\n    border-radius: 8px;\\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);\\n    padding: 2rem;\\n  }\\n\\n  .form-title {\\n    text-align: center;\\n    margin-bottom: 2rem;\\n  }\\n</style>\\n"],"names":[],"mappings":"AAsBE,wBAAW,CACT,SAAS,CAAE,MAAM,CACjB,MAAM,CAAE,CAAC,CAAC,IAAI,CACd,OAAO,CAAE,IAAI,CACb,KAAK,CAAE,IACT,CAEA,2BAAc,CACZ,gBAAgB,CAAE,IAAI,CACtB,aAAa,CAAE,GAAG,CAClB,UAAU,CAAE,CAAC,CAAC,GAAG,CAAC,GAAG,CAAC,KAAK,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,CAAC,GAAG,CAAC,CACxC,OAAO,CAAE,IACX,CAEA,yBAAY,CACV,UAAU,CAAE,MAAM,CAClB,aAAa,CAAE,IACjB"}`
};
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  $$result.css.add(css);
  return `${validate_component(Navbar_1, "Navbar").$$render($$result, {}, {}, {})} <div class="container mx-auto p-4 svelte-zmsnzz" data-svelte-h="svelte-nuxit3"><div class="form-wrapper max-w-lg mx-auto bg-white p-8 rounded-lg shadow-md svelte-zmsnzz"><h1 class="form-title text-2xl font-semibold mb-6 text-center svelte-zmsnzz">Get in touch:</h1> <p class="text-center">Please use the Mailchimp form below to get in touch with us.</p> <iframe src="https://us19.list-manage.com/contact-form?u=79a060ac083c62360805246c1&form_id=c4630b003308d7c72c1d0479c30c9a64" width="100%" height="600px" frameborder="0" style="border:0; overflow:hidden;" title="Mailchimp contact form"></iframe></div></div>  ${validate_component(Spacer, "Spacer").$$render($$result, { height: "6rem" }, {}, {})} ${validate_component(BottomNav_1, "BottomNav").$$render($$result, {}, {}, {})}`;
});

export { Page as default };
//# sourceMappingURL=_page.svelte-BAelJKzz.js.map
