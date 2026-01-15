import React from 'react';
import type { FATProcedure } from '../types';
import { CheckCircle2, AlertTriangle, FileDown } from 'lucide-react';

interface ProcedureViewProps {
    data: FATProcedure;
    onDownload: () => void;
    isDownloading: boolean;
}

/**
 * Procedure Viewer Component
 * --------------------------
 * Displays the generated FAT steps and provides the download action.
 */
export const ProcedureView: React.FC<ProcedureViewProps> = ({ data, onDownload, isDownloading }) => {
    return (
        <div className="bg-white rounded-lg shadow overflow-hidden border border-gray-200">
            {/* Header Section */}
            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <div>
                    <h2 className="text-lg font-bold text-gray-900">2. Generated Procedure</h2>
                    <p className="text-sm text-gray-500">
                        {data.device_model} | {data.project_name}
                    </p>
                </div>
                <button
                    onClick={onDownload}
                    disabled={isDownloading}
                    className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-800 disabled:opacity-50"
                >
                    <FileDown size={18} />
                    {isDownloading ? 'Rendering PDF...' : 'Download PDF'}
                </button>
            </div>

            {/* Steps List */}
            <div className="divide-y divide-gray-100">
                {data.steps.map((step) => (
                    <div key={step.step_id} className="p-6 hover:bg-gray-50 transition-colors group">
                        <div className="flex items-start gap-4">
                            {/* Step ID */}
                            <div className="flex-shrink-0 w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center font-bold text-gray-600">
                                {step.step_id}
                            </div>

                            {/* Content */}
                            <div className="flex-grow">
                                <div className="flex items-center gap-2 mb-1">
                                    <h3 className="font-medium text-gray-900">{step.instruction}</h3>
                                    {step.safety_critical && (
                                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-bold bg-red-100 text-red-700">
                                            <AlertTriangle size={12} />
                                            SAFETY
                                        </span>
                                    )}
                                </div>
                                <div className="flex items-center gap-2 text-sm text-gray-600 bg-blue-50/50 p-2 rounded border border-blue-100/50">
                                    <CheckCircle2 size={14} className="text-blue-500" />
                                    <span>Expect: {step.expected_result}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};