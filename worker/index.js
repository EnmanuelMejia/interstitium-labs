/**
 * Apex is canonical. www is a second copy unless this redirects.
 * Everything else is the static Learning OS in docs/.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.interstitiumlabs.dev") {
      url.hostname = "interstitiumlabs.dev";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
