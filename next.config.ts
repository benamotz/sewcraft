import type { NextConfig } from "next";

// Every page is pre-rendered (content is read from /content at build time; user state lives in the
// browser), so the app ships as plain static files: `npm run build` writes them to /out.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true, // /projects/apron/ → projects/apron/index.html, served correctly by any static host
};

export default nextConfig;
