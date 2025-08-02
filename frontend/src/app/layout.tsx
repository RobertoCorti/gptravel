import type { Metadata } from 'next';
import { Inter, Poppins } from 'next/font/google';
import '../styles/globals.css';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

const poppins = Poppins({ 
  weight: ['400', '500', '600', '700', '800'],
  subsets: ['latin'],
  variable: '--font-poppins',
});

export const metadata: Metadata = {
  title: 'GPTravel ✈️ - AI-Powered Travel Planning',
  description: 'Generate personalized travel itineraries with AI. Plan your perfect trip with GPTravel.',
  keywords: 'travel, AI, travel planning, itinerary, GPT, vacation, trip',
  authors: [
    { name: 'Roberto Corti', url: 'https://github.com/RobertoCorti' },
    { name: 'Stefano Polo', url: 'https://github.com/stefano-polo' }
  ],
  openGraph: {
    title: 'GPTravel ✈️ - AI-Powered Travel Planning',
    description: 'Generate personalized travel itineraries with AI',
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
      <body className="font-sans antialiased bg-gradient-to-br from-blue-50 via-white to-cyan-50">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
} 
