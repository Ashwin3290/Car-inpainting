/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
  },
  compiler: {
    removeConsole: false,
  },
  transpilePackages: ['react-icons'],
};

module.exports = nextConfig;
