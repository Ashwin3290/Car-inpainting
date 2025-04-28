import Link from 'next/link';
import Image from 'next/image';
import { FeatureCard } from '@/components/ui/FeatureCard';

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="main-header">Car Color Studio</h1>
      
      <div className="mt-8 mb-12 text-center">
        <p className="text-xl text-gray-700 max-w-3xl mx-auto">
          A professional-grade application for virtually recoloring car images with AI-powered precision.
        </p>
        <Link href="/studio" className="btn-primary inline-block mt-6">
          Start Recoloring
        </Link>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
        <FeatureCard 
          title="Smart Color Transform" 
          description="Advanced AI-powered car recoloring with intelligent mask generation"
          icon="palette"
        />
        <FeatureCard 
          title="Real-time Preview" 
          description="See changes instantly with our advanced preview system"
          icon="eye"
        />
        <FeatureCard 
          title="Professional Results" 
          description="High-quality output suitable for professional use"
          icon="check-circle"
        />
      </div>
      
      <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
        <h2 className="text-2xl font-semibold mb-4 text-center">How It Works</h2>
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex-1 text-center">
            <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-white text-xl font-bold mx-auto mb-4">1</div>
            <h3 className="font-semibold mb-2">Upload Your Car</h3>
            <p className="text-gray-600">Upload any image of a car to get started</p>
          </div>
          <div className="flex-1 text-center">
            <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-white text-xl font-bold mx-auto mb-4">2</div>
            <h3 className="font-semibold mb-2">Choose a Color</h3>
            <p className="text-gray-600">Select from presets or create your own custom color</p>
          </div>
          <div className="flex-1 text-center">
            <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-white text-xl font-bold mx-auto mb-4">3</div>
            <h3 className="font-semibold mb-2">Transform</h3>
            <p className="text-gray-600">AI intelligently recolors your car while preserving details</p>
          </div>
        </div>
      </div>
      
      <div className="text-center mb-12">
        <h2 className="text-2xl font-semibold mb-8">Ready to transform your car?</h2>
        <Link href="/studio" className="btn-primary">
          Get Started Now
        </Link>
      </div>
    </div>
  );
}
