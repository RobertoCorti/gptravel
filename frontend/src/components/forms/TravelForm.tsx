'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, MapPin, Loader2, AlertCircle, Key, CheckCircle, Heart, Briefcase, Users, User } from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import TravelResults from '@/components/travel/TravelResults';
import { generateTravelPlan, checkBackendHealth } from '@/lib/api';
import { TravelPlanResponse } from '@/types/travel';
import { SavedTravelPlan } from '@/lib/storage';

// Form validation schema
const travelFormSchema = z.object({
  openaiKey: z.string().min(1, 'OpenAI API key is required'),
  departure: z.string().min(1, 'Departure location is required'),
  destination: z.string().min(1, 'Destination is required'),
  departureDate: z.date(),
  returnDate: z.date(),
  travelReason: z.enum(['', 'Business', 'Romantic', 'Solo', 'Friends', 'Family']),
}).refine((data) => data.returnDate > data.departureDate, {
  message: "Return date must be after departure date",
  path: ["returnDate"],
});

type TravelFormData = z.infer<typeof travelFormSchema>;

interface TravelFormProps {
  loadedPlan?: SavedTravelPlan | null;
  onPlanLoaded?: () => void;
}

const travelReasons = [
  { value: '', label: 'Select travel reason', icon: null },
  { value: 'Business', label: 'Business', icon: Briefcase },
  { value: 'Romantic', label: 'Romantic', icon: Heart },
  { value: 'Solo', label: 'Solo', icon: User },
  { value: 'Friends', label: 'Friends', icon: Users },
  { value: 'Family', label: 'Family', icon: Users },
];

export default function TravelForm({ loadedPlan, onPlanLoaded }: TravelFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [travelPlan, setTravelPlan] = useState<TravelPlanResponse | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  const form = useForm<TravelFormData>({
    resolver: zodResolver(travelFormSchema),
    defaultValues: {
      openaiKey: '',
      departure: '',
      destination: '',
      departureDate: new Date(),
      returnDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      travelReason: '',
    },
  });

  const { register, handleSubmit, formState: { errors }, watch, setValue, reset } = form;

  // Load saved plan data when loadedPlan changes
  useEffect(() => {
    if (loadedPlan) {
      setValue('departure', loadedPlan.formData.departure);
      setValue('destination', loadedPlan.formData.destination);
      setValue('departureDate', loadedPlan.formData.departureDate);
      setValue('returnDate', loadedPlan.formData.returnDate);
      // Handle travelReason with fallback to empty string
      const reason = loadedPlan.formData.travelReason;
      if (reason && ['Business', 'Romantic', 'Solo', 'Friends', 'Family'].includes(reason)) {
        setValue('travelReason', reason as 'Business' | 'Romantic' | 'Solo' | 'Friends' | 'Family');
      } else {
        setValue('travelReason', '');
      }
      
      // Call onPlanLoaded to indicate the plan has been loaded
      onPlanLoaded?.();
    }
  }, [loadedPlan, setValue, onPlanLoaded]);

  // Check backend health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await checkBackendHealth();
        setBackendStatus('online');
      } catch (error) {
        setBackendStatus('offline');
      }
    };

    checkHealth();
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  const handleFormSubmit = async (data: TravelFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await generateTravelPlan(data);
      setTravelPlan(result);
    } catch (err) {
      console.error('Travel planning error:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate travel plan');
    } finally {
      setIsLoading(false);
    }
  };

  // If travel plan is generated, show results
  if (travelPlan) {
    return (
      <motion.div
        key="results"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.5 }}
        className="space-y-8"
      >
        <TravelResults 
          travelPlan={travelPlan} 
          formData={{
            departure: watch('departure'),
            destination: watch('destination'),
            departureDate: watch('departureDate'),
            returnDate: watch('returnDate'),
            travelReason: watch('travelReason')
          }}
        />
        <div className="flex justify-center">
          <Button
            onClick={() => {
              setTravelPlan(null);
              setError(null);
            }}
            variant="ghost"
            className="flex items-center gap-2"
          >
            ← Plan Another Trip
          </Button>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className="max-w-2xl mx-auto"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Loaded Plan Indicator */}
      <AnimatePresence>
        {loadedPlan && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 flex items-center gap-3"
          >
            <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
              <CheckCircle className="h-4 w-4 text-white" />
            </div>
            <div>
              <p className="text-blue-800 font-medium">
                Loaded plan: {loadedPlan.name}
              </p>
              <p className="text-blue-600 text-sm">
                You can modify the details below and generate a new plan
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Backend Status */}
      <AnimatePresence>
        {backendStatus !== 'checking' && (
          <motion.div
            variants={itemVariants}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-6"
          >
            <div className={`p-4 rounded-xl border flex items-center gap-3 ${
              backendStatus === 'online' 
                ? 'bg-green-50 border-green-200' 
                : 'bg-yellow-50 border-yellow-200'
            }`}>
              <div className={`w-3 h-3 rounded-full ${
                backendStatus === 'online' ? 'bg-green-500' : 'bg-yellow-500'
              }`} />
              <span className={`text-sm font-medium ${
                backendStatus === 'online' ? 'text-green-800' : 'text-yellow-800'
              }`}>
                {backendStatus === 'online' 
                  ? 'AI Backend: Online & Ready' 
                  : 'AI Backend: Offline (Using Fallback)'}
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.form
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        onSubmit={handleSubmit(handleFormSubmit)}
        className="space-y-6"
      >
        {/* API Key Input */}
        <motion.div variants={itemVariants} className="space-y-2">
          <label htmlFor="openaiKey" className="block text-sm font-medium text-gray-700">
            OpenAI API Key *
          </label>
          <div className="relative">
            <Key className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <Input
              {...register('openaiKey')}
              id="openaiKey"
              type="password"
              placeholder="sk-..."
              className="pl-10"
              error={errors.openaiKey?.message}
            />
          </div>
          <p className="text-xs text-gray-500">
            Your API key is secure and only used for this request. Get one at{' '}
            <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-travel-600 hover:text-travel-700">
              OpenAI Platform
            </a>
          </p>
        </motion.div>

        {/* Location Inputs */}
        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label htmlFor="departure" className="block text-sm font-medium text-gray-700">
              From *
            </label>
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                {...register('departure')}
                id="departure"
                placeholder="New York, NY"
                className="pl-10"
                error={errors.departure?.message}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="destination" className="block text-sm font-medium text-gray-700">
              To *
            </label>
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                {...register('destination')}
                id="destination"
                placeholder="Paris, France"
                className="pl-10"
                error={errors.destination?.message}
              />
            </div>
          </div>
        </motion.div>

        {/* Date Inputs */}
        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label htmlFor="departureDate" className="block text-sm font-medium text-gray-700">
              Departure Date *
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                {...register('departureDate', { valueAsDate: true })}
                id="departureDate"
                type="date"
                className="pl-10"
                error={errors.departureDate?.message}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="returnDate" className="block text-sm font-medium text-gray-700">
              Return Date *
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                {...register('returnDate', { valueAsDate: true })}
                id="returnDate"
                type="date"
                className="pl-10"
                error={errors.returnDate?.message}
              />
            </div>
          </div>
        </motion.div>

        {/* Travel Reason - Interactive Button Selection */}
        <motion.div variants={itemVariants} className="space-y-3">
          <label className="block text-sm font-medium text-gray-700">
            Travel Reason (Optional)
          </label>
          <motion.div
            className="grid grid-cols-2 md:grid-cols-5 gap-3"
            variants={containerVariants}
          >
            {travelReasons.slice(1).map((reason, index) => {
              const Icon = reason.icon;
              const isSelected = watch('travelReason') === reason.value;
              
              return (
                <motion.button
                  key={reason.value}
                  type="button"
                  onClick={() => setValue('travelReason', reason.value as any)}
                  className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                    isSelected
                      ? 'border-travel-500 bg-travel-50 text-travel-700 shadow-md'
                      : 'border-gray-200 hover:border-travel-300 hover:bg-travel-25 bg-white'
                  }`}
                  variants={itemVariants}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  transition={{ type: "spring", stiffness: 400, damping: 17 }}
                >
                  {Icon && (
                    <motion.div
                      animate={isSelected ? { 
                        scale: [1, 1.2, 1],
                        rotate: [0, 5, -5, 0] 
                      } : {}}
                      transition={{ duration: 0.5 }}
                      className="mb-2"
                    >
                      <Icon className="h-6 w-6 mx-auto" />
                    </motion.div>
                  )}
                  <span className="text-sm font-medium block">{reason.label}</span>
                </motion.button>
              );
            })}
          </motion.div>
          {errors.travelReason && (
            <motion.p 
              className="text-red-600 text-sm mt-2"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {errors.travelReason.message}
            </motion.p>
          )}
        </motion.div>

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3"
            >
              <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-red-800 font-medium">Error</h4>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Submit Button */}
        <motion.div variants={itemVariants}>
          <Button
            type="submit"
            size="lg"
            className="w-full"
            isLoading={isLoading}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                Creating Your Perfect Trip...
              </>
            ) : (
              <>
                ✨ Generate Travel Plan
              </>
            )}
          </Button>
        </motion.div>
      </motion.form>
    </motion.div>
  );
} 
