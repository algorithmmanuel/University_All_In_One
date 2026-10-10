import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'EduCyber Nigeria | Learn. Practise. Build. Secure.', description: 'A Nigerian learning platform for secondary, university and cybersecurity learners.' };
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>}
