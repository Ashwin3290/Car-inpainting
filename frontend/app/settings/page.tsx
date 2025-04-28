export default function SettingsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="main-header">Settings</h1>
      <p className="text-center text-lg text-gray-700 mb-8">
        Configure your workspace preferences
      </p>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Application Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="flex items-center">
                <input 
                  type="checkbox" 
                  className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <span className="ml-2">Dark Mode</span>
              </label>
            </div>
            
            <div>
              <label className="flex items-center">
                <input 
                  type="checkbox" 
                  className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                  defaultChecked
                />
                <span className="ml-2">Auto-save Results</span>
              </label>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max History Items
              </label>
              <select className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50">
                <option value="5">5</option>
                <option value="10" selected>10</option>
                <option value="20">20</option>
                <option value="50">50</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Default Color Mode
              </label>
              <select className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50">
                <option value="preset" selected>Preset Colors</option>
                <option value="custom">Custom Color</option>
                <option value="palette">Color Palette</option>
              </select>
            </div>
          </div>
        </div>
        
        <div>
          <h2 className="text-xl font-semibold mb-4">Storage</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Export Directory
              </label>
              <input 
                type="text" 
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50"
                value="./exports"
              />
            </div>
            
            <div>
              <button className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors">
                Clear History
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
