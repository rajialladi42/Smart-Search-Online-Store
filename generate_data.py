"""
generate_data.py
Generates 5,000+ realistic electronics products into products.csv for Smart Search Online Store.
Categories (15):
- Laptops, Smartphones, Tablets, Headphones, Earbuds, Smart Watches,
  Monitors, Keyboards, Mice, Cameras, TVs, Speakers, Chargers, Power Banks, Accessories
"""

import csv
import os
import random

# Fixed seed for reproducible realistic generation
random.seed(42)

CATEGORIES_DATA = {
    "Laptops": {
        "brands": ["Apple", "Dell", "HP", "Lenovo", "ASUS", "Acer", "MSI", "Razer", "Samsung"],
        "series": [
            "ProBook 450", "IdeaPad Slim 5", "ZenBook Duo", "MacBook Pro M3", "MacBook Air M2",
            "XPS 15 Ultrabook", "Pavilion Gaming", "ROG Strix SCAR", "Legion Pro 7i", "ThinkPad X1 Carbon",
            "Swift Go 14", "Predator Helios 16", "Katana 15", "Blade 16 Gaming", "Galaxy Book4 Pro",
            "Envy x360 Convertible", "TUF Gaming A15", "Yoga 9i Dual Screen", "Vostro Business", "Inspiron 14 Plus"
        ],
        "chips": ["Intel Core i5-13500H", "Intel Core i7-14700HX", "Intel Core i9-14900KS", "AMD Ryzen 5 7600X", "AMD Ryzen 7 7840HS", "AMD Ryzen 9 7945HX", "Apple M2 Chip", "Apple M3 Pro Max"],
        "rams": ["8GB DDR5", "16GB DDR5", "32GB LPDDR5X", "64GB Unified RAM"],
        "storage": ["512GB NVMe SSD", "1TB Gen4 SSD", "2TB High-Speed SSD"],
        "displays": ["14-inch OLED 120Hz", "15.6-inch Full HD IPS", "16-inch 240Hz QHD Gaming Display", "13.6-inch Liquid Retina Display"],
        "price_range": (35000, 240000),
        "keywords": ["laptop", "notebook", "ultrabook", "gaming laptop", "computer", "portable pc", "workstation"],
        "images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Smartphones": {
        "brands": ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi", "Realme", "Motorola", "Vivo", "Nothing"],
        "series": [
            "iPhone 15 Pro Max", "Galaxy S24 Ultra", "Pixel 8 Pro", "OnePlus 12", "Xiaomi 14 Ultra",
            "iPhone 14 Plus", "Galaxy A55 5G", "Pixel 7a", "Nothing Phone (2)", "Realme GT 5 Pro",
            "Edge 50 Ultra", "Vivo X100 Pro", "Galaxy Z Flip 5", "iPhone 13 mini", "OnePlus Nord CE 4",
            "Redmi Note 13 Pro+", "Galaxy S23 FE", "Moto G84 5G", "Neo 9 Pro", "Edge 40 Neo"
        ],
        "chips": ["Snapdragon 8 Gen 3", "A17 Pro Bionic", "Tensor G3", "Dimensity 9300", "Snapdragon 7+ Gen 2"],
        "rams": ["8GB RAM", "12GB LPDDR5X", "16GB RAM"],
        "storage": ["128GB UFS 4.0", "256GB Storage", "512GB High Speed Storage", "1TB ROM"],
        "displays": ["6.7-inch AMOLED 120Hz", "6.1-inch Super Retina XDR", "6.8-inch Dynamic AMOLED 2X", "6.55-inch OLED 144Hz"],
        "price_range": (14999, 159999),
        "keywords": ["smartphone", "mobile phone", "android phone", "iphone", "5g mobile", "cellular device"],
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Tablets": {
        "brands": ["Apple", "Samsung", "Lenovo", "Xiaomi", "OnePlus", "Microsoft", "Realme"],
        "series": [
            "iPad Pro 12.9 M2", "iPad Air 5th Gen", "Galaxy Tab S9 Ultra", "Surface Pro 9", "Xiaomi Pad 6",
            "iPad 10th Generation", "Galaxy Tab A9+", "Lenovo Tab P12 Pro", "OnePlus Pad Go", "iPad mini 6",
            "Surface Go 3", "Tab M11 with Stylus", "Galaxy Tab S9 FE", "Redmi Pad SE", "Realme Pad 2"
        ],
        "chips": ["Apple M2", "Snapdragon 8 Gen 2", "MediaTek Helio G99", "Intel Core i5-1235U", "Snapdragon 870"],
        "rams": ["4GB RAM", "8GB RAM", "12GB RAM", "16GB RAM"],
        "storage": ["64GB", "128GB", "256GB", "512GB"],
        "displays": ["11-inch Liquid Retina", "12.4-inch Super AMOLED 120Hz", "10.6-inch 2K IPS", "14.6-inch Dynamic AMOLED"],
        "price_range": (12999, 134999),
        "keywords": ["tablet", "ipad", "android tablet", "tab", "digital notepad", "stylus screen"],
        "images": [
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Headphones": {
        "brands": ["Sony", "Bose", "Sennheiser", "Audio-Technica", "JBL", "Beats", "Skullcandy", "AKG"],
        "series": [
            "WH-1000XM5 Noise Cancelling", "QuietComfort 45", "Momentum 4 Wireless", "ATH-M50x Professional Studio",
            "Live 660NC Over-Ear", "Studio Pro Wireless", "Crusher Evo Bass", "K371 Over-Ear Studio",
            "WH-CH720N Wireless", "700 Noise Cancelling", "HD 560S Audiophile", "Tune 760NC Active Noise Cancelling"
        ],
        "chips": ["Custom ANC Audio Processor", "Dual V1 QN1 Processor", "Audiophile Transducer"],
        "rams": ["Bluetooth 5.3 + Multipoint", "LDAC Hi-Res Audio Certified", "Spatial Audio with Head Tracking"],
        "storage": ["30 Hours Battery", "40 Hours Playback", "50 Hours Long Battery Life", "60 Hours Extreme Playtime"],
        "displays": ["Active Noise Cancellation", "Memory Foam Cushioning", "Foldable Travel Design"],
        "price_range": (2499, 39999),
        "keywords": ["headphones", "over-ear headphones", "wireless headphones", "noise cancelling headphones", "bluetooth headset"],
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Earbuds": {
        "brands": ["Apple", "Sony", "Samsung", "Jabra", "Nothing", "JBL", "boAt", "OnePlus", "Soundcore"],
        "series": [
            "AirPods Pro 2nd Gen USB-C", "WF-1000XM5 Flagship TWS", "Galaxy Buds2 Pro", "Elite 8 Active Rugged",
            "Ear (2) Transparent TWS", "Live Pro 2 TWS", "Airdopes 441 Pro", "Buds Pro 2 Spatial Audio",
            "Liberty 4 NC Noise Cancelling", "AirPods 3rd Gen", "Space A40 Ultra Compact", "Nord Buds 2r"
        ],
        "chips": ["Apple H2 Chip", "Sony Integrated Processor V2", "Bluetooth 5.3 SoC"],
        "rams": ["Active Noise Cancellation ANC", "Transparency Ambient Mode", "IPX5 Sweat & Water Resistant"],
        "storage": ["28 Hours Total Playtime", "36 Hours Total Battery Case", "40 Hours Case Battery Life"],
        "displays": ["Wireless Qi Charging Case", "Dual Drivers Deep Bass", "Ergonomic In-Ear Fit"],
        "price_range": (1299, 24999),
        "keywords": ["earbuds", "true wireless earbuds", "tws", "airpods", "in-ear earphones", "bluetooth earbuds"],
        "images": [
            "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Smart Watches": {
        "brands": ["Apple", "Samsung", "Garmin", "Fitbit", "Amazfit", "Noise", "Fire-Boltt", "Fossil"],
        "series": [
            "Watch Series 9 GPS", "Watch Ultra 2 Rugged Titanium", "Galaxy Watch6 Classic LTE", "Forerunner 965 GPS Running",
            "Sense 2 Advanced Health", "GTR 4 Smart Sports Watch", "ColorFit Pro 5 Max", "Quantum Luxury Smartwatch",
            "Gen 6 Wellness Edition", "Galaxy Watch5 Pro", "Venu 3 AMOLED GPS", "T-Rex 2 Rugged Outdoor"
        ],
        "chips": ["Dual-Core S9 SiP", "Exynos W930", "Multi-GNSS Dual Frequency GPS"],
        "rams": ["Heart Rate & ECG Monitor", "SpO2 Blood Oxygen Tracker", "Sleep Stages & Stress Analysis"],
        "storage": ["7 Days Battery Life", "14 Days Battery", "36 Hours Smart Mode", "48 Hours Ultra Mode"],
        "displays": ["1.43-inch Always-On AMOLED", "Sapphire Crystal Glass Display", "1.96-inch HD Retina Display"],
        "price_range": (1999, 89999),
        "keywords": ["smart watch", "fitness tracker", "digital watch", "smartwatch", "apple watch", "running watch"],
        "images": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Monitors": {
        "brands": ["LG", "Dell", "Samsung", "ASUS", "BenQ", "Acer", "ViewSonic", "MSI", "Gigabyte"],
        "series": [
            "UltraGear 27-inch 240Hz OLED", "Odyssey G9 49-inch Curved DQHD", "UltraSharp 32-inch 4K USB-C Hub",
            "ROG Swift 360Hz Esports", "Mobiuz 34-inch Ultrawide Gaming", "Nitro 24-inch 165Hz IPS",
            "ColorPro 27-inch 4K AdobeRGB", "Optix MAG274QRF Rapid IPS", "M27Q 170Hz Gaming Monitor"
        ],
        "chips": ["AMD FreeSync Premium Pro", "NVIDIA G-Sync Compatible", "HDR400 Certified"],
        "rams": ["0.03ms Ultra-Low Response Time", "1ms GTG Fast Response", "99% sRGB Accurate Color"],
        "storage": ["HDMI 2.1 + DisplayPort 1.4", "USB Type-C 90W Power Delivery", "Dual HDMI 2.0 Ports"],
        "displays": ["4K UHD 3840x2160 Resolution", "QHD 2560x1440 165Hz", "FHD 1080p 144Hz Fast IPS"],
        "price_range": (7999, 129999),
        "keywords": ["monitor", "display screen", "gaming monitor", "4k monitor", "ultrawide screen", "pc display"],
        "images": [
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1547082299-de196ea013d6?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Keyboards": {
        "brands": ["Logitech", "Keychron", "Razer", "Corsair", "SteelSeries", "Redragon", "HyperX", "Ducky"],
        "series": [
            "MX Keys S Advanced Wireless", "K2 Wireless Hot-Swappable", "BlackWidow V4 Pro Mechanical",
            "K70 RGB Rapidfire", "Apex Pro OmniPoint Switches", "Kumara K552 RGB Mechanical",
            "Alloy Origins 60 Compact", "One 3 Mini Mechanical", "G915 LIGHTSPEED Wireless RGB"
        ],
        "chips": ["Optical-Mechanical Fast Switches", "Cherry MX Red Switches", "Gateron Brown Tactile Switches"],
        "rams": ["Per-Key RGB Backlighting", "Double-Shot PBT Keycaps", "Aircraft-Grade Aluminum Frame"],
        "storage": ["Triple Mode: 2.4GHz + BT + Cable", "Detachable Type-C Braided Cable", "Rechargeable 4000mAh Battery"],
        "displays": ["Full-Sized 104 Keys Layout", "Tenkeyless 80% Layout", "Compact 65% Form Factor"],
        "price_range": (1499, 22999),
        "keywords": ["keyboard", "mechanical keyboard", "wireless keyboard", "gaming keyboard", "ergonomic keyboard"],
        "images": [
            "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Mice": {
        "brands": ["Logitech", "Razer", "SteelSeries", "Corsair", "Glorious", "HyperX", "ASUS"],
        "series": [
            "MX Master 3S Ergonomic Wireless", "DeathAdder V3 Pro Wireless", "G502 X LIGHTSPEED Gaming Mouse",
            "Aerox 3 Wireless Ultra-Lightweight", "Model O Minus Gaming Mouse", "Pulsefire Haste 2 Wireless",
            "ROG Harpe Ace Aim Lab Edition", "Viper V2 Pro HyperSpeed", "G305 Wireless High Precision"
        ],
        "chips": ["Focus Pro 30K Optical Sensor", "HERO 25K Ultra Precision Sensor", "BAMF 2.0 26K Sensor"],
        "rams": ["63g Featherlight Weight", "Optical Mouse Switches Gen-3", "Quiet Click Electromagnetic Scroll"],
        "storage": ["80 Hours Continuous Playtime", "90 Hours Long Battery", "Up to 70 Days Rechargeable"],
        "displays": ["Programmable Macro Buttons", "PTFE Smooth Glide Mouse Skates", "Multi-Device Easy-Switch"],
        "price_range": (899, 14999),
        "keywords": ["mouse", "wireless mouse", "gaming mouse", "ergonomic mouse", "optical mouse"],
        "images": [
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Cameras": {
        "brands": ["Sony", "Canon", "Nikon", "Fujifilm", "Panasonic", "GoPro", "Insta360", "DJI"],
        "series": [
            "Alpha 7 IV Mirrorless Camera", "EOS R6 Mark II Full Frame", "Z6 II Mirrorless Hybrid",
            "X-T5 40MP APS-C Mirrorless", "Lumix GH6 4K Cinematic", "HERO 12 Black Action Camera",
            "X3 360-Degree Action Cam", "Osmo Pocket 3 4K Gimbal Camera", "Alpha 6700 Content Creator"
        ],
        "chips": ["BIONZ XR Image Processor", "DIGIC X High Speed Processor", "EXPEED 7 Dual Engine"],
        "rams": ["4K 60fps 10-Bit 4:2:2 Video", "Real-Time Eye Autofocus AI", "5-Axis In-Body Image Stabilization"],
        "storage": ["Dual SD UHS-II & CFexpress Slots", "UHS-I Fast Writing MicroSD Support", "High Speed CFe Slot"],
        "displays": ["Vari-Angle Touchscreen LCD", "High-Resolution OLED Electronic Viewfinder"],
        "price_range": (28999, 299999),
        "keywords": ["camera", "dslr camera", "mirrorless camera", "action camera", "4k video camera", "vlogging camera"],
        "images": [
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "TVs": {
        "brands": ["Samsung", "LG", "Sony", "TCL", "Hisense", "Xiaomi", "OnePlus", "VU"],
        "series": [
            "OLED evo C3 55-inch 4K Smart TV", "Neo QLED 65-inch 8K Quantum Matrix", "Bravia XR A80L 55-inch OLED",
            "Q7 QLED 65-inch 120Hz Google TV", "U7K Mini-LED 55-inch 144Hz", "Smart TV X Pro 43-inch 4K",
            "Q1 Series 55-inch 4K QLED", "The Frame 55-inch Art Mode TV", "Cinema TV Action 50-inch Dolby Vision"
        ],
        "chips": ["Cognitive Processor XR", "Neural Quantum Processor 4K", "α9 AI Processor Gen6 4K"],
        "rams": ["Dolby Vision IQ & Dolby Atmos", "120Hz Native Refresh Rate with VRR", "Quantum HDR 32X Supreme Contrast"],
        "storage": ["4x HDMI 2.1 Ports eARC Support", "32GB High Speed Storage for Apps"],
        "displays": ["4K Ultra HD 3840x2160 OLED Panel", "Quantum Dot Color Technology", "Anti-Glare Wide Viewing Angle"],
        "price_range": (21999, 289999),
        "keywords": ["tv", "smart tv", "oled tv", "4k television", "qled tv", "google tv", "home cinema"],
        "images": [
            "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1461151304267-38535e780c79?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Speakers": {
        "brands": ["JBL", "Bose", "Sony", "Marshall", "Sonos", "Harman Kardon", "Ultimate Ears", "boAt"],
        "series": [
            "Charge 5 Portable Bluetooth Speaker", "SoundLink Revolve+ II 360", "SRS-XG300 Wireless Party Speaker",
            "Emberton II Portable Rock Speaker", "Era 100 Smart Home Speaker", "Onyx Studio 8 Wireless Bluetooth",
            "Boom 3 360-Degree Waterproof", "Stone 1200 High Wattage Party Speaker", "Flip 6 Rugged Outdoor Speaker"
        ],
        "chips": ["Dual Passive Radiators Deep Bass", "Custom Tuned Acoustic Drivers", "Class-D Digital Amplifiers"],
        "rams": ["IP67 Dustproof and Waterproof", "PartyBoost Multiple Speaker Pairing", "Voice Assistant Built-In Alexa & Siri"],
        "storage": ["20 Hours Playtime Built-in Powerbank", "12 Hours Battery Portable", "30 Hours Extended Playtime"],
        "displays": ["Customizable EQ Companion App", "Multi-Color Dynamic LED Lighting Ring"],
        "price_range": (1799, 39999),
        "keywords": ["speaker", "bluetooth speaker", "wireless speaker", "party speaker", "soundbar", "home speaker"],
        "images": [
            "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Chargers": {
        "brands": ["Anker", "Belkin", "Ugreen", "Spigen", "Apple", "Samsung", "Baseus", "Portronics"],
        "series": [
            "GaNPrime 65W Fast Charger", "BoostCharge Pro 3-in-1 MagSafe", "Nexode 100W 4-Port GaN Desktop",
            "ArcStation Pro 45W Dual USB-C", "20W USB-C Power Adapter", "45W Super Fast Charging 2.0 Brick",
            "Blade 100W Ultra Slim GaN Charger", "Adapto 65W Multiport Fast Wall Charger", "30W Nano Compact GaN"
        ],
        "chips": ["GaN Gallium Nitride III Technology", "Power Delivery PD 3.0 & PPS Protocol", "ActiveShield 2.0 Temperature Monitor"],
        "rams": ["Multi-Protection Overvoltage Guard", "Foldable Travel Prongs Design", "Simultaneous 3-Device Charging"],
        "storage": ["Universal Laptop & Phone Compatibility", "Braided 100W Type-C Cable Included"],
        "displays": ["LED Power Status Indicator", "Smart Current Distribution System"],
        "price_range": (699, 9999),
        "keywords": ["charger", "fast charger", "gan charger", "usb-c adapter", "wall charger", "phone charger"],
        "images": [
            "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Power Banks": {
        "brands": ["Anker", "Xiaomi", "Romoss", "Ambrane", "Belkin", "Realme", "Baseus", "URBN"],
        "series": [
            "PowerCore 24K 140W Portable Charger", "20000mAh 33W Fast Charging Bank", "Sense 8+ 30000mAh High Capacity",
            "Stylo Pro 27000mAh 65W Output", "Magnetic Wireless MagSafe 10000mAh", "10000mAh 22.5W Two-Way Fast Charge",
            "Blade HD 20000mAh 100W Laptop Power Bank", "Pocket Size 10000mAh Ultra Compact"
        ],
        "chips": ["Smart Power Allocation IC", "High-Density Lithium Polymer Cells", "Short Circuit Safety Protection"],
        "rams": ["65W Laptop PD Fast Charging", "15W Qi Wireless Charging Pad", "Multi-Port Dual USB-C + Dual USB-A"],
        "storage": ["Airline Approved 99Wh Travel Friendly", "Overheat and Surge Auto Shutoff"],
        "displays": ["Smart Digital OLED Display for Remaining %", "LED Battery Level Indicator Bar"],
        "price_range": (999, 12999),
        "keywords": ["power bank", "portable charger", "battery pack", "external battery", "usb-c powerbank"],
        "images": [
            "https://images.unsplash.com/photo-1609592424364-c24459f0b18f?w=600&auto=format&fit=crop&q=80"
        ]
    },
    "Accessories": {
        "brands": ["Belkin", "Spigen", "Ugreen", "Logitech", "Portronics", "ESR", "CableCreation", "AmazonBasics"],
        "series": [
            "Aluminium Ergonomic Laptop Stand", "ScreenBar Halo Monitor Light Bar", "Thunderbolt 4 8-in-1 Docking Station",
            "Magnetic Wireless Car Mount Charger", "Tough Armor Shockproof Phone Case", "Braided 8K HDMI 2.1 Cable 2m",
            "Ergonomic Memory Foam Wrist Rest Pad", "AirTag Leather Keychain Protective Case", "Universal USB 3.0 Hub 4 Ports"
        ],
        "chips": ["High Quality Brushed Aviation Aluminum", "Shielded Anti-Interference Gold Plated Connectors"],
        "rams": ["Heat Dissipation Cooling Vent Design", "360-Degree Swivel Angle Adjustment"],
        "storage": ["Universal Fit for All Laptops & Devices", "Plug and Play No Drivers Needed"],
        "displays": ["Rubber Anti-Slip Silicone Pads", "Reinforced Strain Relief Durability"],
        "price_range": (399, 8999),
        "keywords": ["accessory", "laptop stand", "usb hub", "docking station", "cable", "phone case", "wrist rest"],
        "images": [
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80"
        ]
    }
}

MODIFIERS = [
    "Pro", "Max", "Ultra", "Plus", "Air", "Elite", "Prime", "Gaming Edition",
    "Special Edition", "Wireless", "Next-Gen", "Creator Series", "Studio", "Signature"
]

COLORS = ["Space Grey", "Midnight Black", "Silver Frost", "Cosmic Blue", "Rose Gold", "Titanium Grey", "Alpine White", "Emerald Green"]

def generate_products(target_count=5020):
    products = []
    pid = 1001
    
    categories = list(CATEGORIES_DATA.keys())
    per_cat = (target_count // len(categories)) + 15
    
    for cat_name in categories:
        data = CATEGORIES_DATA[cat_name]
        brands = data["brands"]
        series_list = data["series"]
        chips = data["chips"]
        rams = data["rams"]
        storage_list = data["storage"]
        displays = data["displays"]
        min_p, max_p = data["price_range"]
        images = data["images"]
        base_keywords = data["keywords"]
        
        cat_count = 0
        while cat_count < per_cat and len(products) < target_count:
            brand = random.choice(brands)
            base_series = random.choice(series_list)
            modifier = random.choice(MODIFIERS)
            color = random.choice(COLORS)
            chip = random.choice(chips)
            ram = random.choice(rams)
            storage = random.choice(storage_list)
            display = random.choice(displays)
            
            # Format product name
            # Make sure it creates realistic titles e.g. "Apple MacBook Pro M3 (16GB DDR5, 512GB NVMe SSD, Space Grey)"
            if brand in base_series:
                prod_name = f"{base_series} {modifier} - {color}"
            else:
                prod_name = f"{brand} {base_series} {modifier} - {color}"
                
            price = round(random.uniform(min_p, max_p) / 50) * 50
            rating = round(random.uniform(3.5, 4.9), 1)
            stock = random.choice([0, 5, 12, 25, 40, 75, 120, 200]) # some zero stock for DMGT filter testing
            
            # Rich description for TF-IDF / Cosine Similarity recommendation
            desc = (
                f"The {prod_name} delivers outstanding performance crafted by {brand} in the {cat_name} category. "
                f"Equipped with {chip} and powered with {ram} for seamless multitasking. Features {storage} "
                f"and an exceptional {display}. Finished in elegant {color} with durable premium craftsmanship. "
                f"Designed for modern professionals, creators, and tech enthusiasts looking for reliability and high efficiency."
            )
            
            # Keywords for search indexing
            keywords_set = set(base_keywords)
            keywords_set.add(brand.lower())
            keywords_set.add(cat_name.lower())
            keywords_set.add(color.lower())
            for word in base_series.lower().split():
                if len(word) > 2:
                    keywords_set.add(word)
            keywords = ", ".join(sorted(keywords_set))
            
            img_url = random.choice(images)
            
            product_id = f"PROD-{pid}"
            products.append({
                "ID": product_id,
                "Name": prod_name,
                "Category": cat_name,
                "Brand": brand,
                "Price": price,
                "Rating": rating,
                "Stock": stock,
                "Description": desc,
                "Image": img_url,
                "Keywords": keywords
            })
            
            pid += 1
            cat_count += 1
            
    return products

def main():
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv")
    products = generate_products(target_count=5050)
    
    print(f"Generating {len(products)} products into {target_path}...")
    
    with open(target_path, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["ID", "Name", "Category", "Brand", "Price", "Rating", "Stock", "Description", "Image", "Keywords"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            writer.writerow(p)
            
    print(f"Successfully generated {len(products)} products into products.csv!")

if __name__ == "__main__":
    main()
