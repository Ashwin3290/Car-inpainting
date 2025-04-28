'use client';

import { useState } from 'react';
import { useHistory } from '@/lib/api/queries';
import { useDeleteHistoryEntry } from '@/lib/api/mutations';
import { TrashIcon, DownloadIcon, LoaderIcon } from '@/components/ui/Icons';
import Image from 'next/image';

export default function HistoryPage() {
  const [expandedEntry, setExpandedEntry] = useState<string | null>(null);
  
  const historyQuery = useHistory();
  const deleteEntryMutation = useDeleteHistoryEntry();
  
  if (historyQuery.isLoading) {
    return (
      <div className="container mx-auto px-4 py-12 flex items-center justify-center">
        <LoaderIcon className="h-8 w-8 text-primary animate-spin mr-2" />
        <p>Loading history...</p>
      </div>
    );
  }
  
  if (historyQuery.isError) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="bg-red-50 p-4 rounded-md text-red-700">
          Error loading history. Please try again.
        </div>
      </div>
    );
  }
  
  const historyEntries = historyQuery.data || [];
  
  if (historyEntries.length === 0) {
    return (
      <div className="container mx-auto px-4 py-12">
        <h1 className="main-header">Processing History</h1>
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <p className="text-gray-500 text-lg">
            No processing history available yet.
            <br />
            Try recoloring some cars first!
          </p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="main-header">Processing History</h1>
      <p className="text-center text-lg text-gray-700 mb-8">
        View and compare your previous transformations
      </p>
      
      <div className="space-y-6">
        {historyEntries.map((entry: any) => (
          <div key={entry.uuid} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div 
              className="p-4 cursor-pointer hover:bg-gray-50 transition-colors flex items-center justify-between"
              onClick={() => setExpandedEntry(expandedEntry === entry.uuid ? null : entry.uuid)}
            >
              <div>
                <p className="font-medium">{new Date(entry.timestamp).toLocaleString()}</p>
                <p className="text-sm text-gray-500">
                  Color: {Array.isArray(entry.color) 
                    ? `RGB(${entry.color.join(', ')})`
                    : entry.color}
                </p>
              </div>
              <div className="flex gap-2">
                <button 
                  className="p-2 rounded-full hover:bg-red-50 text-red-500 transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm('Are you sure you want to delete this history entry?')) {
                      deleteEntryMutation.mutate(entry.uuid);
                    }
                  }}
                >
                  <TrashIcon />
                </button>
                <a 
                  href={`${process.env.NEXT_PUBLIC_API_URL}/api/recolored/${entry.uuid}`}
                  download={`recolored-car-${entry.uuid}.jpg`}
                  className="p-2 rounded-full hover:bg-primary-50 text-primary transition-colors"
                  onClick={(e) => e.stopPropagation()}
                >
                  <DownloadIcon />
                </a>
              </div>
            </div>
            
            {expandedEntry === entry.uuid && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 border-t">
                <div>
                  <p className="font-medium mb-2">Original</p>
                  <div className="relative aspect-video rounded overflow-hidden bg-gray-100">
                    <Image 
                      src={entry.original_image} 
                      alt="Original car"
                      fill
                      className="object-contain"
                    />
                  </div>
                </div>
                <div>
                  <p className="font-medium mb-2">Recolored</p>
                  <div className="relative aspect-video rounded overflow-hidden bg-gray-100">
                    <Image 
                      src={`${process.env.NEXT_PUBLIC_API_URL}/api/recolored/${entry.uuid}`}
                      alt="Recolored car"
                      fill
                      className="object-contain"
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
