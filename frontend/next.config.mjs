/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
            {
                hostname: 'saas-ui.dev'
            }
        ]
    }
};

export default nextConfig;
