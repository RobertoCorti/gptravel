# GPTravel 🛫

**Your AI-Powered Travel Companion** - Create personalized travel itineraries in seconds using the power of AI. From romantic getaways to business trips, we craft the perfect journey just for you.

![GPTravel Homepage](./img/homepage.png)

## ✨ Features

### 🤖 **AI-Powered Planning**
- **Advanced AI Integration**: Creates intelligent, personalized travel itineraries
- **Smart Suggestions**: Activity recommendations based on your preferences and travel style
- **Contextual Planning**: Considers travel dates, location, and trip purpose

### 💾 **Plan Management** 
- **Save & Load Plans**: Keep your favorite itineraries for future reference
- **Plan Library**: Browse and manage up to 10 recent travel plans
- **Export Functionality**: Download plans as JSON files
- **Quick Edit**: Load saved plans and modify them to create new variations

### 🎨 **Modern User Experience**
- **Beautiful Interface**: Clean, responsive design built with Next.js and Tailwind CSS
- **Interactive Forms**: Engaging travel reason selector with animated icons
- **Real-time Feedback**: Live backend status and error handling
- **Smooth Animations**: Powered by Framer Motion for delightful interactions

### 🌍 **Visual Travel Experience**
- **Dynamic Photos**: Beautiful destination and activity images from Unsplash
- **Interactive Itineraries**: Day-by-day navigation with photo galleries
- **Graceful Fallbacks**: Elegant placeholders when images fail to load
- **Responsive Design**: Perfect experience on desktop and mobile


## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.8+ and Poetry
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone and Setup
```bash
git clone https://github.com/RobertoCorti/gptravel.git
cd gptravel

# Install Python dependencies
poetry install

# Install frontend dependencies
cd frontend
npm install
```

### 2. Start the Backend
```bash
# From project root
poetry run python start_backend.py
# Backend runs on http://127.0.0.1:8000
```

### 3. Start the Frontend
```bash
# From frontend directory
cd frontend
npm run dev
# Frontend runs on http://localhost:3000
```

### 4. Start Planning! ✈️
1. Open your browser to `http://localhost:3000`
2. Click **"Start Planning"**
3. Enter your OpenAI API key
4. Fill in your travel details
5. Choose your travel style with the interactive selector
6. Generate and save your perfect itinerary!


## 🛠️ Development

### **Project Structure**
```
gptravel/
├── frontend/                 # Next.js React app
│   ├── src/
│   │   ├── app/             # Next.js app router pages
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/             # Utilities and API clients
│   │   └── types/           # TypeScript type definitions
│   └── public/              # Static assets
├── src/gptravel/            # Python backend modules
│   ├── core/               # Core business logic
│   ├── prototype/          # Legacy Streamlit app
│   └── main.py             # Application entry point
├── backend_api.py          # FastAPI server
├── start_backend.py        # Backend startup script
└── tests/                  # Test suites
```

### **Key Technologies**
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Pydantic, OpenAI API, Python 3.8+
- **Development**: Poetry, ESLint, Prettier, Hot reload
- **Deployment**: Docker support, Vercel-ready frontend

### **Contributing**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request


## 🔧 Configuration

### **Environment Variables**
```bash

# Backend 
OPENAI_API_KEY=your_openai_key_here  # Optional, can be provided via form
```

### **Customization**
- **Colors**: Edit `frontend/tailwind.config.js` for custom color schemes
- **Components**: Modify UI components in `frontend/src/components/`
- **AI Prompts**: Customize travel planning logic in `src/gptravel/core/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
