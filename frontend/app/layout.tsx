import './globals.css';
import { Inter } from 'next/font/google';
import Sidebar from '@/components/ui/Sidebar';
import QueryProvider from '@/components/ui/QueryProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Car Color Studio',
  description: 'Professional-grade application for virtually recoloring car images',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          <div className="flex h-screen bg-background">
            <Sidebar />
            <main className="flex-1 overflow-auto">
              {children}
            </main>
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
