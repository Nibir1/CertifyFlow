import React from 'react';
import type { ReactNode } from 'react';

interface LayoutProps {
    children: ReactNode;
}

/**
 * Main Application Layout
 * -----------------------
 * Provides the consistent header, footer, and container styling.
 */
export const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        {/* CertifyFlow Blue Branding */}
                        <div className="text-2xl font-bold text-[#003B5C]">
                            CertifyFlow
                        </div>
                        <div className="h-6 w-px bg-gray-300 mx-2"></div>
                    </div>
                </div>
            </header>

            {/* Main Content Area */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {children}
            </main>
        </div>
    );
};