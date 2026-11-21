import type { NextConfig } from "next";

const backendUrl = process.env.BACKEND_API_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    // Same-origin proxy to the API so session cookies work without CORS in dev.
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
