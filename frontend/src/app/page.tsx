'use client';

import { useState } from 'react';
import { Plane, MapPin, Calendar, Users, Sparkles, ArrowRight } from 'lucide-react';
import Button from '@/components/ui/Button';
import TravelForm from '@/components/forms/TravelForm';
import { TravelFormData } from '@/types/travel';

export default function HomePage() {
  const [showForm, setShowForm] = useState(false);

  const handleStartPlanning = () => {
    setShowForm(true);
  };

  const handleFormSubmit = (data: TravelFormData) => {
    console.log('Travel form submitted:', data);
    // TODO: Integrate with your Python backend
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="relative z-10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Plane className="h-8 w-8 text-travel-600" />
            <span className="text-2xl font-display font-bold text-gray-900">GPTravel</span>
          </div>
          <div className="hidden md:flex items-center space-x-6">
            <a href="#features" className="text-gray-600 hover:text-travel-600 transition-colors">Features</a>
            <a href="#about" className="text-gray-600 hover:text-travel-600 transition-colors">About</a>
            <Button variant="secondary" size="sm">
              GitHub
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      {!showForm ? (
        <section className="relative px-6 py-20">
          <div className="max-w-4xl mx-auto text-center">
            {/* Floating Icons */}
            <div className="absolute top-10 left-10 animate-float">
              <div className="bg-travel-100 p-3 rounded-full">
                <MapPin className="h-6 w-6 text-travel-600" />
              </div>
            </div>
            <div className="absolute top-20 right-20 animate-float" style={{ animationDelay: '1s' }}>
              <div className="bg-sunset-100 p-3 rounded-full">
                <Calendar className="h-6 w-6 text-sunset-600" />
              </div>
            </div>
            <div className="absolute bottom-20 left-20 animate-float" style={{ animationDelay: '2s' }}>
              <div className="bg-emerald-100 p-3 rounded-full">
                <Users className="h-6 w-6 text-emerald-600" />
              </div>
            </div>

            {/* Main Content */}
            <div className="animate-fade-in">
              <h1 className="text-5xl md:text-7xl font-display font-bold text-gray-900 mb-6">
                Plan Your Perfect
                <span className="gradient-travel bg-clip-text text-transparent"> Trip</span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
                Powered by AI, GPTravel creates personalized itineraries tailored to your preferences. 
                Discover destinations, activities, and routes that match your travel style.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
                <Button 
                  size="lg" 
                  onClick={handleStartPlanning}
                  className="group"
                >
                  <Sparkles className="mr-2 h-5 w-5" />
                  Start Planning
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
                <Button variant="secondary" size="lg">
                  View Demo
                </Button>
              </div>
            </div>

            {/* Features Grid */}
            <div className="grid md:grid-cols-3 gap-8 mt-20">
              <div className="card animate-slide-up text-center" style={{ animationDelay: '0.2s' }}>
                <div className="bg-travel-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="h-8 w-8 text-travel-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">AI-Powered Planning</h3>
                <p className="text-gray-600">Advanced algorithms create personalized itineraries based on your preferences</p>
              </div>
              
              <div className="card animate-slide-up text-center" style={{ animationDelay: '0.4s' }}>
                <div className="bg-sunset-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MapPin className="h-8 w-8 text-sunset-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Smart Destinations</h3>
                <p className="text-gray-600">Discover hidden gems and popular attractions perfectly matched to your interests</p>
              </div>
              
              <div className="card animate-slide-up text-center" style={{ animationDelay: '0.6s' }}>
                <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Calendar className="h-8 w-8 text-emerald-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Optimized Routes</h3>
                <p className="text-gray-600">Efficient day-by-day schedules that maximize your time and experiences</p>
              </div>
            </div>
          </div>
        </section>
      ) : (
        <section className="px-6 py-10">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-900 mb-4">
                Let's Plan Your Adventure
              </h2>
              <p className="text-lg text-gray-600">
                Fill in your travel details and let AI create the perfect itinerary for you
              </p>
            </div>
            <TravelForm onSubmit={handleFormSubmit} />
          </div>
        </section>
      )}
    </div>
  );
} 
