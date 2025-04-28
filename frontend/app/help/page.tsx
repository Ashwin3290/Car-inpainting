export default function HelpPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="main-header">Help & Documentation</h1>
      <p className="text-center text-lg text-gray-700 mb-8">
        Learn how to use Car Color Studio
      </p>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Quick Start Guide</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary mb-4">1</div>
              <h3 className="font-semibold mb-2">Upload Your Image</h3>
              <p className="text-gray-600">
                Click the upload button or drag and drop your image into the upload area.
                Supported formats: JPG, JPEG, PNG
              </p>
            </div>
            
            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary mb-4">2</div>
              <h3 className="font-semibold mb-2">Choose Your Color</h3>
              <p className="text-gray-600">
                Select from preset colors, use the color picker for custom colors,
                or try the color palette generator.
              </p>
            </div>
            
            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary mb-4">3</div>
              <h3 className="font-semibold mb-2">Process and Save</h3>
              <p className="text-gray-600">
                Click 'Transform Color' to process your image.
                Download your result and view history anytime.
              </p>
            </div>
          </div>
        </div>
        
        <div>
          <h2 className="text-2xl font-semibold mb-4">Frequently Asked Questions</h2>
          
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-lg">What image formats are supported?</h3>
              <p className="text-gray-600">
                We support JPG, JPEG, and PNG formats. For best results, use high-resolution images with good lighting.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold text-lg">How does the color recoloring work?</h3>
              <p className="text-gray-600">
                Our AI-powered color transformation technology uses advanced computer vision to identify the car in your image,
                create a precise mask, and intelligently recolor it while preserving important details like reflections,
                shadows, and textures.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold text-lg">What are the limitations?</h3>
              <p className="text-gray-600">
                The system works best on images where the car is clearly visible and well-lit.
                Extremely dark cars or images with poor lighting may produce less optimal results.
                The AI automatically detects and preserves non-paintable areas like windows, lights, and grilles.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold text-lg">Can I use the recolored images commercially?</h3>
              <p className="text-gray-600">
                Yes, you own the output images produced by Car Color Studio.
                They can be used for professional presentations, marketing materials, or any other purpose.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold text-lg">How do I contact support?</h3>
              <p className="text-gray-600">
                For technical support or feature requests, please email us at support@carcolorstudio.com
                or visit our website at carcolorstudio.com/support.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
