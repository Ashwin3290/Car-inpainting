'use client';

import { useState, useCallback, useEffect } from 'react';
import { HexColorPicker } from 'react-colorful';
import { hexToRgb, rgbToHex } from '@/lib/utils';

interface ColorSelectorProps {
  onColorSelected: (color: [number, number, number]) => void;
}

const COLOR_PRESETS = {
  "Midnight Black": "#000000",
  "Arctic White": "#FFFFFF",
  "Racing Red": "#FF0000",
  "Ocean Blue": "#0000FF",
  "Forest Green": "#008000",
  "Sunset Orange": "#FFA500",
  "Royal Purple": "#800080",
};

type ColorMode = 'preset' | 'custom' | 'palette';

export function ColorSelector({ onColorSelected }: ColorSelectorProps) {
  const [colorMode, setColorMode] = useState<ColorMode>('preset');
  const [selectedPreset, setSelectedPreset] = useState<string>("Ocean Blue");
  const [customColor, setCustomColor] = useState("#0000FF");
  
  // Update parent component when color changes
  useEffect(() => {
    let colorHex: string;
    
    if (colorMode === 'preset') {
      colorHex = COLOR_PRESETS[selectedPreset as keyof typeof COLOR_PRESETS];
    } else {
      colorHex = customColor;
    }
    
    const rgbColor = hexToRgb(colorHex);
    onColorSelected(rgbColor);
  }, [colorMode, selectedPreset, customColor, onColorSelected]);
  
  const handlePresetChange = useCallback((preset: string) => {
    setSelectedPreset(preset);
  }, []);
  
  const handleCustomColorChange = useCallback((color: string) => {
    setCustomColor(color);
  }, []);
  
  return (
    <div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Color Mode
        </label>
        <div className="flex gap-2">
          <button
            className={`px-3 py-2 rounded-md text-sm ${
              colorMode === 'preset'
                ? 'bg-primary text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
            onClick={() => setColorMode('preset')}
          >
            Preset Colors
          </button>
          <button
            className={`px-3 py-2 rounded-md text-sm ${
              colorMode === 'custom'
                ? 'bg-primary text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
            onClick={() => setColorMode('custom')}
          >
            Custom Color
          </button>
        </div>
      </div>
      
      {colorMode === 'preset' && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Choose a preset color
          </label>
          <div className="grid grid-cols-4 gap-2 mb-4">
            {Object.entries(COLOR_PRESETS).map(([name, hex]) => (
              <div 
                key={name} 
                className={`cursor-pointer p-1 rounded-md ${
                  selectedPreset === name ? 'ring-2 ring-primary' : ''
                }`}
                onClick={() => handlePresetChange(name)}
              >
                <div
                  className="w-full h-8 rounded"
                  style={{ backgroundColor: hex }}
                  title={name}
                />
              </div>
            ))}
          </div>
          <p className="text-sm font-medium">{selectedPreset}</p>
        </div>
      )}
      
      {colorMode === 'custom' && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Choose a custom color
          </label>
          <HexColorPicker color={customColor} onChange={handleCustomColorChange} />
          <div className="flex items-center gap-3 mt-3">
            <div
              className="w-8 h-8 rounded-md"
              style={{ backgroundColor: customColor }}
            />
            <p className="text-sm">{customColor}</p>
          </div>
        </div>
      )}
    </div>
  );
}
