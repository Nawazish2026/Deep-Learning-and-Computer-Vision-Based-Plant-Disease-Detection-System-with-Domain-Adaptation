import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { LanguageProvider } from '@/contexts/LanguageContext'
import Navbar from '@/components/Navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AgriVision - AI Plant Disease Detection',
  description: 'AI-powered plant disease detection system for farmers',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        <LanguageProvider>
          <Navbar />
          <main className="flex-grow">
            {children}
          </main>
          <footer className="bg-gray-900 text-white py-8">
            <div className="container mx-auto px-4 text-center">
              <p className="text-gray-400">
                © 2025 AgriVision | Personal AIML Project
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Developed by <a href="https://github.com/amanbind898" target="_blank" rel="noopener noreferrer" className="text-green-400 hover:text-green-300">Aman Kumar Bind</a>
              </p>
            </div>
          </footer>
        </LanguageProvider>
      </body>
    </html>
  )
}
