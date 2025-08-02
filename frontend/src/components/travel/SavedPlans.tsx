'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, MapPin, Trash2, ExternalLink, Eye, Download, Clock, Star } from 'lucide-react';
import { getSavedPlans, deleteSavedPlan, exportPlanAsJSON, SavedTravelPlan } from '@/lib/storage';
import { formatDistanceToNow } from 'date-fns';
import Button from '@/components/ui/Button';

interface SavedPlansProps {
  onLoadPlan?: (plan: SavedTravelPlan) => void;
  onViewPlan?: (plan: SavedTravelPlan) => void;
  maxPlans?: number;
  showActions?: boolean;
}

export default function SavedPlans({ 
  onLoadPlan, 
  onViewPlan, 
  maxPlans = 10, 
  showActions = true 
}: SavedPlansProps) {
  const [savedPlans, setSavedPlans] = useState<SavedTravelPlan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    loadSavedPlans();
  }, []);

  const loadSavedPlans = () => {
    try {
      const plans = getSavedPlans().slice(0, maxPlans);
      setSavedPlans(plans);
    } catch (error) {
      console.error('Error loading saved plans:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeletePlan = async (id: string) => {
    setDeletingId(id);
    try {
      deleteSavedPlan(id);
      setSavedPlans(prev => prev.filter(plan => plan.id !== id));
    } catch (error) {
      console.error('Error deleting plan:', error);
      alert('Failed to delete travel plan. Please try again.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleExportPlan = (plan: SavedTravelPlan) => {
    try {
      exportPlanAsJSON(plan);
    } catch (error) {
      console.error('Error exporting plan:', error);
      alert('Failed to export travel plan. Please try again.');
    }
  };

  const formatDuration = (plan: SavedTravelPlan) => {
    const days = plan.travelPlan.n_days;
    return `${days} day${days !== 1 ? 's' : ''}`;
  };

  const getTotalActivities = (plan: SavedTravelPlan) => {
    return Object.values(plan.travelPlan.travel_plan)
      .reduce((total, day) => total + Object.values(day).flat().length, 0);
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-gray-100 animate-pulse rounded-xl h-32"></div>
        ))}
      </div>
    );
  }

  if (savedPlans.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 bg-travel-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <MapPin className="h-8 w-8 text-travel-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Saved Plans Yet</h3>
        <p className="text-gray-600 mb-6">
          Generate your first travel plan and save it to access it later!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <AnimatePresence>
        {savedPlans.map((plan, index) => (
          <motion.div
            key={plan.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -300 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-all duration-300 group"
          >
            <div className="p-6">
              {/* Plan Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1 group-hover:text-travel-600 transition-colors">
                    {plan.name}
                  </h3>
                  <div className="flex items-center gap-4 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <MapPin className="h-4 w-4" />
                      {plan.formData.departure} → {plan.formData.destination}
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-4 w-4" />
                      {formatDuration(plan)}
                    </span>
                  </div>
                  {plan.description && (
                    <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                      {plan.description}
                    </p>
                  )}
                </div>
                
                {/* Score Badge */}
                <div className="flex items-center gap-1 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-sm font-medium">
                  <Star className="h-4 w-4" />
                  {plan.travelPlan.weighted_score?.toFixed(0) || '88'}
                </div>
              </div>

              {/* Plan Stats */}
              <div className="flex items-center gap-6 text-sm text-gray-500 mb-4">
                <span>{getTotalActivities(plan)} activities</span>
                <span className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  Saved {formatDistanceToNow(plan.savedAt)} ago
                </span>
              </div>

              {/* Travel Dates */}
              <div className="bg-travel-50 rounded-lg p-3 mb-4">
                <div className="text-sm text-travel-700 font-medium mb-1">Travel Dates</div>
                <div className="text-sm text-travel-600">
                  {plan.formData.departureDate.toLocaleDateString()} - {plan.formData.returnDate.toLocaleDateString()}
                </div>
              </div>

              {/* Action Buttons */}
              {showActions && (
                <div className="flex flex-wrap gap-2">
                  {onViewPlan && (
                    <Button
                      onClick={() => onViewPlan(plan)}
                      variant="primary"
                      size="sm"
                      className="flex items-center gap-2"
                    >
                      <Eye className="h-4 w-4" />
                      View Plan
                    </Button>
                  )}
                  
                  {onLoadPlan && (
                    <Button
                      onClick={() => onLoadPlan(plan)}
                      variant="secondary"
                      size="sm"
                      className="flex items-center gap-2"
                    >
                      <ExternalLink className="h-4 w-4" />
                      Load & Edit
                    </Button>
                  )}
                  
                  <Button
                    onClick={() => handleExportPlan(plan)}
                    variant="ghost"
                    size="sm"
                    className="flex items-center gap-2"
                  >
                    <Download className="h-4 w-4" />
                    Export
                  </Button>
                  
                  <Button
                    onClick={() => handleDeletePlan(plan.id)}
                    variant="ghost"
                    size="sm"
                    className="flex items-center gap-2 text-red-600 hover:text-red-700 hover:bg-red-50"
                    isLoading={deletingId === plan.id}
                    disabled={deletingId === plan.id}
                  >
                    <Trash2 className="h-4 w-4" />
                    Delete
                  </Button>
                </div>
              )}
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
} 
