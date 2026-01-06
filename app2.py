import streamlit as st
import tensorflow as tf
from tensorflow.keras import layers
from PIL import Image
import numpy as np
import time
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Fish Identifier Pro", 
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# ADVANCED CUSTOM CSS - MODIFIED UI
# ----------------------------
st.markdown("""
    <style>
    /* IMPORT MODERN FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* 1. MAIN APP BACKGROUND - FIXED LIGHT OCEAN BLUE */
    .stApp {
        background-color: #E0F7FA; /* Light Ocean Blue */
        background-image: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 100%);
        font-family: 'Inter', sans-serif;
    }

    /* 2. SIDEBAR BACKGROUND - DARK OCEAN BLUE ANIMATION */
    [data-testid="stSidebar"] {
        /* Dark Ocean Blue Gradient */
        background: linear-gradient(135deg, #0f2027 0%, #203a43 25%, #2c5364 50%, #000428 75%, #004e92 100%);
        background-size: 400% 400%;
        animation: oceanWave 15s ease infinite;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Animation Keyframes */
    @keyframes oceanWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Make Sidebar Content Visible (White Text) */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* 3. MAIN CONTENT TEXT VISIBILITY (DARK BLUE TEXT FOR LIGHT BG) */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        color: #006064 !important; /* Dark Cyan/Blue for headers */
        font-weight: 700;
    }

    p, span, div, label {
        color: #01579B; /* Dark Blue for normal text */
    }

    /* GLASSMORPHISM CONTAINERS - ADAPTED FOR LIGHT BACKGROUND */
    .glass-container {
        background: rgba(255, 255, 255, 0.7); /* More opaque for light mode */
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.10); /* Softer shadow */
        margin: 20px 0;
    }

    /* HERO SECTION TEXT */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        /* Darker Gradient for visibility on light bg */
        background: linear-gradient(135deg, #0277BD 0%, #006064 100%); 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        animation: fadeInDown 1s ease-out;
        
        /* Flexbox for centering logo and text */
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        color: #455A64 !important; /* Grey-Blue */
        text-align: center;
        margin-bottom: 30px;
        animation: fadeInUp 1s ease-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* FILE UPLOADER */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.6);
        border: 2px dashed #0288D1; /* Blue dashed border */
        border-radius: 20px;
        padding: 40px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        background: rgba(255, 255, 255, 0.9);
        border-color: #01579B;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #01579B !important;
        font-weight: 600;
    }

    /* BUTTONS */
    .stButton>button {
        width: 100%;
        height: 60px;
        border-radius: 15px;
        background: linear-gradient(135deg, #0288D1, #0097A7); /* Solid Blue Gradient button */
        color: white !important;
        border: none;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0, 151, 167, 0.3);
        font-family: 'Space Grotesk', sans-serif;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 151, 167, 0.5);
    }
    /* Button text specific override */
    .stButton>button p {
        color: white !important; 
    }

    /* METRIC CARDS */
    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #546E7A !important;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #01579B !important;
    }

    /* TABLE STYLING */
    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        background: white;
    }
    .custom-table th {
        background: #0288D1; /* Solid Blue Header */
        color: #ffffff !important;
        padding: 15px;
        text-align: left;
        font-weight: 700;
    }
    .custom-table td {
        background: #ffffff;
        color: #37474F !important; /* Dark Grey Text */
        padding: 12px 15px;
        border-bottom: 1px solid #ECEFF1;
    }
    .custom-table tr:hover td {
        background: #F1F8E9;
    }

    /* SIDEBAR USER PROFILE */
    .user-profile {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .user-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 0 auto 15px;
        border: 3px solid rgba(255, 255, 255, 0.5);
    }

    /* TAB STYLE OVERRIDES */
    .stTabs [data-baseweb="tab"] {
        color: #546E7A; /* Inactive tab color */
    }
    .stTabs [aria-selected="true"] {
        color: #0277BD !important; /* Active tab color */
        background-color: rgba(2, 119, 189, 0.1) !important;
    }

    /* SPINNER */
    .stSpinner > div {
        border-top-color: #0288D1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# PARAMETERS (PRESERVED)
# ----------------------------
IMG_SIZE = (224, 224)
MODEL_PATH = "best_model.h5" 

# ----------------------------
# CUSTOM SE BLOCK (PRESERVED)
# ----------------------------
def se_block(input_tensor, reduction=16):
    channels = input_tensor.shape[-1]
    se = layers.GlobalAveragePooling2D()(input_tensor)
    se = layers.Dense(channels // reduction, activation='relu')(se)
    se = layers.Dense(channels, activation='sigmoid')(se)
    x = layers.Multiply()([input_tensor, se])
    return x

custom_objects = {"se_block": se_block}

# ----------------------------
# LOAD MODEL (PRESERVED)
# ----------------------------
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model. Error: {e}")
        return None

model = load_model()

# ----------------------------
# CLASS NAMES & DATA (PRESERVED)
# ----------------------------
CLASS_NAMES = [
    'Baim Fish', 'Bata Fish', 'Bele Fish', 'Foli fish', 'Kholisha Fish',
    'Mola fish', 'Mrigel Fish', 'Pabda fish', 'Prawns', 'Puti fish',
    'Shing mach', 'Shrimps', 'Taki fish', 'Tengra', 'koi fish', 'telapia'
]

FISH_INFO = {
    'Baim Fish': {
        'Local Name': 'Tara Baim Fish',
        'English Name': 'Lesser Spiny Eel',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii / Teleostei', 'Order': 'Synbranchiformes', 'Family': 'Mastacembelidae', 'Genus': 'Macrognathus', 'Species': 'Macrognathus aculeatus'},
        'Nutrition': {'Moisture': '~77-80 g', 'Protein (Crude)': '17-20 g', 'Total Fat (Lipid)': '~2-4 g', 'Ash (Minerals)': '~1.0-2.5 g', 'Iron (Fe)': '~1.4-2.0 mg', 'Calcium (Ca)': '~120-150 mg', 'Zinc (Zn)': '1.0-1.5 mg', 'Vitamin A': '~50-150 µg RAE'}
    },
    'Bata Fish': {
        'Local Name': 'Bata Fish',
        'English Name': 'Bata Labeo',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Cypriniformes', 'Family': 'Cyprinidae', 'Genus': 'Labeo', 'Species': 'Labeo bata'},
        'Nutrition': {'Energy': '100-101 kcal', 'Moisture': '72-74 g', 'Protein': '15.6-18.5 g', 'Total Fat (Lipid)': '~3.7-4.2 g', 'Saturated Fat': '~2.15 g', 'Ash (Minerals)': '2.2-4.7 g', 'Calcium (Ca)': '~211-250 mg', 'Iron (Fe)': '~0.07-1.4 mg', 'Phosphorus (P)': '~171-210 mg', 'Omega-3 Fatty Acids': '~0.3-0.4 g'}
    },
    'Bele Fish': {
        'Local Name': 'Bele fish',
        'English Name': 'Tank Goby',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Gobiiformes', 'Family': 'Gobiidae', 'Genus': 'Glossogobius', 'Species': 'Glossogobius giuris'},
        'Nutrition': {'Energy': '100-147 kcal', 'Protein': '17-19 g', 'Total Fat': '~3-4.5 g', 'Moisture': '72-76 g', 'Ash (Minerals)': '1.0-1.5 g', 'Calcium (Ca)': '~80-100 mg', 'Phosphorus (P)': '~200-240 mg', 'Iron (Fe)': '1.0-1.5 mg', 'Omega-3 (EPA + DHA)': '~100-300 mg'}
    },
    'Foli fish': {
        'Local Name': 'Foli fish',
        'English Name': 'Bronze Featherback',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Osteoglossiformes', 'Family': 'Notopteridae', 'Genus': 'Notopterus', 'Species': 'Notopterus notopterus'},
        'Nutrition': {'Energy': '100-110 kcal', 'Moisture': '~74-78 g', 'Protein': '19.5-22.2 g', 'Total Fat (Lipid)': '~1.0-4.0 g', 'Ash (Minerals)': '~1.7-2.0 g', 'Calcium (Ca)': '~80-100 mg', 'Iron (Fe)': '~1.0-1.5 mg', 'Phosphorus (P)': '~180-220 mg', 'Omega-3 (EPA + DHA)': '~100-300 mg'}
    },
    'Kholisha Fish': {
        'Local Name': 'Kholisa fish',
        'English Name': 'Dwarf Gourami',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Anabantiformes', 'Family': 'Osphronemidae', 'Genus': 'Trichogaster', 'Species': 'Trichogaster lalius'},
        'Nutrition': {'Energy': '~80-100 kcal', 'Moisture': '~76-80 g', 'Protein': '15.0-17.5 g', 'Total Fat (Lipid)': '~2.0-3.5 g', 'Ash (Minerals)': '~2.0-4.5 g', 'Calcium (Ca)': '~250-500 mg', 'Iron (Fe)': '~3.0-5.0 mg', 'Phosphorus (P)': '~150-200 mg', 'Omega-3 (EPA + DHA)': '~200-350 mg'}
    },
    'koi fish': {
        'Local Name': 'Koi fish',
        'English Name': 'Climbing Perch',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Anabantiformes', 'Family': 'Anabantidae', 'Genus': 'Anabas', 'Species': 'Anabas testudineus'},
        'Nutrition': {'Energy': '100-105 kcal', 'Moisture': '76-79 g', 'Protein': '16.5-18.0 g', 'Total Fat (Lipid)': '3.0-3.8 g', 'Ash (Minerals)': '~1.5-2.0 g', 'Calcium (Ca)': '~250-350 mg', 'Phosphorus (P)': '~150-200 mg', 'Iron (Fe)': '~1.5-2.5 mg', 'Vitamin D': '100-300 IU', 'Omega-3 (EPA + DHA)': '~150-300 mg'}
    },
    'Mola fish': {
        'Local Name': 'Mola Fish',
        'English Name': 'Mola Carplet',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Cypriniformes', 'Family': 'Danionidae', 'Genus': 'Amblypharyngodon', 'Species': 'Amblypharyngodon mola'},
        'Nutrition': {'Energy': '~98-106 kcal', 'Moisture': '~75-77 g', 'Protein': '14.7-18.2 g', 'Total Fat (Lipid)': '~3.0-5.0 g', 'Ash (Minerals)': '~3.5-4.0 g', 'Vitamin A (Retinol)': '~1960-2503 µg RAE', 'Calcium (Ca)': '~850-1400 mg', 'Iron (Fe)': '~5.0-19.0 mg', 'Phosphorus (P)': '~700-900 mg', 'Omega-3 (DHA)': '1.0-2.9 mg'}
    },
    'Mrigel Fish': {
        'Local Name': 'Mrigel Fish',
        'English Name': 'Mrigal Carp',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Cypriniformes', 'Family': 'Cyprinidae', 'Genus': 'Cirrhinus', 'Species': 'Cirrhinus mrigala'},
        'Nutrition': {'Energy': '110-130 kcal', 'Moisture': '74-76 g', 'Protein': '18.5-20.0 g', 'Total Fat (Lipid)': '~3.0-5.0 g', 'Saturated Fat': '~1.0-1.5 g', 'Ash (Minerals)': '~1.0-1.2 g', 'Calcium (Ca)': '~50-80 mg', 'Phosphorus (P)': '~200-250 mg', 'Iron (Fe)': '~1.0-1.5 mg', 'Omega-3 (EPA + DHA)': '~150-300 mg', 'Cholesterol': '~60-70 mg'}
    },
    'Pabda fish': {
        'Local Name': 'Pabda Fish',
        'English Name': 'Pabda Catfish or Indian Butter Catfish',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Siluriformes', 'Family': 'Siluridae', 'Genus': 'Ompok', 'Species': 'Ompok pabda'},
        'Nutrition': {'Energy': '115-130 kcal', 'Moisture': '74-77 g', 'Protein': '17.5-20.0 g', 'Total Fat (Lipid)': '~4.0-5.5 g', 'Ash (Minerals)': '~1.0-1.5 g', 'Calcium (Ca)': '~50-70 mg', 'Phosphorus (P)': '~180-220 mg', 'Iron (Fe)': '~1.0-2.0 mg', 'Omega-3 (EPA + DHA)': '~300-500 mg', 'Cholesterol': '~50-65 mg'}
    },
    'Prawns': {
        'Local Name': 'Kucho chingri (prawn)',
        'English Name': 'Small River Prawn',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Arthropoda', 'Sub-phylum': 'Crustacea', 'Class': 'Malacostraca', 'Order': 'Decapoda', 'Family': 'Palaemonidae', 'Genus': 'Palaemon', 'Species': 'Palaemon concinnus'},
        'Nutrition': {'Energy': '~85-100 kcal', 'Moisture': '~78-80 g', 'Protein': '~18-21 g', 'Total Fat (Lipid)': '~0.5-1.5 g', 'Ash (Minerals)': '~1.5-2.5 g', 'Calcium (Ca)': '~300-500 mg', 'Iron (Fe)': '~5-10 mg', 'Zinc (Zn)': '~2-3 mg', 'Cholesterol': '~100-150 mg', 'Vitamin B12': '~1.5-3 µg'}
    },
    'Puti fish': {
        'Local Name': 'Puti Fish',
        'English Name': 'Swamp Barb',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Cypriniformes', 'Family': 'Cyprinidae', 'Genus': 'Puntius', 'Species': 'Puntius sophore'},
        'Nutrition': {'Energy': '110-125 kcal', 'Moisture': '~74-78 g', 'Protein': '17.5-19.5 g', 'Total Fat (Lipid)': '~3.0-5.0 g', 'Ash (Minerals)': '~2.5-3.5 g', 'Calcium (Ca)': '~400-800 mg', 'Iron (Fe)': '~3.0-7.0 mg', 'Zinc (Zn)': '2.0-3.0 mg', 'Vitamin A (Retinol)': '~300-500 µg RAE', 'Omega-3 (EPA + DHA)': '300-500 mg'}
    },
    'Shing mach': {
        'Local Name': 'Shing Fish',
        'English Name': 'Stinging Catfish',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Siluriformes', 'Family': 'Heteropneustidae', 'Genus': 'Heteropneustes', 'Species': 'Heteropneustes fossilis'},
        'Nutrition': {'Energy': '100-115 kcal', 'Moisture': '~77-79 g', 'Protein': '17.5-20.0 g', 'Total Fat (Lipid)': '~2.0-4.0 g', 'Ash (Minerals)': '~1.0-1.5 g', 'Iron (Fe)': '~4.0-10.0 mg', 'Calcium (Ca)': '~200-300 mg', 'Phosphorus (P)': '~250-350 mg', 'Omega-3 (EPA + DHA)': '~300-500 mg'}
    },
    'Shrimps': {
        'Local Name': 'Kucho Chingri (Shrimp)',
        'English Name': 'Small River Shrimp',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Arthropoda', 'Sub-phylum': 'Crustacea', 'Class': 'Malacostraca', 'Order': 'Decapoda', 'Family': 'Penaeidae', 'Genus': 'Palaemon', 'Species': 'Palaemon styliferus'},
        'Nutrition': {'Energy': '~90-110 kcal', 'Moisture': '~78-80 g', 'Protein': '18.0-22.0 g', 'Total Fat (Lipid)': '~0.5-2.0 g', 'Ash (Minerals)': '~2.0-3.5 g', 'Calcium (Ca)': '~350-600 mg', 'Iron (Fe)': '~5.0-12.0 mg', 'Zinc (Zn)': '~2.0-4.0 mg', 'Omega-3 (EPA + DHA)': '~200-400 mg', 'Cholesterol': '~150-200 mg'}
    },
    'Taki fish': {
        'Local Name': 'Taki Fish',
        'English Name': 'Spotted Snakehead',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Perciformes', 'Family': 'Channidae', 'Genus': 'Channa', 'Species': 'Channa punctata'},
        'Nutrition': {'Energy': '100-110 kcal', 'Moisture': '~76-79 g', 'Protein': '18.5-20.5 g', 'Total Fat (Lipid)': '~2.0-3.5 g', 'Ash (Minerals)': '~1.0-1.5 g', 'Iron (Fe)': '~1.0-1.5 mg', 'Calcium (Ca)': '~60-90 mg', 'Phosphorus (P)': '~200-250 mg', 'Omega-3 (EPA + DHA)': '~300-500 mg', 'Cholesterol': '~60-70 mg'}
    },
    'telapia': {
        'Local Name': 'Telapia Fish',
        'English Name': 'Nile Tilapia',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Perciformes', 'Family': 'Cichlidae', 'Genus': 'Oreochromis', 'Species': 'Oreochromis niloticus'},
        'Nutrition': {'Energy': '~95-128 kcal', 'Moisture': '~78-80 g', 'Protein': '20.0-22.0 g', 'Total Fat (Lipid)': '~1.0-3.0 g', 'Saturated Fat': '~0.5-1.0 g', 'Ash (Minerals)': '~1.0-1.5 g', 'Potassium (K)': '300-400 mg', 'Phosphorus (P)': '~170-200 mg', 'Vitamin B12': '~2.0-3.5 µg', 'Omega-3 (EPA + DHA)': '~50-150 mg'}
    },
    'Tengra': {
        'Local Name': 'Tengra Fish',
        'English Name': 'Tengra Catfish',
        'Taxonomy': {'Kingdom': 'Animalia', 'Phylum': 'Chordata', 'Sub-phylum': 'Vertebrata', 'Class': 'Actinopterygii', 'Order': 'Siluriformes', 'Family': 'Bagridae', 'Genus': 'Mystus', 'Species': 'Mystus tengara'},
        'Nutrition': {'Energy': '115-135 kcal', 'Moisture': '~72-76 g', 'Protein': '16.5-18.5 g', 'Total Fat (Lipid)': '~5.0-7.0 g', 'Ash (Minerals)': '~1.0-1.5 g', 'Iron (Fe)': '~3.0-5.0 mg', 'Calcium (Ca)': '~100-150 mg', 'Phosphorus (P)': '200-250 mg', 'Omega-3 (EPA + DHA)': '~500-800 mg', 'Cholesterol': '~70-85 mg'}
    }
}

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("""
        <div class="user-profile">
            <img src="https://cdn-icons-png.flaticon.com/512/9187/9187604.png" class="user-avatar">
            <h3>Welcome!</h3>
            <p>user123@gmail.com</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📖 Guide")
    st.info("1. **Upload** a clear photo\n2. **Analyze** the species\n3. **Explore** nutrition data")
    
    st.markdown("### ⚠️ Note")
    st.caption("Please upload a focused photo taken with your phone (JPG, JPEG, or PNG). Downloaded images from online sources are not allowed. The model can give more accurate predictions from a single input image.")
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; font-size: 0.8rem; opacity: 0.7;'>v1.0.0 | Tensorflow & Streamlit | Developed by Bishal Biswas and Md. Mohtashim Masuk</div>", unsafe_allow_html=True)

# ----------------------------
# MAIN PREDICTION LOGIC
# ----------------------------
def predict_image(image, model):
    img = image.convert("RGB").resize(IMG_SIZE)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    preds = model.predict(img_array)[0]
    top_index = np.argmax(preds)
    top_confidence = preds[top_index] * 100
    top_class = CLASS_NAMES[top_index]
    
    return top_class, top_confidence

# ----------------------------
# HERO SECTION WITH LOGO
# ----------------------------
# NOTE: Replace 'LOGO_URL' with the path to your local 'logo.png' or a direct URL
LOGO_URL = "https://png.pngtree.com/png-clipart/20250105/original/pngtree-fish-logo-png-image_19822676.png" 

st.markdown(f"""
    <div class="hero-title">
        <img src="{LOGO_URL}" style="height: 70px; width: 70px; border-radius: 50%; vertical-align: middle; margin-right: 15px; border: 2px solid #0277BD; object-fit: cover;">
        Fish Detector
    </div>
    """, unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">An automated system for species identification & nutrition analysis</div>', unsafe_allow_html=True)

# ----------------------------
# MAIN UI
# ----------------------------
# Center the file uploader using columns
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Drag and drop your fish image here")

if uploaded_file is not None and model is not None:
    # Use container for the glass effect on results
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Layout: Image on Left, Action on Right
    img_col, act_col = st.columns([1, 1], gap="large")
    
    image = Image.open(uploaded_file)
    
    with img_col:
        st.image(image, caption="Source Image", use_container_width=True)
        
    with act_col:
        st.markdown("### 🔍 Ready to Identify?")
        st.write("Our AI model will analyze patterns to detect the species and retrieve nutritional data.")
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Identify Species")

    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        with st.spinner("🧠 Neural Network Analyzing..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            prediction, confidence = predict_image(image, model)
            progress_bar.empty()
            
        # ----------------------------
        # RESULTS DISPLAY
        # ----------------------------
        if confidence < 90.0:
            st.error("❌ UNIDENTIFIED SPECIES")
            st.markdown(
                f"""
                <div class="stAlert" style="background: rgba(255, 0, 0, 0.1); border-color: rgba(255, 0, 0, 0.3);">
                    <h3 style="color: #c62828;">Low Confidence: {confidence:.2f}%</h3>
                    <p style="color: #c62828;">The system could not identify this fish with sufficient accuracy (Threshold: 90%). Please try a clearer image.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.balloons()
            details = FISH_INFO.get(prediction, {})
            
            # --- MAIN RESULT CARD ---
            st.markdown(f"""
            <div class="glass-container" style="text-align: center;">
                <h2>🎣 {details.get('Local Name', prediction)}</h2>
                <p style="font-size: 1.1rem; opacity: 0.8; color: #455A64;">{details.get('English Name', 'Unknown')}</p>
                <div style="margin-top: 15px; display: inline-block; padding: 5px 15px; background: rgba(2, 136, 209, 0.1); border-radius: 20px;">
                    <span style="color: #0277BD; font-weight: bold;">🎯 Confidence: {confidence:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- TABS FOR DETAILS ---
            tab1, tab2 = st.tabs(["🧬 Taxonomy", "🥗 Nutrition Profile"])
            
            # TAB 1: TAXONOMY
            with tab1:
                taxonomy = details.get('Taxonomy', {})
                if taxonomy:
                    tax_html = '<table class="custom-table"><tr><th>Rank</th><th>Scientific Name</th></tr>'
                    tax_order = ['Kingdom', 'Phylum', 'Sub-phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
                    
                    for key in tax_order:
                        val = taxonomy.get(key, 'N/A')
                        tax_html += f"<tr><td><b>{key}</b></td><td>{val}</td></tr>"
                    
                    tax_html += "</table>"
                    st.markdown(tax_html, unsafe_allow_html=True)
                else:
                    st.info("Taxonomy data unavailable.")

            # TAB 2: INTERACTIVE NUTRITION
            with tab2:
                nutrition = details.get('Nutrition', {})
                if nutrition:
                    st.markdown("#### ⚡ Key Nutrients (per 100g)")
                    
                    # Create a Grid for Key Metrics
                    n_col1, n_col2, n_col3 = st.columns(3)
                    
                    # Helper to create HTML cards
                    def create_card(title, value, icon):
                        return f"""
                        <div class="metric-card">
                            <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                            <div class="metric-title">{title}</div>
                            <div class="metric-value">{value}</div>
                        </div>
                        """
                    
                    with n_col1:
                        val = nutrition.get('Energy', 'N/A')
                        st.markdown(create_card("Energy", val, "⚡"), unsafe_allow_html=True)
                    with n_col2:
                        val = nutrition.get('Protein', nutrition.get('Protein (Crude)', 'N/A'))
                        st.markdown(create_card("Protein", val, "🥩"), unsafe_allow_html=True)
                    with n_col3:
                        val = nutrition.get('Total Fat (Lipid)', nutrition.get('Total Fat', 'N/A'))
                        st.markdown(create_card("Total Fat", val, "💧"), unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 📋 Detailed Breakdown")
                    
                    # Detailed Table for the rest
                    nut_html = '<table class="custom-table"><tr><th>Nutrient</th><th>Approximate Value</th></tr>'
                    for k, v in nutrition.items():
                        # Skip the ones we already showed in big cards to avoid redundancy, or show all
                        nut_html += f"<tr><td><b>{k}</b></td><td>{v}</td></tr>"
                    nut_html += "</table>"
                    st.markdown(nut_html, unsafe_allow_html=True)
                    
                else:
                    st.info("Nutrition data unavailable.")