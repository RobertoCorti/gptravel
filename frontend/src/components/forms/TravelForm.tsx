'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Calendar, MapPin, Key, Heart, Briefcase, Users, User } from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { TravelFormData } from '@/types/travel';
import { formatDate, isValidDateRange, validateOpenAIKey } from '@/lib/utils';

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
  onSubmit: (data: TravelFormData) => void;
}

const travelReasons = [
  { value: '', label: 'Select travel reason', icon: null },
  { value: 'Business', label: 'Business', icon: Briefcase },
  { value: 'Romantic', label: 'Romantic', icon: Heart },
  { value: 'Solo', label: 'Solo', icon: User },
  { value: 'Friends', label: 'Friends', icon: Users },
  { value: 'Family', label: 'Family', icon: Users },
];

export default function TravelForm({ onSubmit }: TravelFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<TravelFormValues>({
    resolver: zodResolver(travelSchema),
    defaultValues: {
      departureDate: new Date(),
      returnDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      travelReason: '',
    },
  });

  const handleFormSubmit = async (data: TravelFormValues) => {
    setIsSubmitting(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="card">
        <div className="grid md:grid-cols-2 gap-6">
          {/* OpenAI API Key */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-2 mb-2">
              <Key className="h-5 w-5 text-travel-600" />
              <label className="block text-sm font-medium text-gray-700">
                OpenAI API Key
              </label>
            </div>
            <Input
              type="password"
              placeholder="sk-..."
              error={errors.openaiKey?.message}
              helperText="Your API key is used to generate personalized travel plans"
              {...register('openaiKey')}
            />
          </div>

          {/* Departure */}
          <div>
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
          </div>

          {/* Destination */}
          <div>
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
          </div>

          {/* Departure Date */}
          <div>
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
          </div>

          {/* Return Date */}
          <div>
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
          </div>

          {/* Travel Reason */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Travel Reason
            </label>
            <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
              {travelReasons.slice(1).map((reason) => {
                const Icon = reason.icon;
                const isSelected = watch('travelReason') === reason.value;
                
                return (
                  <button
                    key={reason.value}
                    type="button"
                    onClick={() => setValue('travelReason', reason.value as any)}
                    className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                      isSelected
                        ? 'border-travel-500 bg-travel-50 text-travel-700'
                        : 'border-gray-200 hover:border-travel-300 hover:bg-travel-25'
                    }`}
                  >
                    {Icon && <Icon className="h-6 w-6 mx-auto mb-2" />}
                    <span className="text-sm font-medium">{reason.label}</span>
                  </button>
                );
              })}
            </div>
            {errors.travelReason && (
              <p className="text-red-600 text-sm mt-2">{errors.travelReason.message}</p>
            )}
          </div>
        </div>

        <div className="mt-8 flex justify-center">
          <Button
            type="submit"
            size="lg"
            isLoading={isSubmitting}
            className="w-full md:w-auto"
          >
            {isSubmitting ? 'Creating Your Plan...' : "Let's Go! ✈️"}
          </Button>
        </div>
      </div>
    </form>
  );
} 
