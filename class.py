import streamlit as st
import requests

st.set_page_config(page_title="UNIT CONVERTER", page_icon="📊")

# Conversion factors dictionary
conversion_factors = {
    "Length": {
        ("Metre", "Kilometre"): 0.001,
        ("Kilometre", "Metre"): 1000,
        ("Foot", "Metre"): 0.3048,
        ("Metre", "Foot"): 3.28084,
        ("Inch", "Centimetre"): 2.54,
        ("Centimetre", "Inch"): 0.393701,
        ("Metre", "Centimetre"): 100,
        ("Centimetre", "Metre"): 0.01,
        ("Metre", "Inch"): 39.3701,
        ("Inch", "Metre"): 0.0254,
        ("Foot", "Inch"): 12,
        ("Inch", "Foot"): 1/12,
    },
    "Weight": {
        ("Kilogram", "Gram"): 1000,
        ("Gram", "Kilogram"): 0.001,
        ("Pound", "Kilogram"): 0.453592,
        ("Kilogram", "Pound"): 2.20462,
    },
    "Temperature": {
        ("Celsius", "Fahrenheit"): lambda c: (c * 9/5) + 32,
        ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9,
        ("Celsius", "Kelvin"): lambda c: c + 273.15,
        ("Kelvin", "Celsius"): lambda k: k - 273.15,
        ("Fahrenheit", "Kelvin"): lambda f: (f - 32) * 5/9 + 273.15,
        ("Kelvin", "Fahrenheit"): lambda k: (k - 273.15) * 9/5 + 32,
    },
    "Speed": {
        ("Kilometre per hour", "Metre per second"): 0.277778,
        ("Metre per second", "Kilometre per hour"): 3.6,
        ("Miles per hour", "Kilometre per hour"): 1.60934,
        ("Kilometre per hour", "Miles per hour"): 0.621371,
    },
    "Energy": {
        ("Joule", "Kilojoule"): 0.001,
        ("Kilojoule", "Joule"): 1000,
        ("Calorie", "Joule"): 4.184,
        ("Joule", "Calorie"): 0.239006,
    },
    "Volume": {
        ("Litre", "Millilitre"): 1000,
        ("Millilitre", "Litre"): 0.001,
        ("Gallon", "Litre"): 3.78541,
        ("Litre", "Gallon"): 0.264172,
    },
    "Time": {
        ("Second", "Minute"): 1/60,
        ("Minute", "Second"): 60,
        ("Minute", "Hour"): 1/60,
        ("Hour", "Minute"): 60,
        ("Hour", "Day"): 1/24,
        ("Day", "Hour"): 24,
        ("Day", "Week"): 1/7,
        ("Week", "Day"): 7,
        ("Second", "Hour"): 1/3600,
        ("Hour", "Second"): 3600,
        ("Second", "Day"): 1/86400,
        ("Day", "Second"): 86400,
        ("Second", "Week"): 1/604800,
        ("Week", "Second"): 604800,
    }
}

units = {
    "Length": ["Metre", "Kilometre", "Foot", "Inch", "Centimetre"],
    "Weight": ["Kilogram", "Gram", "Pound"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Speed": ["Kilometre per hour", "Metre per second", "Miles per hour"],
    "Energy": ["Joule", "Kilojoule", "Calorie"],
    "Volume": ["Litre", "Millilitre", "Gallon"],
    "Currency": ["USD", "EUR", "PKR", "INR", "GBP"],
    "Time": ["Second", "Minute", "Hour", "Day", "Week"]
}

def convert(value, from_unit, to_unit, category):
    if from_unit == to_unit:
        return value
    
    if category == "Currency":
        return convert_currency(value, from_unit, to_unit)
    
    conversion = conversion_factors.get(category, {}).get((from_unit, to_unit))
    
    if callable(conversion):
        return round(conversion(value), 2)
    
    return round(value * conversion, 8) if conversion is not None else "Invalid conversion"

def convert_currency(amount, from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            rates = response.json().get("rates", {})
            return round(amount * rates.get(to_currency, 1), 2)
    except:
        return "Error fetching rates"
    
    return "Invalid conversion"

st.markdown(
    """
    <style>
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .animated-heading {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-transform: uppercase;
        background: linear-gradient(-45deg, #ff4500, #ff5733, #ff8c00, #ff2200, #ff6b00);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientFlow 3s ease infinite;
    }
    </style>
    <h1 class="animated-heading">Ultimate Unit Converter</h1>
    """,
    unsafe_allow_html=True
)


st.markdown("<p style='text-align: center; font-style: italic; font-size: 18px;'>Effortless Conversions, Anytime, Anywhere!</p>", unsafe_allow_html=True)
category = st.selectbox("Select Category", list(units.keys()))
input_value = st.number_input("Enter Value", value=1.00, step=0.01)


col1, col2, col3 = st.columns([1.5, 0.2, 1.5])

with col1:
    from_unit = st.selectbox("From", units[category], key="from_unit")
with col2:
    st.markdown("<div style='text-align: center; font-size: 31px;'></div>", unsafe_allow_html=True)
with col3:
    to_unit = st.selectbox("To", units[category], key="to_unit")

st.markdown(
    """
    <style>
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stButton>button {
        display: block;
        margin: auto;  
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        text-transform: uppercase;
        padding: 10px 60px;
        border: none;
        border-radius: 8px;
        background: linear-gradient(45deg, #ff4500, #ff5733, #ff8c00, #ff2200, #ff6b00);
        background-size: 300% 300%;
        color: white !important;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        animation: gradientFlow 3s ease infinite;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        opacity: 0.9;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Convert"):
        result = convert(input_value, from_unit, to_unit, category)
        st.markdown(
            f'''
            <p style="color: rgb(255, 72, 0); font-size: 20px; font-weight: bold; text-align: center;">
                {input_value} {from_unit} is equal to {result} {to_unit}.
            </p>
            ''',
            unsafe_allow_html=True
        )
        st.balloons()  # Ye sirf button click hone ke baad execute hoga

#Footer
st.markdown("<br><br><p style='text-align: center; color:rgb(255, 72, 0)'>Created by Bilal Hassan</p>", unsafe_allow_html=True)
 