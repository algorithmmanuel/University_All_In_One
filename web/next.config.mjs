/** Same-origin API proxy for a single HTTPS ngrok tunnel in private beta. */
import { apiOrigin } from './config/api-origin.mjs';

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
    const origin = apiOrigin();
    return [{source:'/api/v1/:path*',destination:`${origin}/api/v1/:path*`},
            {source:'/health/:path*',destination:`${origin}/health/:path*`}];
  },
};
export default nextConfig;

