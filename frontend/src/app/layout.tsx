import type { Metadata } from 'next';
import { Inter, Poppins } from 'next/font/google';
import '../styles/globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-poppins',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'GPTravel - AI-Powered Travel Planning',
  description: 'Create personalized travel itineraries with the power of AI. Discover amazing destinations and activities tailored just for you.',
  keywords: ['travel', 'AI', 'itinerary', 'vacation', 'trip planning', 'OpenAI', 'GPT'],
  authors: [{ name: 'GPTravel Team' }],
  openGraph: {
    title: 'GPTravel - AI-Powered Travel Planning',
    description: 'Create personalized travel itineraries with the power of AI',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
      <body className={`
        font-sans antialiased
        bg-gradient-to-br from-blue-50 via-white to-cyan-50
        text-gray-900
        min-h-screen
      `}>
        {children}
      </body>
    </html>
  );
} 
