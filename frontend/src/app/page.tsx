'use client';

import { useState } from 'react';
import { Plane, Map, Sparkles, Github, ExternalLink, Users, Heart, Briefcase } from 'lucide-react';
import Button from '@/components/ui/Button';
import TravelForm from '@/components/forms/TravelForm';

const floatingIcons = [
  { Icon: Plane, delay: '0s', position: 'top-20 left-20' },
  { Icon: Map, delay: '1s', position: 'top-32 right-32' },
  { Icon: Heart, delay: '2s', position: 'bottom-32 left-16' },
  { Icon: Briefcase, delay: '0.5s', position: 'bottom-20 right-20' },
  { Icon: Users, delay: '1.5s', position: 'top-1/2 left-8' },
];

export default function HomePage() {
  const [showForm, setShowForm] = useState(false);

  if (showForm) {
    return (
      <main className="min-h-screen p-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <button
              onClick={() => setShowForm(false)}
              className="text-travel-600 hover:text-travel-700 font-medium transition-colors"
            >
              ← Back to Home
            </button>
          </div>
          
          <TravelForm />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen relative overflow-hidden">
      {/* Floating Background Icons */}
      <div className="absolute inset-0 pointer-events-none">
        {floatingIcons.map(({ Icon, delay, position }, index) => (
          <Icon
            key={index}
            className={`
              absolute w-12 h-12 text-travel-200 opacity-20
              animate-float ${position}
            `}
            style={{ animationDelay: delay }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center space-y-8 mb-16">
          {/* Logo/Brand */}
          <div className="flex items-center justify-center space-x-3 mb-8">
            <div className="relative">
              <Plane className="w-12 h-12 text-travel-600 animate-float" />
              <Sparkles className="w-6 h-6 text-sunset-500 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold font-display">
              <span className="bg-gradient-to-r from-travel-600 to-sunset-500 bg-clip-text text-transparent">
                GPTravel
              </span>
            </h1>
          </div>

          {/* Main Headline */}
          <div className="space-y-4">
            <h2 className="text-5xl md:text-7xl font-bold font-display leading-tight">
              <span className="block text-gray-900">Your AI-Powered</span>
              <span className="block bg-gradient-to-r from-travel-600 via-sunset-500 to-travel-700 bg-clip-text text-transparent">
                Travel Companion
              </span>
            </h2>
            <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Create personalized travel itineraries in seconds using the power of AI. 
              From romantic getaways to business trips, we craft the perfect journey just for you.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button
              size="lg"
              onClick={() => setShowForm(true)}
              className="w-full sm:w-auto text-lg px-8 py-4 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300"
            >
              Start Planning ✈️
            </Button>
            
            <div className="flex gap-4">
              <Button
                variant="ghost"
                size="lg"
                onClick={() => window.open('https://github.com/RobertoCorti/gptravel', '_blank')}
                className="text-gray-600 hover:text-travel-600 transition-colors"
              >
                <Github className="w-5 h-5 mr-2" />
                GitHub
              </Button>
              
              <Button
                variant="ghost"
                size="lg"
                onClick={() => window.open('https://gptravel-demo.vercel.app', '_blank')}
                className="text-gray-600 hover:text-travel-600 transition-colors"
              >
                <ExternalLink className="w-5 h-5 mr-2" />
                Live Demo
              </Button>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: Sparkles,
              title: 'AI-Powered',
              description: 'Advanced GPT-4 technology creates personalized itineraries based on your preferences and travel style.',
              gradient: 'from-purple-500 to-pink-500',
            },
            {
              icon: Map,
              title: 'Smart Planning',
              description: 'Intelligent routing and activity suggestions that optimize your time and maximize your experiences.',
              gradient: 'from-travel-500 to-cyan-500',
            },
            {
              icon: Heart,
              title: 'Personalized',
              description: 'Whether business, romantic, or adventure - every itinerary is tailored to your unique travel goals.',
              gradient: 'from-sunset-500 to-red-500',
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="group p-8 rounded-2xl bg-white/80 backdrop-blur-sm border border-gray-200 hover:shadow-xl hover:scale-105 transition-all duration-300"
            >
              <div className={`w-16 h-16 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-8 h-8 text-white" />
              </div>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-4 group-hover:text-travel-600 transition-colors">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16 space-y-4">
          <p className="text-gray-600 text-lg">
            Ready to explore the world with AI as your guide?
          </p>
          <Button
            size="lg"
            onClick={() => setShowForm(true)}
            className="shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300"
          >
            Create Your Journey 🗺️
          </Button>
        </div>
      </div>
    </main>
  );
} 
