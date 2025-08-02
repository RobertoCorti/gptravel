'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, MapPin, Heart, Github, Plane, Camera, Globe } from 'lucide-react';
import TravelForm from '@/components/forms/TravelForm';
import SavedPlans from '@/components/travel/SavedPlans';
import TravelResults from '@/components/travel/TravelResults';
import { SavedTravelPlan } from '@/lib/storage';
import { getSavedPlans } from '@/lib/storage';
import Button from '@/components/ui/Button';

export default function Home() {
  const [showForm, setShowForm] = useState(false);
  const [showSavedPlans, setShowSavedPlans] = useState(false);
  const [loadedPlan, setLoadedPlan] = useState<SavedTravelPlan | null>(null);
  const [viewingPlan, setViewingPlan] = useState<SavedTravelPlan | null>(null);

  const handleLoadPlan = (plan: SavedTravelPlan) => {
    setLoadedPlan(plan);
    setShowSavedPlans(false);
    setShowForm(true);
  };

  const handleViewPlan = (plan: SavedTravelPlan) => {
    setViewingPlan(plan);
    setShowSavedPlans(false);
    setShowForm(false);
  };

  const handleBackToHome = () => {
    setShowForm(false);
    setShowSavedPlans(false);
    setLoadedPlan(null);
    setViewingPlan(null);
  };

  // Check if we have saved plans
  const hasSavedPlans = typeof window !== 'undefined' && getSavedPlans().length > 0;

  // If viewing a specific plan
  if (viewingPlan) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 text-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-2xl font-bold text-gray-900">
                {viewingPlan.name}
              </h1>
              <Button
                onClick={handleBackToHome}
                variant="ghost"
                className="flex items-center gap-2"
              >
                ← Back to Home
              </Button>
            </div>
            <TravelResults 
              travelPlan={viewingPlan.travelPlan} 
              formData={viewingPlan.formData}
            />
          </div>
        </div>
      </main>
    );
  }

  // If showing saved plans
  if (showSavedPlans) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 text-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-3xl font-bold text-gray-900">
                Your Saved Travel Plans
              </h1>
              <Button
                onClick={handleBackToHome}
                variant="ghost"
                className="flex items-center gap-2"
              >
                ← Back to Home
              </Button>
            </div>
            <SavedPlans 
              onLoadPlan={handleLoadPlan}
              onViewPlan={handleViewPlan}
              showActions={true}
            />
          </div>
        </div>
      </main>
    );
  }

  // If showing the form
  if (showForm) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 text-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-3xl font-bold text-gray-900">
                Plan Your Perfect Trip
              </h1>
              <Button
                onClick={handleBackToHome}
                variant="ghost"
                className="flex items-center gap-2"
              >
                ← Back to Home
              </Button>
            </div>
            <TravelForm 
              loadedPlan={loadedPlan}
              onPlanLoaded={() => setLoadedPlan(null)}
            />
          </div>
        </div>
      </main>
    );
  }

  // Homepage hero
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 text-gray-900">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          {/* Floating Icons */}
          <div className="relative mb-16">
            <motion.div
              className="absolute -top-4 -left-4 w-12 h-12 bg-travel-100 rounded-full flex items-center justify-center"
              animate={{ 
                y: [0, -10, 0],
                rotate: [0, 5, 0] 
              }}
              transition={{ 
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <Plane className="h-6 w-6 text-travel-600" />
            </motion.div>
            
            <motion.div
              className="absolute -top-8 right-8 w-10 h-10 bg-sunset-100 rounded-full flex items-center justify-center"
              animate={{ 
                y: [0, -15, 0],
                rotate: [0, -8, 0] 
              }}
              transition={{ 
                duration: 5,
                repeat: Infinity,
                ease: "easeInOut",
                delay: 1
              }}
            >
              <Camera className="h-5 w-5 text-sunset-600" />
            </motion.div>

            <motion.div
              className="absolute top-4 -right-2 w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center"
              animate={{ 
                y: [0, -8, 0],
                rotate: [0, 10, 0] 
              }}
              transition={{ 
                duration: 3.5,
                repeat: Infinity,
                ease: "easeInOut",
                delay: 2
              }}
            >
              <Globe className="h-4 w-4 text-purple-600" />
            </motion.div>

            {/* Main Logo */}
            <div className="flex items-center justify-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-br from-travel-500 to-sunset-500 rounded-2xl flex items-center justify-center shadow-xl mr-4">
                <Plane className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-4xl font-bold text-gray-900">
                GP<span className="bg-gradient-to-r from-travel-600 to-sunset-600 bg-clip-text text-transparent">Travel</span>
              </h1>
            </div>
          </div>

          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Your AI-Powered
              <br />
              <span className="bg-gradient-to-r from-travel-600 via-sunset-500 to-travel-600 bg-clip-text text-transparent">
                Travel Companion
              </span>
            </h2>
            
            <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Create personalized travel itineraries in seconds using the power of 
              AI. From romantic getaways to business trips, we craft the perfect 
              journey just for you.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <Button
                onClick={() => setShowForm(true)}
                variant="primary"
                size="lg"
                className="flex items-center gap-2 text-lg px-8 py-4"
              >
                Start Planning ✈️
              </Button>
              
              {hasSavedPlans && (
                <Button
                  onClick={() => setShowSavedPlans(true)}
                  variant="secondary"
                  size="lg"
                  className="flex items-center gap-2 text-lg px-8 py-4"
                >
                  <MapPin className="h-5 w-5" />
                  View Saved Plans
                </Button>
              )}
              
              <Button
                onClick={() => window.open('https://github.com/RobertoCorti/gptravel', '_blank')}
                variant="ghost"
                size="lg"
                className="flex items-center gap-2 text-lg px-8 py-4"
              >
                <Github className="h-5 w-5" />
                GitHub
              </Button>
              
              <Button
                onClick={() => window.open('#', '_blank')}
                variant="ghost"
                size="lg"
                className="flex items-center gap-2 text-lg px-8 py-4"
              >
                🌐 Live Demo
              </Button>
            </div>
          </motion.div>

          {/* Recent Saved Plans Preview */}
          {hasSavedPlans && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="mb-16"
            >
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-2xl font-bold text-gray-900">Recent Travel Plans</h3>
                  <Button
                    onClick={() => setShowSavedPlans(true)}
                    variant="ghost"
                    className="text-travel-600 hover:text-travel-700"
                  >
                    View All →
                  </Button>
                </div>
                <SavedPlans 
                  onLoadPlan={handleLoadPlan}
                  onViewPlan={handleViewPlan}
                  maxPlans={3}
                  showActions={true}
                />
              </div>
            </motion.div>
          )}

          {/* Feature Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {/* AI-Powered Feature */}
            <motion.div
              className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mb-6 mx-auto">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">AI-Powered</h3>
              <p className="text-gray-600 leading-relaxed">
                Advanced GPT-4 technology creates personalized itineraries based on 
                your preferences and travel style.
              </p>
            </motion.div>

            {/* Smart Planning Feature */}
            <motion.div
              className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-blue-500 rounded-xl flex items-center justify-center mb-6 mx-auto">
                <MapPin className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Smart Planning</h3>
              <p className="text-gray-600 leading-relaxed">
                Intelligent routing and activity suggestions that optimize your time 
                and maximize your experiences.
              </p>
            </motion.div>

            {/* Personalized Feature */}
            <motion.div
              className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center mb-6 mx-auto">
                <Heart className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Personalized</h3>
              <p className="text-gray-600 leading-relaxed">
                Whether business, romantic, or adventure - every itinerary is tailored 
                to your unique travel goals.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </main>
  );
} 
