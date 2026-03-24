export type Language = 'en' | 'hi';

export const translations = {
    en: {
        // Navigation
        nav: {
            home: 'Home',
            detect: 'Detect Disease',
            chat: 'Chat',
            team: 'About',
        },

        // Home page
        home: {
            title: 'AgriVision',
            subtitle: 'AI-Powered Plant Disease Detection',
            description: 'Early detection, healthier crops, better yields. Upload a photo of your plant and get instant disease diagnosis powered by advanced AI technology.',
            startDetection: 'Start Detection',
            liveDemo: 'Try Chat Assistant',
            powerfulFeatures: 'Powerful Features',
            howItWorks: 'How It Works',
            readyToProtect: 'Ready to Protect Your Crops?',
            getStartedFree: 'Get Started Free',
            features: {
                aiDetection: {
                    title: 'AI-Powered Detection',
                    desc: 'Advanced deep learning models trained on 70,000+ images for accurate disease identification'
                },
                chatbot: {
                    title: 'Expert AI Assistant',
                    desc: 'Get instant answers to your farming questions with our intelligent chatbot'
                },
                multilingual: {
                    title: 'Multilingual Support',
                    desc: 'Available in English and Hindi to help farmers across India'
                },
                treatment: {
                    title: 'Treatment Recommendations',
                    desc: 'Receive actionable treatment plans and prevention strategies'
                },
                explainable: {
                    title: 'Explainable AI',
                    desc: 'Understand why the AI made its diagnosis with clear explanations'
                },
                plants: {
                    title: '12+ Plant Species',
                    desc: 'Support for major crops including tomato, potato, corn, and more'
                }
            },
            steps: {
                upload: {
                    title: 'Upload Image',
                    desc: 'Take or upload a photo of the affected plant leaf'
                },
                analyze: {
                    title: 'AI Analysis',
                    desc: 'Our AI model analyzes the image in real-time'
                },
                results: {
                    title: 'Get Results',
                    desc: 'Receive diagnosis and treatment recommendations instantly'
                }
            },
            stats: {
                accuracy: 'Accuracy',
                diseases: 'Diseases',
                plants: 'Plants',
                images: 'Training Images'
            }
        },
        welcomeTitle: 'AI-Powered Plant Disease Detection',
        welcomeSubtitle: 'Early detection, healthier crops, better yields',
        getStarted: 'Get Started',
        learnMore: 'Learn More',

        // Features
        features: 'Features',
        accurateDetection: 'Accurate Detection',
        accurateDetectionDesc: '96% accuracy across 38 plant diseases',
        instantResults: 'Instant Results',
        instantResultsDesc: 'Get predictions in less than a second',
        expertAdvice: 'Expert Advice',
        expertAdviceDesc: 'AI-powered treatment recommendations',

        // Stats
        accuracy: 'Accuracy',
        diseases: 'Diseases Detected',
        plants: 'Plant Species',

        // Predict page
        predict: {
            title: 'Plant Disease Detection',
            subtitle: 'Upload an image or use your camera to detect plant diseases',
            uploadTab: 'Upload Image',
            cameraTab: 'Use Camera',
            dragDrop: 'Drag and drop an image here, or click to select',
            supports: 'Supports: JPG, PNG (Max 10MB)',
            startCamera: 'Start Camera',
            capture: 'Capture & Analyze',
            analyzing: 'Analyzing...',
            analyze: 'Analyze Image',
            uploadAnother: 'Upload Another Image',
            uploadToSee: 'Upload an image to see results',
            result: {
                healthy: 'Plant is Healthy!',
                diseased: 'Disease Detected',
                plant: 'Plant',
                status: 'Status',
                disease: 'Disease',
                confidence: 'Confidence',
                top5: 'Top 5 Predictions',
                recommendations: 'Treatment Recommendations',
                preventive: 'Preventive Measures',
                fungicides: 'Recommended Fungicides',
                precautions: 'Precautions',
                organic: 'Organic Options'
            }
        },
        uploadImage: 'Upload Image',
        useCamera: 'Use Camera',
        dragDrop: 'Drag and drop an image here, or click to select',
        analyzing: 'Analyzing...',
        analyzeImage: 'Analyze Image',

        // Results
        results: 'Results',
        plantName: 'Plant',
        diseaseName: 'Disease',
        confidence: 'Confidence',
        healthy: 'Healthy',
        recommendations: 'Treatment Recommendations',
        fungicides: 'Recommended Fungicides',
        organicOptions: 'Organic Options',
        precautions: 'Precautions',

        // Chat
        chat: {
            title: 'AI Assistant',
            context: 'Context',
            askAnything: 'Ask me anything about plant diseases and treatments!',
            chatPage: {
                title: 'AI Plant Disease Assistant',
                subtitle: 'Get expert advice on plant diseases and farming',
                welcome: 'Welcome to AgriVision AI Assistant!',
                welcomeDesc: 'Ask me anything about plant diseases, farming techniques, and crop management. I\'m here to help you 24/7.',
                features: [
                    'Identify and diagnose plant diseases',
                    'Get treatment recommendations',
                    'Learn about preventive measures',
                    'Understand farming best practices'
                ]
            },
            quickQuestions: 'Quick Questions',
            typeQuestion: 'Type your question here...'
        },
        chatWithAI: 'Chat with AI Assistant',
        askQuestion: 'Ask a question...',
        send: 'Send',
        typing: 'AI is typing...',

        // Team page
        team: {
            title: 'About the Developer',
            subtitle: 'Personal AIML Project',
            responsibilities: 'Responsibilities',
            about: 'About This Project',
            aboutDesc: 'AgriVision is an AI-powered plant disease detection system developed by Aman Kumar Bind as a personal AIML project. This project demonstrates end-to-end machine learning development, from model training to full-stack web deployment, with the mission to help farmers identify and treat plant diseases early.',
            techStack: 'Tech Stack',
            duration: 'Project Duration'
        },

        // Errors
        error: 'Error',
        errorOccurred: 'An error occurred',
        tryAgain: 'Try Again',
        noImageSelected: 'Please select an image first',

        // Common
        loading: 'Loading...',
        cancel: 'Cancel',
        close: 'Close',
        save: 'Save',
        delete: 'Delete',
    },

    hi: {
        // Navigation
        nav: {
            home: 'होम',
            detect: 'रोग पहचानें',
            chat: 'चैट',
            team: 'बारे में',
        },

        // Home page
        home: {
            title: 'AgriVision',
            subtitle: 'AI-संचालित पौधे रोग पहचान',
            description: 'शीघ्र पहचान, स्वस्थ फसलें, बेहतर उपज। अपने पौधे की तस्वीर अपलोड करें और उन्नत AI तकनीक द्वारा संचालित तत्काल रोग निदान प्राप्त करें।',
            startDetection: 'पहचान शुरू करें',
            liveDemo: 'चैट सहायक आज़माएं',
            powerfulFeatures: 'शक्तिशाली विशेषताएं',
            howItWorks: 'यह कैसे काम करता है',
            readyToProtect: 'अपनी फसलों की रक्षा के लिए तैयार हैं?',
            getStartedFree: 'मुफ्त शुरू करें',
            features: {
                aiDetection: {
                    title: 'AI-संचालित पहचान',
                    desc: 'सटीक रोग पहचान के लिए 70,000+ छवियों पर प्रशिक्षित उन्नत डीप लर्निंग मॉडल'
                },
                chatbot: {
                    title: 'विशेषज्ञ AI सहायक',
                    desc: 'हमारे बुद्धिमान चैटबॉट के साथ अपने खेती के सवालों के तत्काल जवाब पाएं'
                },
                multilingual: {
                    title: 'बहुभाषी समर्थन',
                    desc: 'भारत भर के किसानों की मदद के लिए अंग्रेजी और हिंदी में उपलब्ध'
                },
                treatment: {
                    title: 'उपचार सिफारिशें',
                    desc: 'कार्रवाई योग्य उपचार योजनाएं और रोकथाम रणनीतियां प्राप्त करें'
                },
                explainable: {
                    title: 'व्याख्यात्मक AI',
                    desc: 'स्पष्ट स्पष्टीकरण के साथ समझें कि AI ने अपना निदान क्यों किया'
                },
                plants: {
                    title: '12+ पौधों की प्रजातियां',
                    desc: 'टमाटर, आलू, मक्का और अधिक सहित प्रमुख फसलों के लिए समर्थन'
                }
            },
            steps: {
                upload: {
                    title: 'छवि अपलोड करें',
                    desc: 'प्रभावित पौधे की पत्ती की तस्वीर लें या अपलोड करें'
                },
                analyze: {
                    title: 'AI विश्लेषण',
                    desc: 'हमारा AI मॉडल वास्तविक समय में छवि का विश्लेषण करता है'
                },
                results: {
                    title: 'परिणाम प्राप्त करें',
                    desc: 'तुरंत निदान और उपचार सिफारिशें प्राप्त करें'
                }
            },
            stats: {
                accuracy: 'सटीकता',
                diseases: 'रोग',
                plants: 'पौधे',
                images: 'प्रशिक्षण छवियां'
            }
        },
        welcomeTitle: 'AI-संचालित पौधे रोग पहचान',
        welcomeSubtitle: 'शीघ्र पहचान, स्वस्थ फसलें, बेहतर उपज',
        getStarted: 'शुरू करें',
        learnMore: 'और जानें',

        // Features
        features: 'विशेषताएं',
        accurateDetection: 'सटीक पहचान',
        accurateDetectionDesc: '38 पौधों की बीमारियों में 96% सटीकता',
        instantResults: 'तुरंत परिणाम',
        instantResultsDesc: 'एक सेकंड से कम में पूर्वानुमान प्राप्त करें',
        expertAdvice: 'विशेषज्ञ सलाह',
        expertAdviceDesc: 'AI-संचालित उपचार सिफारिशें',

        // Stats
        accuracy: 'सटीकता',
        diseases: 'रोग पहचाने गए',
        plants: 'पौधों की प्रजातियां',

        // Predict page
        predict: {
            title: 'पौधे रोग पहचान',
            subtitle: 'पौधों की बीमारियों का पता लगाने के लिए एक छवि अपलोड करें या अपना कैमरा उपयोग करें',
            uploadTab: 'तस्वीर अपलोड करें',
            cameraTab: 'कैमरा उपयोग करें',
            dragDrop: 'यहां एक तस्वीर खींचें और छोड़ें, या चयन करने के लिए क्लिक करें',
            supports: 'समर्थित: JPG, PNG (अधिकतम 10MB)',
            startCamera: 'कैमरा शुरू करें',
            capture: 'कैप्चर और विश्लेषण करें',
            analyzing: 'विश्लेषण कर रहे हैं...',
            analyze: 'तस्वीर का विश्लेषण करें',
            uploadAnother: 'एक और तस्वीर अपलोड करें',
            uploadToSee: 'परिणाम देखने के लिए एक तस्वीर अपलोड करें',
            result: {
                healthy: 'पौधा स्वस्थ है!',
                diseased: 'रोग का पता चला',
                plant: 'पौधा',
                status: 'स्थिति',
                disease: 'रोग',
                confidence: 'विश्वास',
                top5: 'शीर्ष 5 पूर्वानुमान',
                recommendations: 'उपचार सिफारिशें',
                preventive: 'निवारक उपाय',
                fungicides: 'अनुशंसित फफूंदनाशक',
                precautions: 'सावधानियां',
                organic: 'जैविक विकल्प'
            }
        },
        uploadImage: 'तस्वीर अपलोड करें',
        useCamera: 'कैमरा उपयोग करें',
        dragDrop: 'यहां एक तस्वीर खींचें और छोड़ें, या चयन करने के लिए क्लिक करें',
        analyzing: 'विश्लेषण कर रहे हैं...',
        analyzeImage: 'तस्वीर का विश्लेषण करें',

        // Results
        results: 'परिणाम',
        plantName: 'पौधा',
        diseaseName: 'रोग',
        confidence: 'विश्वास',
        healthy: 'स्वस्थ',
        recommendations: 'उपचार की सिफारिशें',
        fungicides: 'अनुशंसित फफूंदनाशक',
        organicOptions: 'जैविक विकल्प',
        precautions: 'सावधानियां',

        // Chat
        chat: {
            title: 'AI सहायक',
            context: 'संदर्भ',
            askAnything: 'मुझसे पौधों की बीमारियों और उपचार के बारे में कुछ भी पूछें!',
            chatPage: {
                title: 'AI पौधे रोग सहायक',
                subtitle: 'पौधों की बीमारियों और खेती पर विशेषज्ञ सलाह प्राप्त करें',
                welcome: 'AgriVision AI सहायक में आपका स्वागत है!',
                welcomeDesc: 'मुझसे पौधों की बीमारियों, खेती की तकनीकों और फसल प्रबंधन के बारे में कुछ भी पूछें। मैं 24/7 आपकी मदद के लिए यहां हूं।',
                features: [
                    'पौधों की बीमारियों की पहचान और निदान',
                    'उपचार की सिफारिशें प्राप्त करें',
                    'निवारक उपायों के बारे में जानें',
                    'खेती के सर्वोत्तम अभ्यासों को समझें'
                ]
            },
            quickQuestions: 'त्वरित प्रश्न',
            typeQuestion: 'अपना प्रश्न यहां टाइप करें...'
        },
        chatWithAI: 'AI सहायक के साथ चैट करें',
        askQuestion: 'एक सवाल पूछें...',
        send: 'भेजें',
        typing: 'AI टाइप कर रहा है...',

        // Team page
        team: {
            title: 'डेवलपर के बारे में',
            subtitle: 'व्यक्तिगत AIML परियोजना',
            responsibilities: 'जिम्मेदारियां',
            about: 'इस परियोजना के बारे में',
            aboutDesc: 'AgriVision एक AI-संचालित पौधे रोग पहचान प्रणाली है जिसे अमन कुमार बिंद द्वारा एक व्यक्तिगत AIML परियोजना के रूप में विकसित किया गया है। यह परियोजना मॉडल प्रशिक्षण से लेकर पूर्ण-स्टैक वेब तैनाती तक, एंड-टू-एंड मशीन लर्निंग विकास को प्रदर्शित करती है, जिसका उद्देश्य किसानों को पौधों की बीमारियों की शीघ्र पहचान और उपचार में मदद करना है।',
            techStack: 'तकनीकी स्टैक',
            duration: 'परियोजना अवधि'
        },

        // Errors
        error: 'त्रुटि',
        errorOccurred: 'एक त्रुटि हुई',
        tryAgain: 'पुनः प्रयास करें',
        noImageSelected: 'कृपया पहले एक तस्वीर चुनें',

        // Common
        loading: 'लोड हो रहा है...',
        cancel: 'रद्द करें',
        close: 'बंद करें',
        save: 'सहेजें',
        delete: 'हटाएं',
    },
};

// Helper function to get translation
export function t(key: string, lang: Language = 'en'): string {
    const keys = key.split('.');
    let value: any = translations[lang];

    for (const k of keys) {
        value = value?.[k];
    }

    return value || key;
}
