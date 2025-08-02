'use client';

import { useState } from 'react';
import { MapPin, Calendar, Star, Clock, Share2, Download } from 'lucide-react';
import Button from '@/components/ui/Button';
import { TravelPlanResponse } from '@/types/travel';
import { format, addDays } from 'date-fns';

interface TravelResultsProps {
  travelPlan: TravelPlanResponse;
}

export default function TravelResults({ travelPlan }: TravelResultsProps) {
  const [activeDay, setActiveDay] = useState(0);
  
  const days = Object.keys(travelPlan.travel_plan);
  const startDate = new Date(); // You might want to pass this from the form

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: `${travelPlan.destination_place} Travel Plan`,
        text: `Check out my AI-generated travel plan for ${travelPlan.destination_place}!`,
        url: window.location.href,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  const handleDownload = () => {
    // TODO: Implement PDF/text download functionality
    alert('Download feature coming soon!');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {travelPlan.departure_place} → {travelPlan.destination_place}
            </h1>
            <div className="flex items-center space-x-6 text-gray-600">
              <div className="flex items-center space-x-2">
                <Calendar className="h-5 w-5" />
                <span>{travelPlan.n_days} days</span>
              </div>
              {travelPlan.weighted_score && (
                <div className="flex items-center space-x-2">
                  <Star className="h-5 w-5 text-yellow-500" />
                  <span className="font-medium">{travelPlan.weighted_score}/100</span>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex space-x-3">
            <Button variant="secondary" size="sm" onClick={handleShare}>
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
            <Button variant="secondary" size="sm" onClick={handleDownload}>
              <Download className="h-4 w-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
      </div>

      {/* Travel Plan */}
      <div className="grid lg:grid-cols-4 gap-6">
        {/* Days Navigation */}
        <div className="lg:col-span-1">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Itinerary</h3>
            <div className="space-y-2">
              {days.map((day, index) => {
                const date = addDays(startDate, index);
                const isActive = activeDay === index;
                
                return (
                  <button
                    key={day}
                    onClick={() => setActiveDay(index)}
                    className={`w-full text-left p-3 rounded-lg transition-colors duration-200 ${
                      isActive
                        ? 'bg-travel-50 border border-travel-200 text-travel-700'
                        : 'hover:bg-gray-50 border border-gray-200'
                    }`}
                  >
                    <div className="font-medium">{day}</div>
                    <div className="text-sm text-gray-500">
                      {format(date, 'MMM dd, yyyy')}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Day Details */}
        <div className="lg:col-span-3">
          <div className="card">
            {(() => {
              const selectedDay = days[activeDay];
              const dayPlan = travelPlan.travel_plan[selectedDay];
              const date = addDays(startDate, activeDay);
              
              return (
                <div>
                  <div className="flex items-center space-x-3 mb-6">
                    <Calendar className="h-6 w-6 text-travel-600" />
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">{selectedDay}</h2>
                      <p className="text-gray-600">{format(date, 'EEEE, MMMM dd, yyyy')}</p>
                    </div>
                  </div>

                  <div className="space-y-6">
                    {Object.entries(dayPlan).map(([city, activities]) => (
                      <div key={city} className="border-l-4 border-travel-200 pl-4">
                        <div className="flex items-center space-x-2 mb-4">
                          <MapPin className="h-5 w-5 text-travel-600" />
                          <h3 className="text-xl font-semibold text-gray-900">{city}</h3>
                        </div>
                        
                        <div className="space-y-3">
                          {activities.map((activity, activityIndex) => (
                            <div 
                              key={activityIndex}
                              className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                            >
                              <div className="flex-shrink-0 mt-1">
                                <div className="w-6 h-6 bg-travel-100 text-travel-600 rounded-full flex items-center justify-center text-sm font-medium">
                                  {activityIndex + 1}
                                </div>
                              </div>
                              <div className="flex-1">
                                <p className="text-gray-900">{activity}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })()}
          </div>
        </div>
      </div>

      {/* Trip Summary */}
      <div className="card">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Trip Summary</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-travel-600">{travelPlan.n_days}</div>
            <div className="text-gray-600">Days</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-travel-600">
              {Object.values(travelPlan.travel_plan).reduce(
                (total, day) => total + Object.values(day).flat().length, 0
              )}
            </div>
            <div className="text-gray-600">Activities</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-travel-600">
              {new Set(Object.values(travelPlan.travel_plan).flatMap(day => Object.keys(day))).size}
            </div>
            <div className="text-gray-600">Cities</div>
          </div>
        </div>
      </div>
    </div>
  );
} 
