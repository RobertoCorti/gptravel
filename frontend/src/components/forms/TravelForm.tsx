'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, MapPin, Key, Heart, Briefcase, Users, User, AlertCircle, CheckCircle, Wifi, WifiOff, Sparkles } from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import TravelResults from '@/components/travel/TravelResults';
import { TravelFormData, TravelPlanResponse } from '@/types/travel';
import { formatDate, isValidDateRange, validateOpenAIKey } from '@/lib/utils';
import { generateTravelPlan, APIError, checkBackendHealth } from '@/lib/api';

const travelSchema = z.object({
  openaiKey: z.string()
    .min(1, 'OpenAI API key is required')
    .refine(validateOpenAIKey, 'Invalid OpenAI API key format'),
  departure: z.string().min(1, 'Departure location is required'),
  destination: z.string().min(1, 'Destination is required'),
  departureDate: z.date(),
  returnDate: z.date(),
  travelReason: z.enum(['Business', 'Romantic', 'Solo', 'Friends', 'Family', '']),
}).refine(
  (data) => isValidDateRange(data.departureDate, data.returnDate),
  {
    message: 'Return date must be after departure date',
    path: ['returnDate'],
  }
);

type TravelFormValues = z.infer<typeof travelSchema>;

interface TravelFormProps {
  onSubmit?: (data: TravelFormData) => void;
}

const travelReasons = [
  { value: '', label: 'Select travel reason', icon: null },
  { value: 'Business', label: 'Business', icon: Briefcase },
  { value: 'Romantic', label: 'Romantic', icon: Heart },
  { value: 'Solo', label: 'Solo', icon: User },
  { value: 'Friends', label: 'Friends', icon: Users },
  { value: 'Family', label: 'Family', icon: Users },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 20,
    },
  },
};

export default function TravelForm({ onSubmit }: TravelFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [travelPlan, setTravelPlan] = useState<TravelPlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
    reset,
  } = useForm<TravelFormValues>({
    resolver: zodResolver(travelSchema),
    defaultValues: {
      departureDate: new Date(),
      returnDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      travelReason: '',
    },
  });

  // Check backend health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const isHealthy = await checkBackendHealth();
        setBackendStatus(isHealthy ? 'online' : 'offline');
      } catch {
        setBackendStatus('offline');
      }
    };
    
    checkHealth();
  }, []);

  const handleFormSubmit = async (data: TravelFormValues) => {
    setIsSubmitting(true);
    setError(null);
    setSuccess(false);
    
    try {
      const result = await generateTravelPlan(data);
      setTravelPlan(result);
      setSuccess(true);
      
      // Call optional onSubmit callback
      if (onSubmit) {
        onSubmit(data);
      }
    } catch (err) {
      if (err instanceof APIError) {
        if (err.status === 400) {
          setError(`Validation Error: ${err.message}`);
        } else if (err.status >= 500) {
          setError(`Server Error: ${err.message}. Please try again in a moment.`);
        } else {
          setError(`API Error (${err.status}): ${err.message}`);
        }
      } else if (err instanceof Error) {
        if (err.message.includes('Unable to connect')) {
          setError(`${err.message}. ${backendStatus === 'offline' ? 'The AI backend appears to be offline.' : ''}`);
        } else {
          setError(err.message);
        }
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
      console.error('Travel plan generation failed:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleStartOver = () => {
    setTravelPlan(null);
    setError(null);
    setSuccess(false);
    reset();
  };

  // If we have a travel plan, show the results with animation
  if (travelPlan) {
    return (
      <motion.div 
        className="space-y-6"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <motion.div 
          className="flex items-center justify-between"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center space-x-2">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.3, type: "spring", stiffness: 300 }}
            >
              <CheckCircle className="h-6 w-6 text-green-600" />
            </motion.div>
            <h2 className="text-2xl font-semibold text-gray-900">
              Your Travel Plan is Ready!
            </h2>
          </div>
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button 
              variant="secondary" 
              onClick={handleStartOver}
            >
              Plan Another Trip
            </Button>
          </motion.div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <TravelResults travelPlan={travelPlan} />
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.form 
      onSubmit={handleSubmit(handleFormSubmit)} 
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Backend Status */}
      <AnimatePresence>
        {backendStatus !== 'checking' && (
          <motion.div 
            className={`flex items-center space-x-2 p-3 rounded-lg ${
              backendStatus === 'online' 
                ? 'bg-green-50 text-green-700 border border-green-200' 
                : 'bg-yellow-50 text-yellow-700 border border-yellow-200'
            }`}
            variants={itemVariants}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              {backendStatus === 'online' ? (
                <Wifi className="h-5 w-5" />
              ) : (
                <WifiOff className="h-5 w-5" />
              )}
            </motion.div>
            <span className="text-sm">
              {backendStatus === 'online' 
                ? 'AI Backend Online - Real GPT-powered travel planning available' 
                : 'AI Backend Offline - Using fallback planning (limited features)'
              }
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Display */}
      <AnimatePresence>
        {error && (
          <motion.div 
            className="bg-red-50 border border-red-200 rounded-xl p-4"
            variants={itemVariants}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
          >
            <div className="flex items-center space-x-2">
              <motion.div
                animate={{ rotate: [0, -10, 10, -10, 0] }}
                transition={{ duration: 0.5 }}
              >
                <AlertCircle className="h-5 w-5 text-red-600" />
              </motion.div>
              <p className="text-red-800 font-medium">Error generating travel plan</p>
            </div>
            <p className="text-red-700 mt-1">{error}</p>
            {backendStatus === 'offline' && (
              <p className="text-red-600 text-sm mt-2">
                💡 Tip: Start the Python backend with <code className="bg-red-100 px-1 rounded">python start_backend.py</code> for full AI features.
              </p>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div className="card" variants={itemVariants}>
        <motion.div 
          className="grid md:grid-cols-2 gap-6"
          variants={containerVariants}
        >
          {/* OpenAI API Key */}
          <motion.div className="md:col-span-2" variants={itemVariants}>
            <div className="flex items-center space-x-2 mb-2">
              <motion.div
                animate={{ 
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0]
                }}
                transition={{ 
                  duration: 2,
                  repeat: Infinity,
                  repeatDelay: 3
                }}
              >
                <Key className="h-5 w-5 text-travel-600" />
              </motion.div>
              <label className="block text-sm font-medium text-gray-700">
                OpenAI API Key
              </label>
            </div>
            <Input
              type="password"
              placeholder="sk-..."
              error={errors.openaiKey?.message}
              helperText="Your API key enables AI-powered travel planning"
              {...register('openaiKey')}
            />
          </motion.div>

          {/* Departure */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center space-x-2 mb-2">
              <MapPin className="h-5 w-5 text-emerald-600" />
              <label className="block text-sm font-medium text-gray-700">
                Departure
              </label>
            </div>
            <Input
              placeholder="New York, NY"
              error={errors.departure?.message}
              {...register('departure')}
            />
          </motion.div>

          {/* Destination */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center space-x-2 mb-2">
              <MapPin className="h-5 w-5 text-sunset-600" />
              <label className="block text-sm font-medium text-gray-700">
                Destination
              </label>
            </div>
            <Input
              placeholder="Paris, France"
              error={errors.destination?.message}
              {...register('destination')}
            />
          </motion.div>

          {/* Departure Date */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center space-x-2 mb-2">
              <Calendar className="h-5 w-5 text-travel-600" />
              <label className="block text-sm font-medium text-gray-700">
                Departure Date
              </label>
            </div>
            <Input
              type="date"
              error={errors.departureDate?.message}
              {...register('departureDate', { 
                valueAsDate: true,
                setValueAs: (value) => value ? new Date(value) : undefined 
              })}
            />
          </motion.div>

          {/* Return Date */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center space-x-2 mb-2">
              <Calendar className="h-5 w-5 text-travel-600" />
              <label className="block text-sm font-medium text-gray-700">
                Return Date
              </label>
            </div>
            <Input
              type="date"
              error={errors.returnDate?.message}
              {...register('returnDate', { 
                valueAsDate: true,
                setValueAs: (value) => value ? new Date(value) : undefined 
              })}
            />
          </motion.div>

          {/* Travel Reason */}
          <motion.div className="md:col-span-2" variants={itemVariants}>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Travel Reason
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
                        ? 'border-travel-500 bg-travel-50 text-travel-700'
                        : 'border-gray-200 hover:border-travel-300 hover:bg-travel-25'
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
                      >
                        <Icon className="h-6 w-6 mx-auto mb-2" />
                      </motion.div>
                    )}
                    <span className="text-sm font-medium">{reason.label}</span>
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
        </motion.div>

        <motion.div 
          className="mt-8 flex justify-center"
          variants={itemVariants}
        >
          <Button
            type="submit"
            size="lg"
            isLoading={isSubmitting}
            className="w-full md:w-auto group relative overflow-hidden"
          >
            <AnimatePresence mode="wait">
              {isSubmitting ? (
                <motion.div
                  key="loading"
                  className="flex items-center"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  >
                    <Sparkles className="mr-2 h-5 w-5" />
                  </motion.div>
                  {backendStatus === 'online' ? 'AI is crafting your perfect trip...' : 'Creating your trip plan...'}
                </motion.div>
              ) : (
                <motion.span
                  key="default"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center"
                >
                  Let's Go! ✈️
                </motion.span>
              )}
            </AnimatePresence>
          </Button>
        </motion.div>
      </motion.div>
    </motion.form>
  );
} 
