import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'EduCyber Nigeria | Learn. Practise. Build. Secure.', description: 'A cybersecurity-only learning and simulation platform for secondary students, university learners and professionals.' };
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>}
