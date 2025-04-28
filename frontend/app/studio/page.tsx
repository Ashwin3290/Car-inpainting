
'use client';

import { useCallback, useState } from 'react';
import { ColorSelector } from '@/components/studio/ColorSelector';
import { ImageUploader } from '@/components/studio/ImageUploader';
import { ImagePreview } from '@/components/studio/ImagePreview';
import { TransformButton } from '@/components/studio/TransformButton';
import { useRecolorMutation, useSaveHistory } from '@/lib/api/mutations';

export default function StudioPage() {
  const [imageUuid, setImageUuid] = useState<string | null>(null);
  const [selectedColor, setSelectedColor] = useState<[number, number, number]>([0, 0, 255]); // Default blue
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [recoloredImage, setRecoloredImage] = useState<string | null>(null);
  
  const recolorMutation = useRecolorMutation();
  const saveHistoryMutation = useSaveHistory();
  
  const handleImageUploaded = useCallback((uuid: string, imageUrl: string) => {
    setImageUuid(uuid);
    setOriginalImage(imageUrl);
    setRecoloredImage(null);
  }, []);
  
  const handleColorSelected = useCallback((color: [number, number, number]) => {
    setSelectedColor(color);
  }, []);
  
  const handleTransform = useCallback(() => {
    if (!imageUuid) return;
    
    recolorMutation.mutate(
      { imageUuid, color: selectedColor },
      {
        onSuccess: (data) => {
          if (data.success) {
            // Construct the URL for the recolored image
            const recoloredImageUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/recolored/${imageUuid}`;
            setRecoloredImage(recoloredImageUrl);
            
            // Save to history
            saveHistoryMutation.mutate({
              uuid: imageUuid,
              color: selectedColor,
              original_image: originalImage,
              recolored_image: recoloredImageUrl,
              settings: { preserve_luminance: true } // You can add more settings here if needed
            });
          }
        }
      }
    );
  }, [imageUuid, selectedColor, recolorMutation, originalImage, saveHistoryMutation]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="main-header">Color Studio</h1>
      <p className="text-center text-lg text-gray-700 mb-8">
        Transform your car's appearance with professional-grade recoloring
      </p>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Upload Image</h2>
            <ImageUploader onImageUploaded={handleImageUploaded} />
            
            {originalImage && (
              <div className="mt-6">
                <h3 className="font-medium mb-2">Original Image</h3>
                <ImagePreview imageUrl={originalImage} alt="Original car" />
              </div>
            )}
            
            {recoloredImage && (
              <div className="mt-6">
                <h3 className="font-medium mb-2">Recolored Image</h3>
                <ImagePreview imageUrl={recoloredImage} alt="Recolored car" />
              </div>
            )}
          </div>
        </div>
        
        <div>
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Color Configuration</h2>
            <ColorSelector onColorSelected={handleColorSelected} />
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <TransformButton 
              onClick={handleTransform} 
              disabled={!imageUuid} 
              loading={recolorMutation.isPending} 
            />
            
            {recoloredImage && (
              <a 
                href={recoloredImage} 
                download="recolored-car.jpg"
                className="btn-primary w-full mt-4 text-center"
                target="_blank"
                rel="noopener noreferrer"
              >
                Download
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
