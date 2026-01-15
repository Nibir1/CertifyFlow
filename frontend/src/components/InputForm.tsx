import React, { useState } from 'react';

interface InputFormProps {
    onGenerate: (text: string) => void;
    isLoading: boolean;
}

/**
 * Input Form Component
 * --------------------
 * Captures the raw technical specification from the user.
 */
export const InputForm: React.FC<InputFormProps> = ({ onGenerate, isLoading }) => {
    const [text, setText] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (text.trim()) {
            onGenerate(text);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
                1. Input Technical Specification
            </h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    className="w-full h-48 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm resize-y"
                    placeholder="Paste raw spec here (e.g. 'Vaisala HMP155, Power 24V...')"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    disabled={isLoading}
                />
                <div className="mt-4 flex justify-end">
                    <button
                        type="submit"
                        disabled={!text.trim() || isLoading}
                        className={`px-6 py-2 rounded-md text-white font-medium transition-colors ${isLoading
                                ? 'bg-gray-400 cursor-not-allowed'
                                : 'bg-[#003B5C] hover:bg-[#002840]'
                            }`}
                    >
                        {isLoading ? 'Generating Procedure...' : 'Generate Test Steps'}
                    </button>
                </div>
            </form>
        </div>
    );
};