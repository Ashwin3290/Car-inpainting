'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadIcon, LoaderIcon } from '@/components/ui/Icons';
import { useImageUpload, useMaskGeneration, useCarAnalysis } from '@/lib/api/mutations';

interface ImageUploaderProps {
  onImageUploaded: (uuid: string, imageUrl: string) => void;
}

export function ImageUploader({ onImageUploaded }: ImageUploaderProps) {
  const [isProcessing, setIsProcessing] = useState(false);
  
  const uploadMutation = useImageUpload();
  const maskMutation = useMaskGeneration();
  const analysisMutation = useCarAnalysis();
  
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    setIsProcessing(true);
    
    try {
      // Upload the image
      const uploadResult = await uploadMutation.mutateAsync(file);
      
      if (uploadResult.success) {
        const imageUuid = uploadResult.uuid;
        const imageUrl = URL.createObjectURL(file);
        
        // Generate mask
        await maskMutation.mutateAsync(imageUuid);
        
        // Analyze car
        await analysisMutation.mutateAsync(imageUuid);
        
        // Notify parent component
        onImageUploaded(imageUuid, imageUrl);
      }
    } catch (error) {
      console.error('Error processing image:', error);
    } finally {
      setIsProcessing(false);
    }
  }, [uploadMutation, maskMutation, analysisMutation, onImageUploaded]);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
    maxFiles: 1,
    disabled: isProcessing,
  });

  return (
    <div 
      {...getRootProps()} 
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
        isDragActive ? 'border-primary bg-primary-50' : 'border-gray-300 hover:border-primary'
      }`}
    >
      <input {...getInputProps()} />
      
      {isProcessing ? (
        <div className="flex flex-col items-center justify-center py-4">
          <LoaderIcon className="h-12 w-12 text-primary animate-spin mb-4" />
          <p className="text-gray-600">Processing image...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-4">
          <UploadIcon className="h-12 w-12 text-gray-400 mb-4" />
          <p className="text-gray-600">
            {isDragActive
              ? "Drop the image here"
              : "Drag & drop a car image here, or click to select"}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Supported formats: JPG, JPEG, PNG
          </p>
        </div>
      )}
    </div>
  );
}
