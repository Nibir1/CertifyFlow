import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { InputForm } from './components/InputForm';
import { ProcedureView } from './components/ProcedureView';
import { api } from './api/endpoints';
import type { FATProcedure } from './types';
import { Loader2, AlertCircle } from 'lucide-react';

function App() {
  // State to hold the generated procedure
  const [procedure, setProcedure] = useState<FATProcedure | null>(null);

  // Mutation 1: Generate Procedure (Text -> JSON)
  const generateMutation = useMutation({
    mutationFn: (text: string) => api.generateProcedure({ raw_text: text }),
    onSuccess: (data) => {
      setProcedure(data);
    },
    onError: (error) => {
      console.error('Generation failed:', error);
    }
  });

  // Mutation 2: Download PDF (JSON -> PDF Blob)
  const pdfMutation = useMutation({
    mutationFn: (data: FATProcedure) => api.generatePDF(data),
    onSuccess: (blob) => {
      // standard browser trick to trigger a file download from a Blob
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      // Naming convention: FAT_DeviceModel.pdf
      link.setAttribute('download', `FAT_${procedure?.device_model || 'Procedure'}.pdf`);
      document.body.appendChild(link);
      link.click();
      // Cleanup
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    onError: (error) => {
      console.error('PDF Generation failed:', error);
    }
  });

  return (
    <Layout>
      <div className="space-y-8">

        {/* Section 1: Input */}
        <InputForm
          onGenerate={(text) => generateMutation.mutate(text)}
          isLoading={generateMutation.isPending}
        />

        {/* Error State */}
        {generateMutation.isError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded flex items-center gap-2">
            <AlertCircle size={20} />
            <span>
              <b>Generation Failed:</b> Check the backend logs. Ensure your OpenAI Key is valid.
            </span>
          </div>
        )}

        {/* Loading State (Skeleton or Spinner) */}
        {generateMutation.isPending && (
          <div className="flex flex-col items-center justify-center py-12 text-gray-500 animate-pulse">
            <Loader2 size={48} className="animate-spin text-[#003B5C] mb-4" />
            <p className="font-medium">AI is analyzing specification...</p>
            <p className="text-sm">Mapping requirements to ISO standards</p>
          </div>
        )}

        {/* Section 2: Results View (Only shown after success) */}
        {procedure && !generateMutation.isPending && (
          <ProcedureView
            data={procedure}
            onDownload={() => pdfMutation.mutate(procedure)}
            isDownloading={pdfMutation.isPending}
          />
        )}

      </div>
    </Layout>
  );
}

export default App;