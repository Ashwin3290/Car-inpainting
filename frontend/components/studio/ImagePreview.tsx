'use client';

import { useState } from 'react';
import Image from 'next/image';

interface ImagePreviewProps {
  imageUrl: string;
  alt: string;
}

export function ImagePreview({ imageUrl, alt }: ImagePreviewProps) {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <div className="relative rounded-lg overflow-hidden bg-gray-50 aspect-video">
      <Image
        src={imageUrl}
        alt={alt}
        className={`object-contain transition-opacity duration-300 ${
          isLoading ? 'opacity-0' : 'opacity-100'
        }`}
        fill
        sizes="(max-width: 768px) 100vw, 50vw"
        onLoadingComplete={() => setIsLoading(false)}
      />
      
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-8 w-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}
    </div>
  );
}
