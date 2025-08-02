'use client';

import { useState } from 'react';
import { Calendar, MapPin, Users, Star, Camera, ExternalLink } from 'lucide-react';
import { TravelPlanResponse } from '@/types/travel';
import { getActivityPhoto, getDestinationPhoto } from '@/lib/unsplash';
import Image from 'next/image';

interface TravelResultsProps {
  travelPlan: TravelPlanResponse;
}

// Fallback image component
const FallbackImage = ({ alt, className }: { alt: string; className: string }) => (
  <div className={`${className} bg-gradient-to-br from-travel-100 to-travel-200 flex items-center justify-center`}>
    <Camera className="h-8 w-8 text-travel-400" />
  </div>
);

export default function TravelResults({ travelPlan }: TravelResultsProps) {
  const [selectedDay, setSelectedDay] = useState<string>(
    Object.keys(travelPlan.travel_plan)[0] || 'Day 1'
  );
  const [imageErrors, setImageErrors] = useState<Set<string>>(new Set());

  const days = Object.keys(travelPlan.travel_plan);
  const selectedActivities = travelPlan.travel_plan[selectedDay];

  // Get a beautiful destination header photo
  const destinationPhoto = getDestinationPhoto(travelPlan.destination_place);

  const handleImageError = (imageId: string) => {
    setImageErrors(prev => new Set(prev).add(imageId));
  };

  return (
    <div className="space-y-8">
      {/* Beautiful Destination Header */}
      <div className="relative h-64 rounded-2xl overflow-hidden">
        {!imageErrors.has('destination-header') ? (
          <Image
            src={destinationPhoto.url}
            alt={destinationPhoto.alt}
            fill
            className="object-cover"
            priority
            onError={() => handleImageError('destination-header')}
          />
        ) : (
          <FallbackImage 
            alt={destinationPhoto.alt} 
            className="w-full h-full"
          />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
        <div className="absolute bottom-6 left-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Your {travelPlan.n_days}-Day Journey to {travelPlan.destination_place}
          </h1>
          <p className="text-white/90 flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            From {travelPlan.departure_place}
          </p>
        </div>
        
        {/* Photo Credit */}
        <div className="absolute bottom-2 right-2">
          <a 
            href={destinationPhoto.photographer_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-white/70 text-xs hover:text-white transition-colors flex items-center gap-1"
          >
            <Camera className="h-3 w-3" />
            Photo by {destinationPhoto.photographer}
          </a>
        </div>
      </div>

      {/* Trip Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-travel-500 to-travel-600 text-white p-6 rounded-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-travel-100">Duration</p>
              <p className="text-2xl font-bold">{travelPlan.n_days} Days</p>
            </div>
            <Calendar className="h-8 w-8 text-travel-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-sunset-500 to-sunset-600 text-white p-6 rounded-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sunset-100">Activities</p>
              <p className="text-2xl font-bold">
                {Object.values(travelPlan.travel_plan)
                  .reduce((total, day) => total + Object.values(day).flat().length, 0)}
              </p>
            </div>
            <Users className="h-8 w-8 text-sunset-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 text-white p-6 rounded-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-emerald-100">Trip Score</p>
              <p className="text-2xl font-bold">{travelPlan.weighted_score?.toFixed(0) || '88'}/100</p>
            </div>
            <Star className="h-8 w-8 text-emerald-200" />
          </div>
        </div>
      </div>

      {/* Day Navigation */}
      <div className="flex space-x-2 overflow-x-auto pb-2">
        {days.map((day) => (
          <button
            key={day}
            onClick={() => setSelectedDay(day)}
            className={`px-6 py-3 rounded-xl font-medium whitespace-nowrap transition-all duration-200 ${
              selectedDay === day
                ? 'bg-travel-500 text-white shadow-lg scale-105'
                : 'bg-gray-100 text-gray-700 hover:bg-travel-50 hover:text-travel-600'
            }`}
          >
            {day}
          </button>
        ))}
      </div>

      {/* Selected Day Activities */}
      {selectedActivities && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
            <div className="w-8 h-8 bg-travel-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
              {selectedDay.split(' ')[1]}
            </div>
            {selectedDay} Itinerary
          </h2>

          {Object.entries(selectedActivities).map(([city, activities], cityIndex) => (
            <div key={city} className="space-y-4">
              <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
                <MapPin className="h-5 w-5 text-travel-600" />
                {city}
              </h3>

              <div className="grid gap-4">
                {activities.map((activity, activityIndex) => {
                  const photo = getActivityPhoto(activity, city);
                  const imageId = `activity-${selectedDay}-${cityIndex}-${activityIndex}`;
                  
                  return (
                    <div
                      key={activityIndex}
                      className="bg-white rounded-xl border border-gray-200 hover:shadow-lg transition-all duration-300 overflow-hidden group"
                    >
                      <div className="flex flex-col md:flex-row">
                        {/* Activity Photo with Error Handling */}
                        <div className="relative w-full md:w-48 h-48 md:h-32">
                          {!imageErrors.has(imageId) ? (
                            <Image
                              src={photo.url}
                              alt={photo.alt}
                              fill
                              className="object-cover group-hover:scale-105 transition-transform duration-300"
                              onError={() => handleImageError(imageId)}
                            />
                          ) : (
                            <FallbackImage 
                              alt={photo.alt} 
                              className="w-full h-full group-hover:scale-105 transition-transform duration-300"
                            />
                          )}
                          <div className="absolute top-2 left-2 bg-travel-500 text-white px-2 py-1 rounded-full text-xs font-medium">
                            #{activityIndex + 1}
                          </div>
                        </div>

                        {/* Activity Details */}
                        <div className="p-4 flex-1 flex flex-col justify-between">
                          <div>
                            <h4 className="font-medium text-gray-900 mb-2 group-hover:text-travel-600 transition-colors">
                              {activity}
                            </h4>
                            <p className="text-sm text-gray-600 flex items-center gap-1">
                              <MapPin className="h-4 w-4" />
                              {city}
                            </p>
                          </div>
                          
                          {/* Action Buttons */}
                          <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                            <div className="text-xs text-gray-500 flex items-center gap-1">
                              <Camera className="h-3 w-3" />
                              Photo by {photo.photographer}
                            </div>
                            <div className="flex gap-2">
                              <button className="text-xs text-travel-600 hover:text-travel-700 font-medium flex items-center gap-1">
                                <ExternalLink className="h-3 w-3" />
                                Learn More
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 pt-6 border-t border-gray-200">
        <button className="flex-1 bg-travel-500 text-white py-3 px-6 rounded-xl font-medium hover:bg-travel-600 transition-colors flex items-center justify-center gap-2">
          <ExternalLink className="h-5 w-5" />
          Share This Plan
        </button>
        <button className="flex-1 bg-gray-100 text-gray-700 py-3 px-6 rounded-xl font-medium hover:bg-gray-200 transition-colors">
          Download PDF
        </button>
      </div>
    </div>
  );
} 
