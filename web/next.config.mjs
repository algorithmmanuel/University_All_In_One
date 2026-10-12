/** Same-origin API proxy for a single HTTPS ngrok tunnel in private beta. */
const nextConfig = {
  async headers() {
    return [{
      source: '/reset-password',
      headers: [
        {key:'Referrer-Policy', value:'no-referrer'},
        {key:'Cache-Control', value:'no-store'},
        {key:'X-Robots-Tag', value:'noindex, nofollow'},
      ],
    }];
  },
  async rewrites() {
    return [{source:'/api/v1/:path*',destination:'http://127.0.0.1:8000/api/v1/:path*'},
            {source:'/health/:path*',destination:'http://127.0.0.1:8000/health/:path*'}];
  },
};
export default nextConfig;
